from decimal import Decimal

from lab1.data import Currencies, Currency
from lab1.parsing import XMLProvider, NBPParser


class CurrencyCalculator:
    def __init__(self):
        provider = XMLProvider('https://www.nbp.pl/kursy/xml/lasta.xml')
        parser = NBPParser(provider.get_xml_gen())

        currencies_list = [
            Currency(code, name, avg_exchange_rate, conversion_factor)
            for code, name, avg_exchange_rate, conversion_factor
            in parser.parse()
        ]
        currencies_list.append(Currency('PLN', 'złoty', Decimal(1), 1))

        self._currencies = Currencies(currencies_list)
        self._currencies_dict: {str: Currency} = self._currencies.get_currencies_dict()

    @property
    def currencies(self) -> [Currency]:
        return self._currencies.currencies

    @property
    def currencies_dict(self) -> {str: Currency}:
        return self._currencies_dict

    @staticmethod
    def convert(currency_from: Currency, currency_to: Currency, amount: Decimal) -> Decimal:
        return (currency_from.avg_exchange_rate / currency_from.conversion_factor) \
               / (currency_to.avg_exchange_rate / currency_to.conversion_factor) * amount