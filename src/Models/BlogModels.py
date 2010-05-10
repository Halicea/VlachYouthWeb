'''
Created on 08.1.2010

@author: KMihajlov
'''
###########
from google.appengine.ext import db
import datetime as dt
from ProfileModels import Person
###########

class Post(db.Model):
    ''' A simple Post Class'''
    Title = db.StringProperty(required=True)
    Entry = db.TextProperty(required=True)
    Creator = db.ReferenceProperty(Person , required=True, collection_name='creator_posts')
    DateCreated = db.DateTimeProperty(required=True)
    DateModified = db.DateTimeProperty(required=True)
    TimesRead = db.IntegerProperty(default=0)
    IsArchive = db.BooleanProperty(default=False)
    #Reference items of the post
    def get_Comments(self, limit=100, offset=0):
        return self.reference_post_comments.fetch(limit=limit, offset=offset)
    Comments = property(get_Comments, None)
    
    @classmethod
    def GetLastPosts(cls, days_old=0, fetch_limit=7):
        if(not isinstance(days_old, int)):
            raise Exception('days_old parameter must be int')
        if(not isinstance(fetch_limit, int)):
            raise Exception('fetch_limit parameter must be int')
        return cls.all().order('-DateCreated').fetch(fetch_limit)
   
    @classmethod
    def CreateNew(cls, title, entry, creator, _autoInsert=False):
        result = cls(Title=title, Entry=entry, Creator=creator, DateCreated=dt.datetime.now(), DateModified=dt.datetime.now())
        if _autoInsert:
            result.put()
        return result     

class ShortPost(db.Model):
    '''Short description of a post, a new page is needed for this one'''
    Title = db.StringProperty(required=True)
    Entry = db.TextProperty(required=True)
    Creator = db.ReferenceProperty(Person , required=True, collection_name='creator_short_posts')
    DateCreated = db.DateTimeProperty(required=True)
    DateModified = db.DateTimeProperty(required=True)
    ReferencePost = db.ReferenceProperty(Post, collection_name='reference_post_short_posts')
    
    @classmethod
    def CreateNew(cls, title, entry, creator, referencePost, _autoInsert=False):
        result = cls(Title=title, Entry=entry, Creator=creator, ReferencePost=referencePost , DateCreated=dt.datetime.now(), DateModified=dt.datetime.now())
        if _autoInsert:
            result.put()
        return result

class Comment(db.Model):
    '''A class  used for storring comments of someones Post'''
    ReferencePost = db.ReferenceProperty(Post, required=True, collection_name='reference_post_comments')
    Entry = db.TextProperty(required=True)
    Creator = db.ReferenceProperty(Person, collection_name='creator_comments')
    DateCreated = db.DateTimeProperty(required=True)
    IsShow = db.BooleanProperty()
    @classmethod
    def CreateNew(cls, referencePost, entry, creator, isShow, _isAutoInsert=False):
        result = cls(ReferencePost=referencePost, Entry=entry, creator=creator, IsShow=isShow, DateCreated=dt.datetime.now())
        if _isAutoInsert:
            result.put()
        return result

class Reply(db.Model):
    '''Class used for storing replies on comments'''
    Entry = db.TextProperty(required=True)
    Creator = db.ReferenceProperty(Person, collection_name='creator_replies')
    ReferenceComment = db.ReferenceProperty(Comment, collection_name='reference_comment_replies')
    DateCreated = db.DateTimeProperty()
    IsShow = db.BooleanProperty(default=True)

class Quote(db.Model):
    ''' Class for saving quotes  that are displayed'''
    QuoteText = db.TextProperty(required=True)
    Author = db.ReferenceProperty(Person, required=True, collection_name='author_quotes')
    CreatedOn = db.DateProperty(required=True)
    PublishDate = db.DateProperty(required=True)

    def put(self):
        if not self.is_saved():
            self.CreatedOn = dt.date.today()
        if self.validate():
            return self.put()
        else:
            raise Exception('The Data for the Quote is not valid or the User has no right ot save it')

    def validate(self):
        if self.Author.IsAdmin and len(self.QuoteText) > 20:
            return True
        else:
            return False
