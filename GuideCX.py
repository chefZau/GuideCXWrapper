

class GuideCX:

    def __init__(self, key) -> None:
        self.key = key
        self.head = {
            'Authorization': 'Bearer ' + key
        }