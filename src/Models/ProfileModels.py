'''
Created on Aug 5, 2009

@author: kosta mihajlov
'''
from google.appengine.ext import db
from Models.BaseModels import Person
from datetime import datetime as dt
from google.appengine.api import images
class Profile(db.Model):
    UserName = db.StringProperty()
    Owner = db.ReferenceProperty(Person, required=True, collection_name='owner_profiles') 
    AboutMe = db.TextProperty()
    Interests = db.StringListProperty()
    Hobies = db.StringListProperty()
    TopFriends = db.StringListProperty()
    DateCreated = db.DateTimeProperty()
    DateModified = db.DateTimeProperty()
    IsGroup = db.BooleanProperty()
    #methods
    def get_Friends(self, limit=100, offset=0):
        return [f.Friend  for f in self.owner_friendships.fetch(limit=limit, offset=offset)]
    def get_Requests(self, limit=100, offset=0):
        return self.owner_friendship_requests.fetch(limit=limit, offset=offset)
    def get_Images(self, limit=100, offset=0):
        return ProfileImage.GetAllForProfile(self, limit=limit, offset=offset)
    def get_Messages(self, limit=100, offset=0):
        return self.to_messages.fetch(limit=limit, offset=offset)
    def get_Tags(self, limit=100, offset=0):
        return self.owner_person_image_tags.fetch(limit=limit, offset=offset)
    ##end Methods
        
    ###Static Methods
    @classmethod 
    def CreateNew(cls, owner, userName, aboutMe='', interests=[], hobies=[], topFirends=[], isGroup=False, _isAutoInsert=False):
        result = cls(
                    UserName=userName,
                    Owner=owner,
                    AboutMe=aboutMe,
                    Interests=interests,
                    Hobies=hobies,
                    TopFriends=topFirends,
                    DateCreated=dt.now(),
                    DateModified=dt.now(),
                    IsGroup=isGroup,
                   )
        if _isAutoInsert:
            result.put()
        return result
    
    @classmethod
    def GetByUserName(cls, userName):
        result = cls.gql("WHERE UserName =:u", u=userName).get()
        return result
    
    @classmethod
    def GetByOwner(cls, owner):    
        result = cls.gql("WHERE Owner =:o", o=owner).get()
        return result
    ##end Static Methods
class ProfileAlbum(db.Model):
    Owner = db.ReferenceProperty(Profile, required=True, collection_name='owner_profile_albums')
    CoverImageKey = db.StringProperty()
    Name = db.StringProperty(required=True)
    DateCreated = db.DateTimeProperty() 

class ProfileImage(db.Model):
    Owner = db.ReferenceProperty(Profile, required=True, collection_name='owner_profile_images')
    Album = db.ReferenceProperty(ProfileAlbum, collection_name='album_profile_images')
    Image = db.BlobProperty(required=True)
    Thumbnail = db.BlobProperty()
    DateAdded = db.DateTimeProperty(required=True)
    IsDefault = db.BooleanProperty(required=True)
    def get_Comments(self, limit=100, offset=0):
        return self.image_image_comments.fetch(limit=limit, offset=offset)
    
    def GenerateThumbnail(self, _isAutoInsert=False):
        '''If thumbnail is null this method automatically will generate it.'''
        img = images.Image(self.Image)
        img.resize(width=80, height=100)
        img.im_feeling_lucky()
        self.Thumbnail = img.execute_transforms(output_encoding=images.JPEG)
        if _isAutoInsert:
            self.put()
        return self.Thumbnail
        
    @classmethod
    def CreateNew(cls, owner, image, album=None, isDefault=False, _isAutoInsert=False):
        img = images.Image(image).resize(width=80, heigth=100).im_feeling_lucky()
        thumbnail = img.execute_transforms(output_encoding=images.JPEG)
        result = cls(Owner=owner, Image=image, Thumbnail=thumbnail, Album = album, IsDefault=isDefault, DateAdded=dt.now())
        if _isAutoInsert:
            result.put()
        return result  
    @classmethod
    def GetAllForProfile(cls, profile, limit=100, offset=0):
        return profile.owner_person_images.fetch(limit=limit, offset=offset)   

class ProfileImageTag(db.Model):
    TagedBy = db.ReferenceProperty(Profile, required=True, collection_name='taged_by_profile_image_tags')
    Owner = db.ReferenceProperty(Profile, required=True, collection_name='owner_profile_image_tags')
    TagedImage = db.ReferenceProperty(ProfileImage, required=True, collection_name='taged_image_profile_image_tags')
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    @classmethod
    def CreateNew(cls, tagedBy , owner, tag, x=0, y=0, _isAutoInsert=False):
        result = cls(TagedBy=tagedBy, Owner=owner, Tag=tag, x=x, y=y)
        if _isAutoInsert:
            result.put()
        return result
    
class ProfileImageComment(db.Model):
    From = db.ReferenceProperty(Profile, required=True, collection_name='from_profile_image_comments')
    Image = db.ReferenceProperty(ProfileImage, required=True, collection_name='image_profile_image_comments')
    Message = db.TextProperty(required=True)
    
    ## Static Methods
    @classmethod
    def CreateNew(cls, fromProfile, image, message, _isAutoInsert=False):
        result = cls(From=fromProfile, Image=image, Message=message)
        if _isAutoInsert:
            result.put()
        return result
    
class Friendship(db.Model):
    Owner = db.ReferenceProperty(Profile, indexed=True, collection_name='owner_friendships')
    Friend = db.ReferenceProperty(Profile, indexed=True, collection_name='friend_friendships')
    DateCreated = db.DateProperty(required=True)
    
    @classmethod
    def CreateNew(cls, owner, friend, _isAutoInsert=False):
        # @type friend: Profile
        # @type owner: Profile 
        result = cls(Owner=owner, Friend=friend, DateCreated=dt.now())
        if _isAutoInsert:
            result.put()
        return result
            
class FriendshipRequest(db.Model):
    Owner = db.ReferenceProperty(Profile, indexed=True, required=True, collection_name='owner_friendship_requests')
    Requestor = db.ReferenceProperty(Profile, indexed=True, required=True, collection_name='requestor_friendship_requests')
    Message = db.TextProperty()
    DateCreated = db.DateProperty(required=True)
    ## Methods
    def Accept(self):
        Friendship.CreateNew(self.Owner, self.Requestor, _isAutoInsert=True)
        Friendship.CreateNew(self.Requestor, self.Owner, _isAutoInsert=True)
        self.delete()
    def Reject(self):
        self.delete()
    ## end Methods
    
    ## Static Methods    
    @classmethod
    def CreateNew(cls, owner, requestor, message, _isAutoInsert=False):
        result = cls(Owner=owner, Requestor=requestor, Message=message, DateCreated=dt.now())
        if _isAutoInsert:
            result.put()
        return result
    ###end Static Methods

class Message(db.Model):
    From = db.ReferenceProperty(Profile , required=True, collection_name='from_messages')
    To = db.ReferenceProperty(Profile, required=True, collection_name='to_messages')
    Subject = db.StringProperty()
    Message = db.TextProperty(required=True)
    DateSent = db.DateTimeProperty(required=True)
    IsRead = db.BooleanProperty()
    
    @classmethod
    def CreateNew(cls, fromProfile, toProfile, subject, message, isRead=False, _isAutoInsert=False):
        result = cls(From=fromProfile, To=toProfile, Subject=subject, Message=message, IsRead=isRead)
        if _isAutoInsert:
            result.put()
        return result

    
