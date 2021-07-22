import requests
from jsonschema import validate


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

    # Milestone APIs

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

    # Notes APIs

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

    # Project APIs

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

    # Task APIs

    def getTask(self, taskID):
        """Retrieves the detail of a single task.

        Args:
            taskID (string): 
                The task ID.

        Returns:
            dict(): The JSON response of the HTTP request.
        """
        endpoint = f'/tasks/{taskID}'
        url = self.HOST + endpoint

        response = requests.get(url, headers=self.head).json()

        return response

    def getTasksByProject(self, projectID, **kwargs):

        endpoint = f'/projects/{projectID}/tasks'
        url = self.HOST + endpoint

        SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "Project Attributes",
            "description": "The schema to look for a project.",
            "type": "object",
            "properties": {
                "assigneeEmail": {
                    "description": "Assignee's email array.",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "string",
                        "pattern": "^\S+@\S+$"
                    }
                },
                "status": {
                    "description": "Task status array",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "enum": [
                            "not_started",
                            "working_on_it",
                            "stuck",
                            "sign_off",
                            "done",
                            "not_applicable",
                            "not_scheduled",
                            "scheduled"
                        ]
                    }
                },
                "projectStatus": {
                    "description": "Project status array.",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "enum": [
                            "on_hold",
                            "on_time",
                            "done",
                            "late"
                        ]
                    }
                },
                "type": {
                    "description": "Task type array.",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "enum": [
                            "regular",
                            "event",
                            "grouped"
                        ]
                    }
                },
                "responsibility": {
                    "description": "Task responsibility array.",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "enum": [
                            "internal",
                            "third_party",
                            "customer"
                        ]
                    }
                },
                "priority": {
                    "description": "Task priority array.",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high"
                        ]
                    }
                },
                "limit": {
                    "description": "The max number of tasks to return.",
                    "type": "number",
                    "minimum": 0,
                    "maximum": 50,
                    "exclusiveMaximum": True
                },
                "offset": {
                    "description": "The number of tasks to skip.",
                    "type": "number",
                    "minimum": 0,
                }
            }
        }

        try:
            validate(schema=SCHEMA, instance=kwargs)
        except:
            raise ValueError('Invalid argument(s)!')

        response = requests.get(url, params=kwargs, headers=self.head).json()

        return response

    def getTasks(self, **kwargs):
        """Retrieves a summarized list of tasks from your organization.

        Raises:
            ValueError: If the input is invalid.

        Returns:
            dict(): The JSON response of the HTTP request.
        """
        endpoint = f'/tasks'
        url = self.HOST + endpoint

        SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "Project Attributes",
            "description": "The schema to look for a project.",
            "type": "object",
            "properties": {
                "assigneeEmail": {
                    "description": "Assignee's email array.",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^\S+@\S+$"
                    }
                },
                "status": {
                    "description": "Task status array",
                    "type": "array",
                    "items": {
                        "enum": [
                            "not_started",
                            "working_on_it",
                            "stuck",
                            "sign_off",
                            "done",
                            "not_applicable",
                            "not_scheduled",
                            "scheduled"
                        ]
                    }
                },
                "projectStatus": {
                    "description": "Project status array.",
                    "type": "array",
                    "items": {
                        "enum": [
                            "on_hold",
                            "on_time",
                            "done",
                            "late"
                        ]
                    }
                },
                "type": {
                    "description": "Task type array.",
                    "type": "array",
                    "items": {
                        "enum": [
                            "regular",
                            "event",
                            "grouped"
                        ]
                    }
                },
                "responsibility": {
                    "description": "Task responsibility array.",
                    "type": "array",
                    "items": {
                        "enum": [
                            "internal",
                            "third_party",
                            "customer"
                        ]
                    }
                },
                "priority": {
                    "description": "Task priority array.",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high"
                        ]
                    }
                },
                "limit": {
                    "description": "The max number of tasks to return.",
                    "type": "number",
                    "minimum": 0,
                    "maximum": 50,
                    "exclusiveMaximum": True
                },
                "offset": {
                    "description": "The number of tasks to skip.",
                    "type": "number",
                    "minimum": 0,
                }
            }
        }

        try:
            validate(schema=SCHEMA, instance=kwargs)
        except:
            raise ValueError('Invalid argument(s)!')

        response = requests.get(url, params=kwargs, headers=self.head).json()

        return response

    def updateTask(self, taskID, **kwargs):
        """Updates task attributes.

        Args:
            taskID (string): 
                The task ID.

        Raises:
            ValueError: If the user input is invalid, raise the error.
            Check TASK_SCHEMA for the definitions.

        Returns:
            dict(): The JSON response of the HTTP request. Returns the fields
            that were updated.
        """

        endpoint = f'/tasks/{taskID}'
        url = self.HOST + endpoint

        TASK_SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "Task",
            "description": "The schema of the task.",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "description": "The name of the task.",
                    "type": "string"
                },
                "description": {
                    "description": "The description of the task.",
                    "type": "string"
                },
                "assigneeEmail": {
                    "description": "The email of the user to reassign a task. This user must already be on the project.",
                    "type": "string",
                    "pattern": "^\S+@\S+$"
                },
                "startOn": {
                    "description": "The starting time of the task.",
                    "type": "string",
                    "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
                },
                "dueOn": {
                    "description": "The end time of the task.",
                    "type": "string",
                    "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
                },
                "status": {
                    "description": "The status of the task.",
                    "enum": [
                        "not_started",
                        "working_on_it",
                        "stuck",
                        "sign_off",
                        "done",
                        "not_applicable",
                        "not_scheduled",
                        "scheduled"
                    ]
                }
            }
        }

        try:
            validate(schema=TASK_SCHEMA, instance=kwargs)
        except:
            raise ValueError('Invalid argument(s)!')

        response = requests.patch(url, json=kwargs, headers=self.head).json()

        return response

    def updateTaskStatus(self, taskID, status):
        """Updates the status of a task.

        This endpoint has a rate limit of 10 requests per minute in order to
        prevent the abuse or overload of GuideCX services.

        Args:
            taskID (string): 
                The task ID.
            status (string): 
                Please check VALID_STATUS for available status. 

        Raises:
            ValueError: If status is invalid raise the error.

        Returns:
            dict(): The JSON response of the HTTP request.
        """

        VALID_STATUS = {
            "not_started",
            "working_on_it",
            "stuck",
            "sign_off",
            "done",
            "not_applicable",
            "not_scheduled",
            "scheduled"
        }

        if status not in VALID_STATUS:
            raise ValueError('Invalid status!')

        endpoint = f'/tasks/{taskID}'
        url = self.HOST + endpoint

        body = {
            'status': status
        }

        response = requests.post(url, json=body, headers=self.head).json()

        return response

    # Custom Field APIs
