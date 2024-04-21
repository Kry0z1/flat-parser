from typing import Dict, List

from src.grabber import HTMLGrabber
from src.processor import Processor


def parseUrls(urls: Dict[str, str]) -> List:
    names = []
    with open('urls.txt', 'r') as f:
        for line in f:
            url, shortName = line.split()
            urls[shortName] = url
            names.append(shortName)
    return names


def printOptions(names: List[str]) -> None:
    if len(names) == 0:
        raise KeyError('No URLs found')
    print("Options found: ")
    for (i, shortName) in enumerate(names):
        print(f"{i + 1}) {shortName}")


def getInput(names: List[str]) -> str:
    if len(names) == 1:
        return names[0]
    while True:
        id = input(f"What site would you like to parse?(number in [1-{len(names)}])\n")
        if not id.isnumeric():
            print("Please enter a number")
        elif int(id) < 1 or int(id) > len(names):
            print(f"Please enter a number between 1 and {len(names)}")
        else:
            return names[int(id) - 1]


def main():
    urls = dict()

    names = parseUrls(urls)
    printOptions(names)

    name = getInput(names)
    print(f"So you chose {name}")

    exec(f"from src.parsers.{name}Parser import {name}Parser")
    parser = locals()[f"{name}Parser"]()

    exec(f"from src.url_formatters.{name}Formatter import {name}Formatter")
    formatter = locals()[f"{name}Formatter"]()

    processor = Processor()

    page = HTMLGrabber.getPage(formatter.format(urls[name]))
    parsedData = parser.parse(page)

    flats = processor.process(parsedData)


if __name__ == '__main__':
    main()
