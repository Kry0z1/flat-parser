from typing import List


class Processor:
    def process(self, flats: List):
        print("Found: ")
        for i, flat in enumerate(flats):
            print(f"   {i+1}) {flat.link}")
            print(f"  - Price:{flat.price}")
            print(f"       {flat.price_info}")
            print(f"  - Nearest station: {flat.metro}")
            print(f"  - Address: {flat.street}")
            print(f"  - Description: {flat.description}\n\n\n")
