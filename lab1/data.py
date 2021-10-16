from decimal import Decimal


class Currency:
    def __init__(self, code: str, title: str, avg_exchange_rate: Decimal, conversion_factor: int):
        self._code: str = code
        self._title: str = title
        self._avg_exchange_rate: Decimal = avg_exchange_rate
        self._conversion_factor: int = conversion_factor

    @property
    def code(self) -> str:
        return self._code

    @property
    def title(self) -> str:
        return self._title

    @property
    def avg_exchange_rate(self) -> Decimal:
        return self._avg_exchange_rate

    @property
    def conversion_factor(self) -> int:
        return self._conversion_factor

    def __repr__(self) -> str:
        return f'Currency({self.code}, {self.title}, {self.avg_exchange_rate}, {self.conversion_factor})'


class Currencies:
    def __init__(self, currencies: [Currency]):
        self._currencies = currencies

    @property
    def currencies(self) -> [Currency]:
        return self._currencies

    @property
    def currencies_dict(self) -> {str: Currency}:
        return {
            currency.code: currency
            for currency
            in self._currencies
        }