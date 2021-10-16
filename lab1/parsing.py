import requests

from typing import Generator, Tuple
from decimal import Decimal
from xml.etree import ElementTree

from lab1.utils import SingletonMetaclass


class XMLProvider(metaclass=SingletonMetaclass):
    def __init__(self, url: str):
        response = requests.get(url)
        self._xml: ElementTree.Element = ElementTree.fromstring(response.content)

    @property
    def xml(self) -> ElementTree.Element:
        return self._xml

    def get_xml_gen(self) -> Generator[ElementTree.Element, None, None]:
        yield from self._xml


class NBPParser:
    def __init__(self, data_source):
        self._data_source = data_source

    def parse(self) -> Generator[Tuple[str, str, Decimal, int], None, None]:
        data_it = iter(self._data_source)
        next(data_it)
        next(data_it)

        for element in data_it:
            code = element.find('kod_waluty').text
            name = element.find('nazwa_waluty').text
            avg_exchange_rate_str = element.find('kurs_sredni').text
            avg_exchange_rate = Decimal(avg_exchange_rate_str.replace(',', '.'))
            conversion_factor = int(element.find('przelicznik').text)

            yield code, name, avg_exchange_rate, conversion_factor