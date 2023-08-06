from .user.user import User
from .group.group import Group
import requests

class Tools:
    def __init__(self):
        """
        This class gives you functionality to do things such as: get recommended games, search for users/groups/etc, and a bunch of other things.  
        Most of the methods here are related to using the roblox algorithm  

        WARNING: Any methods used here are sent unauthenticated, which means you can only view the information returned  
        Any data returned here can be used as if you're not logged in to roblox, for example you cannot send a trade to the user since you're not logged in
        """
        self.requests = requests.Session()

    def player_search(self, keyword):
        """
        Given a keyword it will search for players matching the keyword  
        This is an algorithmic method  

        Returns: List[User objects]
        """
        r = self.requests.get(f"https://users.roblox.com/v1/users/search?keyword={keyword}&?limit=15")
        users = []
        for user in r.json()["data"]:
            users.append(User(self.requests, user["id"]))
        return users

    def group_search(self, keyword):
        """
        Given a keyword it will search for groups matching the keyword  
        This is an algorithmic method
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/search?keyword={keyword}&?limit=15")
        groups = []
        for group in r.json()["data"]:
            group.append(Group(self.requests, group["id"], group["name"], group["description"]))
        return groups

    def limited_user_search(self, keyword):
        """
        [SP]  
        Searches for users who own limited items.  
        NOTE: This uses rolimons api and not Roblox's.  
        Methods that don't use Roblox's api are marked with [SP]
        """
        r = self.requests.get(f"https://www.rolimons.com/api/playersearch?searchstring={keyword}")
        users = []
        for user in r.json()["players"]:
            users.append(User(self.requests, user[0]))
        return users

tools = Tools()