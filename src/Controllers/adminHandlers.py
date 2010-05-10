'''
Created on Jul 21, 2009
@author: Kosta
'''

from google.appengine.ext import db
from Models.BaseModels import Person, Admin
from MyRequestHandler import MyRequestHandler
from lib import messages
from Controllers.baseHandlers import LoginHandler
handlerType="admin"
class UserSearchHandler(MyRequestHandler):
    def get(self):
        if(self.User and self.User.IsAdmin):
            g = self.request.get
            if(g('search')):
                query = Person.all()
                #query.filter('Name=', g('search'))
                self.respond({'result':query.fetch(limit=100)})  
                #self.response.out.write(str(query.fetch(limit=20)))
            else:
                self.respond()
        else:
            self.redirect(LoginHandler.get_url())

class SearchResultsHandler(MyRequestHandler):
    def get(self):
        if(self.User and self.User.IsAdmin):
            g = self.request.get
            
            if(g('search')):
                query = Person.all()
                query.filter('Name=', g('search'))
                persons = query.fetch(limit=100)
                self.respond({'result':persons})  
            else:
                self.respond()
        else:
            self.redirect(LoginHandler.get_url())

class AddAdminHandler(MyRequestHandler):
    def get(self):
        g = self.request.get        
        if(self.User and self.User.IsAdmin):
            if(g('UserName')):
                u = Admin(userId=g('UserName'))
                db.put(u)
                self.respond({'laStatus':'Successfuly saved the Admin ' + g('UserName')})
            else:    
                self.respond()  
        else:
            self.redirect(LoginHandler.get_url())

class ListAdminsHandler(MyRequestHandler):
    def get(self):
        self.SetTemplate(handlerType,'admin_ListUsers.html')
        if(self.User and self.User.IsAdmin):
            querry = Person.gql("WHERE IsAdmin =:v", v=True)
            result=querry.fetch(1000)
            self.respond({'result':result})
        else:
            self.status(messages.not_allowed_to_access)
            self.redirect(LoginHandler.get_url())
            

class ListUsersHandler( MyRequestHandler ):
    def get( self ):
        self.SetTemplate(handlerType, 'admin_ListUsers.html')
        if self.User and self.User.IsAdmin:
            offset = self.request.get( 'Offset' ) or 0
            result = Person.all().fetch( limit=30, offset=offset )
            self.respond( locals() )
        else:
            self.status = 'You Must be Loged in as administrator in order to list the users'
            self.redirect( LoginHandler.get_url() )
