class Role:
    def __init__(self, requests, name=None, roleId=None, rank=None, description=None):
        """
        Represents a Role object
        """
        self.requests = requests
        self.name = name
        """Name of the role"""
        self.id = roleId
        """ID of the role"""
        self.rank = rank
        """The role's rank"""
        self.description = description
        """The description of the role"""

    def get_permissions(self):
        """
        Returns the role's permissions
        """
        pass

    def delete(self):
        """
        Deletes the role
        """
        pass

    def members(self):
        """
        Returns all members who have this role
        """
        pass

    def membercount(self):
        """
        Returns the amount of members who have this role
        """
        pass