import requests as re


class HTMLGrabber:
    @staticmethod
    def getPage(url: str) -> str:
        response = re.get(url)
        if response.status_code == 200:
            return response.text
        raise ConnectionError("Unable to connect to server")
