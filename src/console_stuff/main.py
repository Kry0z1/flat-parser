from typing import Dict, List

from src.console_stuff.grabber import HTMLGrabber
from src.console_stuff.processor import Processor
from src.console_stuff.parsers.parser import Parser
from src.console_stuff.url_formatters.formatter import Formatter


def parseUrls(urls: Dict[str, str]) -> List:
    names = []
    with open('src/urls.txt', 'r') as f:
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


def getUrlsAndUsersChoiceOnUrl():
    urls = dict()

    names = parseUrls(urls)
    printOptions(names)

    name = getInput(names)

    return urls, name


def getParser(name: str):
    exec(f"from src.console_stuff.parsers.{name}Parser import {name}Parser")
    parser = locals()[f"{name}Parser"]()
    return parser


def getFormatter(name: str):
    exec(f"from src.console_stuff.url_formatters.{name}Formatter import {name}Formatter")
    formatter = locals()[f"{name}Formatter"]()
    return formatter


def getProcessor():
    return Processor()


def getParsedData(formatter: Formatter, urls: dict, parser: Parser, name: str, params: dict[str, any] = None):
    page = HTMLGrabber.getPage(formatter.format(urls[name], params))
    parsedData = parser.parse(page)
    return parsedData


def main():
    urls, name = getUrlsAndUsersChoiceOnUrl()
    parser = getParser(name)
    formatter = getFormatter(name)
    processor = getProcessor()
    parsedData = getParsedData(formatter, urls, parser, name)
    processor.process(parsedData)


if __name__ == '__main__':
    main()
