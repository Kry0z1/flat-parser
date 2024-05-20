from src.console_stuff.parsers.parser import Parser
from src.console_stuff.flat import Flat
from typing import List
from bs4 import BeautifulSoup


class CianParser(Parser):
    def __init__(self):
        pass

    def parse(self, page: str) -> List:
        soup = BeautifulSoup(page, 'html.parser')
        flats = list(soup.find_all(attrs={'data-name': 'LinkArea'}))
        result = []
        for flat in flats:
            try:
                link = flat.a.attrs['href']
                price = flat.find(attrs={'data-mark': 'MainPrice'}).span.text
                price_info = flat.find(attrs={'data-mark': 'MainPrice'}).parent.next_sibling.p.text
                metro = flat.find(attrs={'data-name': 'SpecialGeo'}).a.find('div').next_sibling.text
                street = "".join(i.text for i in flat.find(attrs={'data-name': 'SpecialGeo'}).next_sibling.children)
                desc = flat.find(attrs={'data-name': 'Description'}).p.text
                result.append(Flat(link, price, metro, desc, price_info, street))
            except AttributeError:
                pass
        return result
