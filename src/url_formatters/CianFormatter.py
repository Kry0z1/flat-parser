from src.url_formatters.formatter import Formatter


class CianFormatter(Formatter):
    def format(self, url: str) -> str:
        room_numbers = map(int, input("Input room count(in a single line like: 1 2 3): ").split())
        sort_type = input("Input sort(by price or by date): ")
        sort_type = "price_object_order" if "price" in sort_type.lower() else "creation-date-desc"
        rooms = "".join(f"&room{i}=1" for i in room_numbers)
        return (f"https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=1" +
                rooms +
                f"&sort={sort_type}&type=4")
