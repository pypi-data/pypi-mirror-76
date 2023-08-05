from ..utils.functions import Functions
from ..user import User

functions = Functions()

class Groupshout:
    def __init__(self, requests, message : str, authorId : int, created : str, updated : str):
        """
        Represents a group shout
        """
        self.requests = requests
        self.message = message
        """The shout's message"""
        self.author = User(self.requests, authorId)
        """A User object for who sent the shout"""
        self.created = functions.dateconvert(created)
        """The date the shout was sent (datetime.datetime UTC)"""
        self.updated = functions.dateconvert(updated)
        """The date the shout was updated"""