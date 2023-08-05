import json

from ..utils.errors import PermissionError, HTTPError, InvalidValue, InvalidParameters
from ..game import Game

from .joinrequest import JoinRequest
from .wallpost import Wallpost
from .member import Member
from .role import Role
from .groupshout import Groupshout


class Group:
    def __init__(self, requests, groupId=None, name=None, description=None):
        """
        Represents a group object  
        As of right now this class is not complete.
        """
        self.requests = requests
        self.id = groupId
        """The ID of the group"""
        self.name = name
        """The name of the group"""
        self.description = description
        """The description of the group"""

    def get_member(self, id=None, username=None):
        """
        Gets the member either by id or username, returns None if the user isn't in the group  

        Parameters: id[int], username[string] | You only need to specify one
        """
        if id:
            r = self.requests.get(f"https://groups.roblox.com/v2/users/{str(id)}/groups/roles")
            if r.status_code == 200:
                for group in r.json()["data"]:
                    if group["group"]["id"] == self.id:
                        info = self.requests.get(f"https://api.roblox.com/users/{str(id)}").json()
                        return Member(self.requests, info["Id"], info["Username"], group["role"]["id"], group["role"]["name"], group["role"]["rank"])
                return None
            else:
                raise HTTPError(f"Request failed with status code {r.status_code}")
        elif username:
            info = self.requests.get(f"https://api.roblox.com/users/get-by-username?username={username}").json()
            r = self.requests.get(f"https://groups.roblox.com/v2/users/{info['Id']}/groups/roles")
            if r.status_code == 200:
                for group in r.json()["data"]:
                    if group["group"]["id"] == self.id:
                        return Member(self.requests, info["Id"], info["Username"], group["role"]["id"], group["role"]["name"], group["role"]["rank"])
                return None
            else:
                raise HTTPError(f"Request failed with status code {r.status_code}")

    def get_role(self, name=None, rank=None):
        """
        Gets the role either by name (case-sensitive) or rank, returns None if the role doesn't exist  

        Parameters: name[string], rank[int] | You only need to specify one
        """
        if name:
            r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/roles")
            for role in r.json()["roles"]:
                if role["name"] == name:
                    return Role(self.requests, role["name"], role["id"], role["rank"], role["description"])
            return None
        elif rank:
            r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/roles")
            for role in r.json()["roles"]:
                if role["rank"] == rank:
                    return Role(self.requests, role["name"], role["id"], role["rank"], role["description"])
        else:
            raise InvalidParameters("Name or rank not specified")



    def joinrequests(self):
        """
        Gets a list of join requests in the group  
        Returns a list of JoinRequest objects  

        The `Accept Join Requests` permission is required for this action
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/join-requests")
        if r.status_code == 200:
            requests = []
            for joinrequest in r.json()["data"]:
                requests.append(JoinRequest(self.requests, joinrequest["requester"]["userId"], joinrequest["requester"]["username"], joinrequest["created"]))
            return requests
        elif r.status_code == 403 or r.status_code == 400:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def games(self):
        """
        Returns a list of games the group has created
        """
        r = self.requests.get(f"https://games.roblox.com/v2/groups/{str(self.id)}/games")
        gameslist = []
        for game in r.json()["data"]:
            gameslist.append(Game(self.requests, game["id"]))
        return gameslist


    def members(self):
        """
        Returns a list of members in the group  

        Returns a list of Member objects
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/users")
        userslist = []
        for user in r.json()["data"]:
            userslist.append(Member(self.requests, user["user"]["userId"], user["user"]["username"], user["role"]["id"], user["role"]["name"], user["role"]["rank"]))
        return userslist

    def wall(self):
        """
        Returns the last 50 messages posted on the group wall  
        Returns a list of Wallpost objects  

        The `View Group Wall` permission is required for this action
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/wall/posts?limit=50")
        wallposts = []
        for post in r.json()["data"]:
            wallposts.append(Wallpost(self.requests, Group, post["body"], self.id, post["id"], post["poster"]["username"], post["poster"]["userId"], post["created"], post["updated"]))
        return wallposts

    def set_role_by_rank(self, member, rank=None):
        """
        Sets the member's role by the rank  
        
        Parameters: member[Member object], rank[int]  

        The `Manage lower-ranked member ranks` permission is required for this action
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/roles")
        for role in r.json()["roles"]:
            if role["rank"] == rank:
                data = {
                    "roleId": role["id"]
                }
                r = self.requests.patch(f"https://groups.roblox.com/v1/groups/{str(self.id)}/users/{str(member.user.id)}", data=json.dumps(data))
                if r.status_code == 200:
                    return True
                elif r.status_code == 403 or r.status_code == 400:
                    raise PermissionError("You do not have the appropriate permissions for this action")
                else:
                    raise HTTPError(f"Request failed with status code {r.status_code}")
        raise InvalidValue("There is no role with that rank")
        

    def set_role(self, member, rolename=None):
        """
        Sets the member's role by the role's name  
        
        Parameters: member[Member object], rolename[string]  

        The `Manage lower-ranked member ranks` permission is required for this action
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/roles")
        for role in r.json()["roles"]:
            if role["name"] == rolename:
                data = {
                    "roleId": role["id"]
                }
                r = self.requests.patch(f"https://groups.roblox.com/v1/groups/{str(self.id)}/users/{str(member.user.id)}", data=json.dumps(data))
                if r.status_code == 200:
                    return True
                elif r.status_code == 403 or r.status_code == 400:
                    raise PermissionError("You do not have the appropriate permissions for this action")
                else:
                    raise HTTPError(f"Request failed with status code {r.status_code}")
        raise InvalidValue("There is no role with that name")

    def funds(self):
        """
        Returns the amount of funds in the group  

        The group funds have to be public or you have access to them otherwise this raises a PermissionError
        """
        r = self.requests.get(f"https://economy.roblox.com/v1/groups/{str(self.id)}/currency")
        if r.status_code == 200:
            return r.json()["robux"]
        elif r.status_code == 403 or r.status_code == 400:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def allies(self):
        """
        Returns a list of allies the group has  

        Returns a list of Group objects
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/relationships/allies?maxRows=50&sortOrder=Asc&startRowIndex=0")
        if r.status_code == 200:
            groups = []
            for group in r.json()["relatedGroups"]:
                groups.append(Group(self.requests, group["id"]))
            return groups
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def enemies(self):
        """
        Returns a list of enemies the group has  

        Returns a list of Group objects
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/relationships/enemies?maxRows=50&sortOrder=Asc&startRowIndex=0")
        if r.status_code == 200:
            groups = []
            for group in r.json()["relatedGroups"]:
                groups.append(Group(self.requests, group["id"]))
            return groups
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")



    def auditlog(self):
        pass

    def shout(self, message):
        """
        Sets/updates the groups shout message  

        Parameters: message[string] | The message to shout

        The `Post group shout` permission is required for this action  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        data = {
            "message": message
        }
        r = self.requests.patch(f"https://groups.roblox.com/v1/groups/{str(self.id)}/status", data=json.dumps(data))
        if r.status_code == 200:
            return True
        elif r.status_code == 403 or r.status_code == 400:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def get_shout(self):
        """
        Returns a Groupshout object representing the current shout message
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}")
        if r.status_code == 200:
            data = r.json()
            return Groupshout(self.requests, data["shout"]["body"], data["shout"]["poster"]["userId"], data["shout"]["created"], data["shout"]["updated"])
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def roles(self):
        """
        Returns a list of roles the group has
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/roles")
        if r.status_code == 200:
            roleslist = []
            for role in r.json()["roles"]:
                roleslist.append(Role(self.requests, role["name"], role["id"], role["rank"], role["description"]))
            return roleslist
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")

    def creator(self):
        """
        Returns a Member object of who owns the group
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}")
        if r.status_code == 200:
            data = r.json()
            roles = self.requests.get(f"https://groups.roblox.com/v2/users/{data['owner']['userId']}/groups/roles").json()["data"]
            roledata = {}
            for item in roles:
                if item["group"]["id"] == self.id:
                    roledata["roleId"] = item["role"]["id"]
                    roledata["roleName"] = item["role"]["name"]
                    roledata["rank"] = item["role"]["rank"]
                    break
            return Member(self.requests, data["owner"]["userId"], data["owner"]["username"], roledata["roleId"], roledata["roleName"], roledata["rank"])
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")

    def payout(self, member, amount=None):
        """
        Sends a group payout to the specified user  

        Parameters: member[Member object], amount[int]

        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def exile(self, member):
        """
        Exiles a user from the group  

        Parameters: member[Member object]  

        The `Kick lower-ranked members` permission is required for this action
        """
        r = self.requests.delete(f"https://groups.roblox.com/v1/groups/{str(self.id)}/users/{str(member.id)}")
        if r.status_code == 200:
            return True
        elif r.status_code == 403 or r.status_code == 400:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def post(self, message : str):
        """
        Posts a message on the group's wall  

        Parameters: message[string]  
        Returns: A Wallpost Object
        """
        data = {
            "body": message
        }
        r = self.requests.post(f"https://groups.roblox.com/v2/groups/7302938/wall/posts", data=json.dumps(data))
        print(r.text)
        if r.status_code == 200:
            data = r.json()
            return Wallpost(self.requests, Group, data["body"], self.id, data["id"], data["poster"]["username"], data["poster"]["userId"], data["created"], data["updated"])
        elif r.status_code == 403 or r.status_code == 400:
            raise PermissionError("You do not have the appropriate permissions for this action or Captcha may have been requested")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")

    def claim_ownership(self):
        """
        Claims ownership of the group  

        This will only work if the group is unowned  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass