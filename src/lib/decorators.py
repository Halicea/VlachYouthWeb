'''
Created on 04.1.2010

@author: KMihajlov
'''
#from lib import messages
from lib import exceptions
from Controllers.MyRequestHandler import MyRequestHandler as mrh

class LogedInOnly(mrh):
    def __init__(self, f):
        self.f = f
    def __call__(self, f):
        if self.User:
            if self.User.IsAdmin:
                self.f()
            else:
                raise exceptions.NotValidAccess("Must be Loged In in order to view this page")
        else:
            raise exceptions.NotValidAccess("Must be Loged In order to view this page")


#class AdminOnly(mrh):
#    def __init__(self, f):
#        self.f = f
#    def __call__(self, *args):
#        if self.User:
#            if self.User.IsAdmin:
#                self.f(*args)
#            else:
#                #print str(self.f.__module__)+' '+str(self.f.__name__)+ ": Must be Administrator in order to view this page"
#                #raise exceptions.NotValidAccess("Must be Administrator in order to view this page")
#                self.redirect('/NotAuthorized')
#        else:
#            self.f(*args)
#def accountingHandler(handler):
#    handler.TemplatesDir='Views/pages/accounting'
#    return handler
#def adminHandler(handler):
#    handler.TemplatesDir='Views/pages/accounting'
#    return handler
#def staticHandler(handler):
#    handler.TemplatesDir='Views/pages/accounting'
#    return handler
#def profilesHandler(handler):
#    handler.TemplatesDir='Views/pages/accounting'
#    return handler
#def dictionaryHandler(handler):
#    handler.TemplateDir='Views/pages/accounting'
#    return handler
#def blogHandler(handler):
#    handler.TemplateDir='Views/pages/accounting'
#    return handler
