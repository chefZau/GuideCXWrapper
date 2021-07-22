import requests

class GuideCX:

    def __init__(self, key, host) -> None:
        self.KEY = key
        self.HOST = host
        self.head = {
            'Authorization': 'Bearer ' + key
        }