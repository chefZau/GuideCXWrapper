import requests


class GuideCX:

    def __init__(self, key, host):
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

    def Note(text, userEmail, internalOnly=False):

        note = {
            'text': text,
            'userEmail': userEmail,     # if !exists, project manager's email
            'internalOnly': internalOnly
        }

        return note

    def getNote(self, noteID):

        endpoint = f'/notes/{noteID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response

    def createNoteToProject(self, projectID, text, userEmail, internalOnly=False):

        endpoint = f'/projects/{projectID}/notes'
        url = self.HOST + endpoint

        body = self.Note(text, userEmail, internalOnly)

        response = requests.post(url, json=body, headers=self.head).json()

        return response

    def getNotesFromProject(self, projectID):

        endpoint = f'/projects/{projectID}/notes'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()

        return response

    def createNoteToTask(self, taskID, text, userEmail, internalOnly=False):

        endpoint = f'/tasks/{taskID}/notes'
        url = self.HOST + endpoint

        body = self.Note(text, userEmail, internalOnly)

        response = requests.post(url, json=body, headers=self.head).json()

        return response

    def createPendingProject():