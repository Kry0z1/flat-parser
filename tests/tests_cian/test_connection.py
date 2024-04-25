import requests


def test_connection():
    url = "https://www.cian.ru/"
    assert requests.get(url).status_code == 200
