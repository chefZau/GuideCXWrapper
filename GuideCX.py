

class GuideCX:

    def __init__(self, key, host) -> None:
        self.key = key
        self.HOST = host
        self.head = {
            'Authorization': 'Bearer ' + key
        }