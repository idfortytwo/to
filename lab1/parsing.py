from decimal import Decimal
from xml.etree import ElementTree

import requests

from lab1.utils import SingletonMetaclass
from lab1.data import Currency


class XMLProvider(metaclass=SingletonMetaclass):
    def __init__(self, url):
        self._response = requests.get(url)

    def get_xml(self):
        xml = ElementTree.fromstring(self._response.content)
        yield from xml


class NBPParser:
    def __init__(self, data_source):
        self._data_source = data_source

    def parse(self):
        data_it = iter(self._data_source)
        next(data_it)
        next(data_it)

        for element in data_it:
            code = element.find('kod_waluty').text
            title = element.find('nazwa_waluty').text
            avg_exchange_rate_str = element.find('kurs_sredni').text
            avg_exchange_rate = Decimal(avg_exchange_rate_str.replace(',', '.'))
            conversion_factor = int(element.find('przelicznik').text)

            yield Currency(code, title, avg_exchange_rate, conversion_factor)