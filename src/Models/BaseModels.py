'''
Created on Jul 21, 2009

@author: Kosta
'''
###########
from google.appengine.ext import db
import datetime as dt
###########

class Person(db.Model):
    '''A Person with Name, Surname Phone Email e.t.c'''
    Name = db.StringProperty(required=True)
    Surname = db.StringProperty(required=True)
    Email = db.EmailProperty(required=True)
    Password = db.StringProperty(required=True)
    Public = db.BooleanProperty(default=True)
    Notify = db.BooleanProperty(default=False)
    DateAdded = db.DateTimeProperty()
    IsAdmin = db.BooleanProperty(default=False)

    def put(self):
        _isValid_, _error_ = self.__validate__()
        if(_isValid_):
            if not self.is_saved():
                self.DateAdded = dt.datetime.now()
            super(Person, self).put()
        else:
            raise Exception(_error_)

    def __validate__(self):
        __errors__ = []
        if not self.Name or len(self.Name) < 3:
            __errors__.append('Name must not be less than 3 characters')
        if not self.Surname or len(self.Surname) < 3:
            __errors__.append('Surname must not be less than 3 characters')
        if not self.Email: #or self.Email.validate('^[0-9,a-z,A-Z,.]+@[0-9,a-z,A-Z].[com, net, org]'):
            __errors__.append('Email Must Not be Empty')
        if len(self.Password) < 6  or str(self.Password).find(self.Name) >= 0:
            __errors__.append('Not a good Password(Must be at least 6 characters long, and not containing your name')

        return not __errors__ and (True, None) or (False, ' and\r\n'.join(__errors__))
    
    @classmethod
    def CreateNew(csl, name, surname, email, password, public, notify, _autoSave=False):
        result = cls(Email=email,
                    Name=name,
                    Surname=surname,
                    Password=password,
                    Public=public,
                    Notify=notify
                    )
        if _autoSave:
            result.put()
        return result
    @classmethod
    def GetUser(cls, uname, password):
        return cls.gql('WHERE Email= :email AND Password= :passwd', email=uname, passwd=password).get()
		
class Admin(Person):
    '''Admin can view all users'''
    #user = db.UserProperty()
    UserId = db.EmailProperty(required=True, default='kosta.mihajlov@gmail.com')
    IsEnabled = db.BooleanProperty(default=True)
    def __init__(self, userId='kosta.mihajlov@gmail.com'):
        if userId:
            super(Admin, self).__init__(Email=userId)
            self.UserId = userId
            self.IsEnabled = True
            self.IsAdmin = True
        else:
            exc = Exception()
            exc.message = 'No relevant UserId'
            raise exc

class WishList(db.Model):
    '''Whishes for the page look&feel and functionality '''
    Owner = db.ReferenceProperty(Person)
    Wish  = db.TextProperty()
    DateAdded = db.DateTimeProperty()
    @classmethod
    def CreateNew(cls, owner, wish, _isAutoInsert=False):
        result = cls(Owner=owner, Wish=wish, DateAdded = dt.datetime.now())
        if _isAutoInsert: result.put()
        return result
    
    @classmethod
    def GetAll(cls, limit=1000, offset=0):
        return cls.all().fetch(limit=limit, offset=offset)