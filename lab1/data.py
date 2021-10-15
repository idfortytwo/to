from lab1.utils import SingletonMetaclass


class Currency:
    def __init__(self, code, title, avg_exchange_rate, conversion_factor):
        self._code = code
        self._title = title
        self._avg_exchange_rate = avg_exchange_rate
        self._conversion_factor = conversion_factor

    @property
    def code(self):
        return self._code

    @property
    def title(self):
        return self._title

    @property
    def avg_exchange_rate(self):
        return self._avg_exchange_rate

    @property
    def conversion_factor(self):
        return self._conversion_factor

    def __repr__(self):
        return f'Currency({self.code}, {self.title}, {self.avg_exchange_rate}, {self.conversion_factor})'


class Currencies(metaclass=SingletonMetaclass):
    def __init__(self, currencies):
        self._currencies = {
            currency.code: currency
            for currency
            in currencies
        }

    @property
    def currencies_dict(self):
        return self._currencies