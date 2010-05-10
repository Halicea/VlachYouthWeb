'''
Created on 17.1.2010

@author: KMihajlov
'''
class NotValidAccess(Exception):
    def __init__(self, value=""):
        self.value=value
    def __str__(self):
        return self.value or "You don't have access to View this resource";
            