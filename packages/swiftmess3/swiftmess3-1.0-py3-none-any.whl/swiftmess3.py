"""
Swiftmess3 is a Python module to parse SWIFT messages used for financial transactions in banking.
"""
# Copyright (c) 2012, Thomas Aglassinger
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import decimal
import logging
import re
from datetime import date, datetime

_log = logging.getLogger('swift')

__version__ = '1.0'

_FamtMarker = 'FAMT/'


class Error(Exception):
    pass


def message_items(readable):
    """
    Message items found in ``readable`` as tuples of the form ``(nestingLevel, type, value)`` with:

    * nestingLevel: level of nested blocks
    * type: one of: 'message', 'block', 'field', 'value'
    * value: for 'block' this is the block key, for 'field' this is the field name, 'value' this is the value
      and for 'message' this is ``None``.

    The messages have to be stored in EDIFACT / ISO 15022 format.
    """
    assert readable is not None

    # Possible values for ``state``.
    _BeforeStartOfBlock = 'BeforeStartOfBlock'
    _InBlockKey = 'InBlockKey'
    _InLine = 'InLine'
    _InFieldKey = 'InFieldKey'
    _InFieldValue = 'InFieldValue'
    _InValue = 'InValue'

    state = _BeforeStartOfBlock
    text = None
    blockKey = None
    fieldKey = None
    level = 0

    char = readable.read(1)
    while char:
        _log.debug(f'level={level}, char={char}, state={state}, text={text}')
        if char == '\r':
            pass
        elif state == _BeforeStartOfBlock:
            if char == '{':
                state = _InBlockKey
                level += 1
                text = ''
            elif char == '}':
                if level == 0:
                    raise Error(f'unmatched {char} outside of any block must be removed')
                level -= 1
            elif char == '\n':
                if level != 0:
                    raise Error(f'nested block must be closed (state={state}, level={level})')
                yield level, 'message', None
            elif char != '\r':
                raise Error(f'block must start with {{ instead of {char}')
        elif state == _InBlockKey:
            if char == ':':
                state = _InLine
                blockKey = int(text)
                yield level, 'block', blockKey
                text = None
            elif char.isdigit():
                text += char
            else:
                raise Error(f'block id must consist of decimal digits bug encountered {char}')
        elif state == _InLine:
            if char == '{':
                state = _InBlockKey
                level += 1
                text = ''
            elif char == '}':
                state = _BeforeStartOfBlock
                level -= 1
                assert level >= 0
            elif char == ':':
                state = _InFieldKey
                text = ''
            elif char == '\n':
                yield level, 'value', ''
            else:
                state = _InValue
                text = char
        elif state == _InFieldKey:
            if char == ':':
                state = _InFieldValue
                fieldKey = text
                text = ''
            else:
                text += char
        elif state == _InFieldValue:
            if (char == '\n') or char == '}':
                yield level, 'field', fieldKey
                yield level, 'value', text
                fieldKey = None
                text = None
                if char == '}':
                    state = _BeforeStartOfBlock
                    level -= 1
                    assert level >= 0
                else:
                    state = _InLine
            else:
                text += char
        elif state == _InValue:
            if (char == '\n') or char == '}':
                yield level, 'value', text
                text = None
                if char == '}':
                    state = _BeforeStartOfBlock
                    level -= 1
                    assert level >= 0
                else:
                    state = _InLine
            else:
                text += char
        char = readable.read(1)
    if state != _BeforeStartOfBlock:
        raise Error(f'block must be closed (state={state})')
    if level != 0:
        raise Error(f'nested block must be closed (state={state}, level={level})')


def structuredItems(messageToRead):
    assert messageToRead is not None
    block = None
    field = None
    value = None
    valuesSoFar = []
    for level, kind, value in message_items(messageToRead):
        if kind == 'block':
            if block is not None:
                yield level, block, field, valuesSoFar
            block = value
            field = None
            valuesSoFar = []
        elif kind == 'field':
            if block is None:
                raise Error(f'block for field "{value}" must be specified')
            yield level, block, field, valuesSoFar
            field = value
            valuesSoFar = []
        elif kind == 'value':
            valuesSoFar.append(value)
        else:
            assert False, f'kind={kind}'
    # Yield the last item.
    if valuesSoFar:
        yield level, block, field, valuesSoFar


class Trade(object):
    """A trade in a `Report`."""
    def __init__(self):
        self.accrInterest = None
        self.ca = None
        self.ccpStatus = None
        self.clearingMember = None
        self.exchangeMember = None
        self.leg = None
        self.orderNettingType = None
        self.orderNumber = None
        self.originType = None
        self.settlementDate = None
        self.tradeDate = None
        self.tradeLocation = None
        self.tradeNumber = None
        self.tradeSettlement = None
        self.tradeType = None
        self.transactionType = None


