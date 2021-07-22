import requests


class GuideCX:
    """A Wrapper for using GuideCX API.

    Attributes:
        KEY: The API token.
        HOST: The API base URL.
        head: The header for making HTTP requests.
    """

    def __init__(self, key, host):
        """Creates an instance with three attributes: KEY, HOST, and head.

        Args:
            key (string): 
                The API token for using the API. You need to be an admin to see
                it. Go to Company Details > Integrations > Open API to find the
                token.
            host (string): 
                The base URL of the API. For instance, if you are using version.
                1.0, the base URL is `https://api.guidecx.com/api/v1`.
        """
        self.KEY = key
        self.HOST = host

        # Every API call requires a header. Instead of creating a dictionary
        # every time before the call, we embedded the header in an attribute.
        # To use it, do `self.head` and assign it to the `headers` parameter
        # when using the requests library.

        self.head = {
            'Authorization': 'Bearer ' + key
        }

    def getMilestone(self, milestoneID):
        """Retrieves an individual milestone by ID.

        Args:
            milestoneID (string): 
                The milestone ID.

        Returns:
            dict(): The JSON response of the HTTP request.
        """

        endpoint = f'/milestones/{milestoneID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response

    def getMilestonesByProject(self, projectID):
        """Retrieves all milestones from the specified project.

        Args:
            projectID (string): 
                The project ID.

        Returns:
            dict(): The JSON response of the HTTP request.
        """

        endpoint = f'/projects/{projectID}/milestones'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response

    def Note(text, userEmail, internalOnly=False):
        """Creates a Note object.

        Both the `createNoteToProject`, and `createNoteToTask` trigger the Note 
        method. The method creates the JSON body for their HTTP calls.

        Args:
            text (string): 
                The note itself.
            userEmail (string): 
                This email will be used to look up a GuideCX user to add as the
                author of the note. If the user or email doesn't exist, the 
                project manager will be used as default.
            internalOnly (bool, optional): 
                Sets the note to `Internal Only`. Defaults to False - align to 
                the GuideCX documentation.

        Returns:
            dict(): With three key-value pairs. Here is a quick example:
            ```JSON
                {
                    "text": "string",
                    "userEmail": "string",
                    "internalOnly": false
                }
            ```
        """

        note = {
            'text': text,
            'userEmail': userEmail,     # if !exists, project manager's email
            'internalOnly': internalOnly
        }

        return note

    def getNote(self, noteID):
        """Retrieves the details of a single note.

        Args:
            noteID (string): The note ID.

        Returns:
            dict(): The JSON response of the HTTP request.
        """

        endpoint = f'/notes/{noteID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()
        return response

    def createNoteToProject(self, projectID, text, userEmail, internalOnly=False):
        """Adds a new note to the specified project.

        Args:
            projectID (string): 
                The proejct ID.
            text (string): 
                The note itself.
            userEmail (string): 
                This email will be used to look up a GuideCX user to add as the
                author of the note. If the user or email doesn't exist, the 
                project manager will be used as default.
            internalOnly (bool, optional): 
                Sets the note to `Internal Only`. Defaults to False - align to 
                the GuideCX documentation.

        Returns:
            dict(): The JSON response of the HTTP request.
        """
        endpoint = f'/projects/{projectID}/notes'
        url = self.HOST + endpoint

        body = self.Note(text, userEmail, internalOnly)

        response = requests.post(url, json=body, headers=self.head).json()

        return response

    def getNotesFromProject(self, projectID):
        """Retrieves all notes from the specified project.

        Args:
            projectID (string): 
                The project ID.

        Returns:
            dict(): The JSON response of the HTTP request.
        """

        endpoint = f'/projects/{projectID}/notes'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()

        return response

    def createNoteToTask(self, taskID, text, userEmail, internalOnly=False):
        """Adds a new note to the specified task.

        Args:
            taskID ([type]): [description]
            text (string): 
                The note itself.
            userEmail (string): 
                This email will be used to look up a GuideCX user to add as the
                author of the note. If the user or email doesn't exist, the 
                project manager will be used as default.
            internalOnly (bool, optional): 
                Sets the note to `Internal Only`. Defaults to False - align to 
                the GuideCX documentation.

        Returns:
            dict(): The JSON response of the HTTP request.
        """

        endpoint = f'/tasks/{taskID}/notes'
        url = self.HOST + endpoint

        body = self.Note(text, userEmail, internalOnly)

        response = requests.post(url, json=body, headers=self.head).json()

        return response

    def createPendingProject(self):
        pass

    def getProjects(self, limit=10, offset=0, customerName=None, projectName=None, projectManagerEmail=None):
        """Retrieves a summarized list of projects from your organization.

        Args:
            limit (int, optional): 
                The max numbre of projects to return. Defaults to 10.
                Note: Maximum is 50.
            offset (int, optional): 
                The number of projects to skip. Defaults to 0.
            customerName (string, optional): 
                The name of the organization which owns the project(s) in 
                question. Defaults to None.
            projectName (string, optional): 
                THe name of the project(s) in question. Defaults to None.
            projectManagerEmail (string, optional): 
                The email of the project manager over the project(s) in 
                questions. Defaults to None.

        Returns:
            dict(): The JSON response of the HTTP request.
        """
        endpoint = f'/projects'
        url = self.HOST + endpoint

        queryStrings = {
            'limit': limit,
            'offset': offset,
        }

        if customerName:
            queryStrings['customerName'] = customerName

        if projectName:
            queryStrings['projectName'] = projectName

        if projectManagerEmail:
            queryStrings['projectManagerEmail'] = projectManagerEmail

        response = requests.get(url, headers=self.head,
                                params=queryStrings).json()
        return response


    def getProject(self, projectID):
        """Retrieves a single project with more details.

        For even more details, you can get project tasks, notes and milestones.

        Args:
            projectID (string): 
                The project ID.

        Returns:
            dict(): The JSON response of the HTTP request.
        """
        endpoint = f'/projects/{projectID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()

        return response

    
    def addCusFieldToProject(self, projectID, customFieldId, value):
        """Add a new custom field to an existing project.

        Args:
            projectID (string): 
                The project ID.
            customFieldId (string): 
                The custom field id in the organization.
            value (string): 
                The value of the new custom field.

        Returns:
            dict(): The JSON response of the HTTP request.
        """
        endpoint = f'/projects/{projectID}/custom-fields'
        url = self.HOST + endpoint

        body = {
            'customFieldId': customFieldId,
            'value': value
        }

        response = requests.post(url, headers=self.head, json=body).json()

        return response

