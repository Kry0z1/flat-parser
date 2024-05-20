from src.console_stuff.parsers.CianParser import CianParser
import requests


def test_parsing():
    parser = CianParser()
    flats = parser.parse(requests.get("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat"
                                      "&region=1&sort=price_object_order&type=4&room1=1").text)
    assert flats
    for flat in flats:
        assert flat.link
        assert flat.metro
        assert flat.description
        assert flat.street
        assert flat.price_info
