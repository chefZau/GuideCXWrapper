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

    def getMilestonesByProject(self, projectID):

        endpoint = f'/projects/{projectID}/milestones'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response

    def getNote(self, noteID):

        endpoint = f'/notes/{noteID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response

    def createNoteToProject(self, projectID, text, userEmail, internalOnly=False):
        
        endpoint = f'/projects/{projectID}/notes'
        url = self.HOST + endpoint

        body = {
            'text': text,
            'userEmail': userEmail,     # if !exists, project manager's email
            'internalOnly': internalOnly
        }

        response = requests.post(url, json=body, headers=self.head).json()

        return response