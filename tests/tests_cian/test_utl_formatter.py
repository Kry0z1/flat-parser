from src.url_formatters.CianFormatter import CianFormatter


def input_price(x):
    if "room" in x:
        return "1"
    return "price"


def input_date(x):
    if "room" in x:
        return "1"
    return "date"


def test_utl_formatter():
    formatter = CianFormatter()
    url = "https://www.cian.ru/"
    url_price = formatter.format(url, input=input_price)
    url_date = formatter.format(url, input=input_date)

    for url_test in (url_price, url_date):
        assert url_test.startswith("https://www.cian.ru/cat.php?")
        lst = url_test.split("?")[1]
        lst = lst.split("&")
        for item in lst:
            assert item.count("=") == 1

    assert "price_object_order" in url_price
    assert "creation-date-desc" in url_date