class Report(object):
    def __init__(self, messageToRead):
        assert messageToRead is not None
        self.report = None
        for item in structuredItems(messageToRead):
            _log.debug(f'item: {item}')
            leveBlockField = item[:3]
            if self.report is None:
                if leveBlockField == (1, 4, '77E'):
                    report = self._valueFor(item, '/TRNA')
                    if self.report is None:
                        self.report = report
                        if self.report == 'RAWCE260':
                            self._initCe260()
                    else:
                        raise Error(f'cannot set report to "{report}" because it already is "{self.report}"')
            elif self.report == 'RAWCE260':
                self._processCe260(item)
            else:
                raise Error(f'cannot (yet) read reports of type "{self.report}"')

        if self.report == 'RAWCE260':
            # Add possibly remaining trade.
            self._appendPossibleTrade()
            self._trade = None
            if not self.trades:
                raise Error('report must contain at least 1 trade (starting with :94B::PRIC)')

    def _valueFor(self, item, valuePrefix, strip=True, required=True, defaultValue=None):
        assert item is not None
        assert valuePrefix
        if required:
            assert defaultValue is None

        result = None
        _, block, field, values = item
        valueIndex = 0
        valueCount = len(values)
        while (result is None) and (valueIndex < valueCount):
            value = values[valueIndex]
            if value.startswith(valuePrefix):
                result = value[len(valuePrefix):]
                if strip:
                    result = result.strip()
            else:
                valueIndex += 1
        if result is None:
            if required:
                raise Error(f'block {block}, field "{field}" must contain {valuePrefix} but found only: {values}')
            else:
                result = defaultValue
        return result

    def _slashedNameValue(self, item):
        assert item is not None
        _, block, field, values = item
        if len(values) != 1:
            raise Error(f'value in block "{block}", field "{field}" must fit into one line but is: {values}')
        # TODO: compile regex.
        finding = re.match(r'[:](?P<name>.+)//(?P<value>.*)', values[0])
        if finding is None:
            raise Error(
                f'value in block "{block}", field "{field}" '
                f'must contain text matching ":<NAME>//<VALUE>" but is: {values}'
            )
        name = finding.group('name')
        value = finding.group('value')
        return name, value

    def _dateFromIsoText(self, item, name, text):
        assert item is not None
        assert text is not None

        _, block, field, _ = item
        try:
            textAsTime = datetime.strptime(text, '%Y%m%d')
        except ValueError as error:
            message = f'cannot convert "{text}" in block "{block}", field "{field}"'
            if name is not None:
                message += f', item "{name}"'
            message += f' to date: {error}'
            raise Error(message)
        result = date(textAsTime.year, textAsTime.month, textAsTime.day)
        return result

    def _decimalFrom(self, item, name, value):
        """
        A ``decimal.Decimal`` from ``value`` properly handling all kinds of separators.

        Examples:

        * _decimalFrom(..., '1') --> 1
        * _decimalFrom(..., '123.45') --> 123.45
        * _decimalFrom(..., '123,45') --> 123.45
        * _decimalFrom(..., '123456.78') --> 123456.78
        * _decimalFrom(..., '123,456.78') --> 123456.78
        * _decimalFrom(..., '123.456,78') --> 123456.78
        """
        assert item is not None
        assert value is not None

        isGermanNumeric = False
        firstCommaIndex = value.find(',')
        if firstCommaIndex >= 0:
            firstDotIndex = value.find('.')
            if firstCommaIndex > firstDotIndex:
                isGermanNumeric = True
        if isGermanNumeric:
            unifiedValue = value.replace('.', '').replace(',', '.')
        else:
            unifiedValue = value.replace(',', '')
        try:
            result = decimal.Decimal(unifiedValue)
        except Exception as error:
            _, block, field, _ = item
            message = f'cannot convert "{value}" in block "{block}", field "{field}"'
            if name is not None:
                message += f', item "{name}"'
            message += f' to decimal: {error}'
            raise Error(message)

        return result

    def _currencyAndAmountFrom(self, item, name, value):
        """
        tuple with currency (as ISO code) and amount extracted from ``value``.

        Example: 'EUR123,45' --> ('EUR', 123.45)
        """
        assert item is not None
        assert value is not None

        def errorMessage(details):
            _, block, field, _ = item
            result = f'cannot convert "{value}" in block "{block}", field "{field}"'
            if name is not None:
                result += f', item "{name}"'
            result += f' to currency and amount: {details}'
            return result

        if len(value) < 4:
            raise Error(errorMessage('value must have at least 4 characters'))
        currency = value[:3]
        try:
            amount = self._decimalFrom(item, name, value[3:])
        except Exception as error:
            raise Error(errorMessage(error))
        return currency, amount

    def _initCe260(self):
        self.financialInstrument = None
        self.safekeepingAccount = None
        self.trades = []
        self._trade = None

    def _checkHasTrade(self, field, name=None):
        if self._trade is None:
            message = 'trade must start with 94B::PRIC before details can be specified with '
            if name is None:
                message += field
            else:
                message += field + '::' + name
            raise Error(message)

    def _appendPossibleTrade(self):
        if self._trade is not None:
            self.trades.append(self._trade)

    def _processCe260(self, item):
        def createTransactionDetailsNameToValueMap(item):
            level, block, field, values = item
            assert level == 1
            assert block == 4
            assert field == '70E'
            assert values

            result = {}
            TrDeHeader = ':TRDE//'
            if values[0].startswith(TrDeHeader):
                transactionDetails = [values[0][len(TrDeHeader):]]
                transactionDetails.extend(values[1:])
                detailsText = ' '.join(transactionDetails)
                for detail in detailsText.split('/'):
                    detail = detail.rstrip()
                    if detail != '':
                        indexOfFirstSpace = detail.find(' ')
                        if indexOfFirstSpace >= 0:
                            name = detail[:indexOfFirstSpace]
                            value = detail[indexOfFirstSpace + 1:].lstrip()
                        else:
                            name = detail
                            value = None
                        if name in result:
                            raise Error(f'duplicate transaction detail "{name}" must be removed: {transactionDetails}')
                        result[name] = value
            else:
                raise Error(f'transaction details in field "{field}" must start with "{TrDeHeader}" but are: {values}')
            return result

        level, block, field, values = item
        if (level == 1) and (block == 4):
            if field == '19A':
                name, value = self._slashedNameValue(item)
                if name == 'ACRU':
                    self._checkHasTrade(field, name)
                    self._trade.accrInterest = self._currencyAndAmountFrom(item, name, value)
                elif name == 'PSTA':
                    self._checkHasTrade(field, name)
                    self._trade.tradeSettlement = self._currencyAndAmountFrom(item, name, value)
            elif field == '20C':
                name, value = self._slashedNameValue(item)
                if name == 'TRRF':
                    self._checkHasTrade(field, name)
                    _TradeNumberIndex = 8
                    if len(value) <= _TradeNumberIndex:
                        raise Error(
                            f'trade number in {field}::{name} '
                            f'must have at least {_TradeNumberIndex + 1} characters: "{value}"'
                        )
                    self._trade.tradeNumber = value[_TradeNumberIndex:]
            elif field == '35B':
                self.financialInstrument = values
            if field == '36B':
                name, value = self._slashedNameValue(item)
                if name == 'PSTA':
                    self._checkHasTrade(field, name)
                    if value.startswith(_FamtMarker):
                        nominalText = value[len(_FamtMarker):]
                        try:
                            self._trade.nominal = self._decimalFrom(item, name, nominalText)
                        except Exception as error:
                            raise Error(error)
            elif field == '70E':
                self._checkHasTrade(field)
                transactionDetails = createTransactionDetailsNameToValueMap(item)
                self._trade.clearingMember = transactionDetails.get('CLGM')
                self._trade.exchangeMember = transactionDetails.get('EXCH')
                self._trade.leg = transactionDetails.get('LN')
                self._trade.originType = transactionDetails.get('OT')
                self._trade.transactionType = transactionDetails.get('TYPE')
                self._trade.ca = transactionDetails.get('CA')
                self._trade.ccpStatus = transactionDetails.get('CCPSTAT')
                self._trade.orderNettingType = transactionDetails.get('ORDNETT')
                self._trade.orderNumber = transactionDetails.get('ORDNB')
                self._trade.tradeType = transactionDetails.get('TTYP')
            elif field == '94B':
                name, value = self._slashedNameValue(item)
                if name == 'PRIC':
                    self._appendPossibleTrade()
                    self._trade = Trade()
                elif name == 'TRAD':
                    self._checkHasTrade(field, name)
                    ExchHeader = 'EXCH/'
                    if value.startswith(ExchHeader):
                        self._trade.tradeLocation = value[len(ExchHeader):]
            elif field == '97A':
                self.safekeepingAccount = self._valueFor(item, ':SAFE//')
            elif field == '98A':
                name, value = self._slashedNameValue(item)
                if name == 'SETT':
                    self._trade.settlementDate = self._dateFromIsoText(item, name, value)
                elif name == 'TRAD':
                    self._trade.tradeDate = self._dateFromIsoText(item, name, value)
