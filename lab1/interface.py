import decimal
import re

from decimal import Decimal

from lab1.calculator import CurrencyCalculator
from lab1.data import Currency


class UserInterface:
    def __init__(self):
        self._calculator = CurrencyCalculator()
        self._format = '{} | {:35} | {:11} | {}'

    def _print_header(self):
        print(self._format.format('Kod', 'Nazwa', 'Kurs średni', 'Przelicznik'))
        print('----+-------------------------------------+-------------+------------')

    def _print_currency(self, currency: Currency):
        print(self._format.format(
            currency.code, currency.name, currency.avg_exchange_rate, currency.conversion_factor))

    def _print_currencies(self):
        self._print_header()
        for currency in self._calculator.currencies:
            self._print_currency(currency)

    @staticmethod
    def _get_amount_from_input() -> Decimal:
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

    def _get_currency_from_input(self, input_prompt: str) -> Currency:
        currency = None

        while not currency:
            code = input(input_prompt).strip().upper()

            if not self._check_currency_code_format(code):
                print('Nieprawidłowy kod waluty')
                continue

            currency = self._calculator.currencies_dict.get(code, None)
            if not currency:
                print('Nie znaleziono takiej waluty')

        return currency

    @staticmethod
    def _check_currency_code_format(code: str) -> re.Match:
        return re.match('^[A-Z]{3}$', code)

    @staticmethod
    def _ask_exit() -> bool:
        answer = input('Kontynuować? Y/N ')
        return answer.upper() == 'N'

    def _input_loop(self):
        amount = self._get_amount_from_input()
        currency_from = self._get_currency_from_input('Przelicz z (kod waluty): ')
        currency_to = self._get_currency_from_input('Przelicz na (kod waluty): ')
        final_amount = self._calculator.convert(currency_from, currency_to, amount)

        print(f'{currency_from.code} {amount} -> {currency_to.code} {final_amount:.5f}')

    def run(self):
        self._print_currencies()
        while True:
            self._input_loop()
            if self._ask_exit():
                break