# pyroblox
[![Downloads](https://pepy.tech/badge/pyroblox-viown)](https://pepy.tech/project/pyroblox-viown)

An API Wrapper for ROBLOX.  
As of right now this library lacks some features and will experience breaking changes frequently. If your code breaks after updating, re-read the documentation to keep it up to date.

This library is still incomplete and maturing, if you experience any problems or minor bugs please open an issue.
***
# Docs
You can find the latest documentation here:
https://viown.github.io/pyroblox/
***
# Guide
This library has a basic guide that explains how to use this library:  [Guide](https://docs.google.com/document/d/15IgirmZIYKGinPy5abXBY3G0_r6mb2o9k_lrW63F-iY/edit?usp=sharing)

***
# Installation

Stable installation (Recommended):  
```pip install pyroblox-viown --upgrade```

Latest installation:  
```pip install git+https://github.com/viown/pyroblox.git```
***
# Examples

```py
# Getting a user
import pyroblox

client = pyroblox.Login(cookie=".ROBLOSECURITY here")

user = client.account.get_user(username="ROBLOX") # Get the user by name/id
print(user.id) # Print the users ID.
```  
```py
# Getting a group
import pyroblox

client = pyroblox.Login(cookie=".ROBLOSECURITY here") # Logs in to the roblox account through .ROBLOSECURITY

group = client.account.get_group(id=26) # Gets the group with id 26
print(group.name) # Prints the groups name
```

You can find a long list of examples in pyroblox/examples, but you should read the documentation to see everything you can do with pyroblox.
***
# Coming Soon
This lists features that will definitely be coming soon to pyroblox

- Full interaction with the Group API (85% complete)
- Support for bulk operations
- More methods for classes
- Better usability
- Interaction with more roblox apis (Catalog, Library, Chat, etc)
- Improvements to methods, classes, etc
- Cursor paging
- And a lot more
***
# Contact

You can contact me on discord ```vi#0049``` for help with the library
