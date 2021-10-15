import decimal
import re
from decimal import Decimal

from lab1.data import Currencies, Currency
from lab1.parsing import XMLProvider, NBPParser


class CurrencyCalculator:
    def __init__(self, url):
        provider = XMLProvider(url)
        parser = NBPParser(provider.get_xml_gen())

        currencies_gen = (
            Currency(code, title, avg_exchange_rate, conversion_factor)
            for code, title, avg_exchange_rate, conversion_factor
            in parser.parse()
        )
        self._currencies_dict = Currencies(currencies_gen).currencies_dict

        self._format = '{} | {:35} | {:11} | {}'

    def _print_header(self):
        print(self._format.format('Kod', 'Nazwa', 'Kurs średni', 'Przelicznik'))
        print('----+-------------------------------------+-------------+------------')

    def _print_currency(self, currency: Currency):
        print(self._format.format(
            currency.code, currency.title, currency.avg_exchange_rate, currency.conversion_factor))

    def _show_currencies(self):
        self._print_header()
        for currency in self._currencies_dict.values():
            self._print_currency(currency)

    @staticmethod
    def _get_amount_from_input() -> int:
        amount = None

        while not amount:
            amount_str = input('Kwota: ')
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    print('Kwota ma być nieujemna')
                    amount = 0
            except decimal.InvalidOperation:
                print('Kwota ma być w formacie numerycznym')

        return amount

    def _get_currency_from_input(self, input_prompt) -> Currency:
        currency = None

        while not currency:
            code = input(input_prompt).strip().upper()

            if not self._check_currency_code_format(code):
                print('Nieprawidłowy kod waluty')
                continue

            currency = self._currencies_dict.get(code, None)
            if not currency:
                print('Nie znaleziono takiej waluty')

        return currency

    @staticmethod
    def _check_currency_code_format(code: str) -> re.Match:
        return re.match('^[A-Z]{3}$', code)

    @staticmethod
    def _convert(currency_from: Currency, currency_to: Currency, amount: int) -> int:
        return (currency_from.avg_exchange_rate / currency_from.conversion_factor) \
               / (currency_to.avg_exchange_rate / currency_to.conversion_factor) * amount

    @staticmethod
    def _ask_exit() -> bool:
        answer = input('Kontynuować? Y/N ')
        return answer.upper() == 'N'

    def _input_loop(self):
        amount = self._get_amount_from_input()
        currency_from = self._get_currency_from_input('Przelicz z (kod waluty): ')
        currency_to = self._get_currency_from_input('Przelicz na (kod waluty): ')
        final_amount = self._convert(currency_from, currency_to, amount)

        print(f'{currency_from.code} {amount} -> {currency_to.code} {final_amount:.5f}')

    def run(self):
        self._show_currencies()
        while True:
            self._input_loop()
            if self._ask_exit():
                break