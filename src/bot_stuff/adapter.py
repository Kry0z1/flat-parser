import io
from contextlib import redirect_stdout

import src.console_stuff.main as console


class Adapter:
    urls = dict()
    names = list()

    def __init__(self):
        self.names = console.parseUrls(self.urls)

    def show_options(self):
        return self.get_string_from_print(console.printOptions, self.names)

    def get_start_message(self):
        return "Hello, I am a bot that is designed to help you on your way to find the best place to live " \
               "for the best price!\nTo see what websites I can look through to parse all the information " \
               "and parameters to do that there are just type '/params'"

    def load(self, params):
        parser = console.getParser(params['chosen'])
        formatter = console.getFormatter(params['chosen'])
        parsed = console.getParsedData(formatter, self.urls, parser, params['chosen'], params)
        return parsed

    @staticmethod
    def get_string_from_print(command, *args):
        f = io.StringIO()
        with redirect_stdout(f):
            command(*args)
        return f.getvalue()
