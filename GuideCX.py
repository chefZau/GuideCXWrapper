import requests

class GuideCX:

    def __init__(self, key, host) -> None:
        self.KEY = key
        self.HOST = host
        self.head = {
            'Authorization': 'Bearer ' + key
        }

    def getMilestone(self, milestoneID):
        
        endpoint = f'/milestones/{milestoneID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response