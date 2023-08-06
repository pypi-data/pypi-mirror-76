import json
from ..user.user import User
from ..utils.errors import HTTPError

class Message:
    def __init__(self, requests, subject=None, body=None, authorId=1, isSystem=False, isRead=False, messageId=False):
        """
        Represents a message object
        """
        self.requests = requests
        self.subject = subject
        """The subject of the message"""
        self.body = body
        """The content of the message"""
        self.authorId = authorId
        self.isread = isRead
        """Whether or not the message is marked as read"""
        self.issystem = isSystem
        """Whether or not this is a system message"""
        self.id = messageId
        """The ID of the message"""

    def author(self):
        """
        Returns a User object that represents who wrote the message
        """
        return User(self.requests, userid=self.authorId)

    def mark_read(self):
        """
        Marks a message as read
        """
        data = {
            "messageIds": [self.id]
        }
        r = self.requests.post("https://privatemessages.roblox.com/v1/messages/mark-read", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")
            

    def mark_unread(self):
        """
        Marks a message as unread
        """
        data = {
            "messageIds": [self.id]
        }
        r = self.requests.post("https://privatemessages.roblox.com/v1/messages/mark-unread", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def archive(self):
        """
        Archives the message
        """
        data = {
            "messageIds": [self.id]
        }
        r = self.requests.post("https://privatemessages.roblox.com/v1/messages/archive", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def unarchive(self):
        """
        Unarchives the message  
        This method only works for archived messages.
        """
        data = {
            "messageIds": [self.id]
        }
        r = self.requests.post("https://privatemessages.roblox.com/v1/messages/unarchive", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")