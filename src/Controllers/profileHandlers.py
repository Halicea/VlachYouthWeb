'''
Created on Oct 16, 2007

@author: Kosta
'''
from MyRequestHandler import MyRequestHandler
from Models.BaseModels import Person
import Models.ProfileModels as pm

handlerType = "profiles"
class UserProfileHandler(MyRequestHandler):
    def get(self):
        if self.User:
            userKey = self.g('key')
            if self.g('op')=='src' and self.g('searchWord'):
                self.SetTemplate(handlerType, 'SearchUsers.html')
                pass
            elif userKey:
                user = Person.get(userKey)
                if user:
                    profile = user.owner_profiles.get()
                    if not profile:
                        profile = pm.Profile.CreateNew(owner=user, userName=user.Email, _isAutoInsert=True)
                    self.respond({'profile':profile, 'profileImages': self.getImageKeys(profile)})
                    #self.response.out.write(user.Name+'<br/>'+user.Surname)
                else:
                    self.status = 'Such User does not exists'
                    self.respond()
            else:
                profile = self.User.owner_profiles.get()
                if not profile:
                    profile = pm.Profile.CreateNew(owner=self.User, userName=self.User.Email, _isAutoInsert=True)
                self.respond({'profile':profile, 'profileImages': self.getImageKeys(profile)})
        else:   
            self.status = "Must be loged in order to view someones profile"
            self.redirect('/Login')
    def getImageKeys(self, profile=None):
        result=None
        if not profile:
            if self.User:
                result = pm.ProfileImage.gql("WHERE Owner =:o",o=self.User.owner_profiles.get())
            else: 
                result = None
        else:
            result=pm.ProfileImage.gql("WHERE Owner =:o",o=profile)
        return result

class ProfileImagesHandler(MyRequestHandler):
    def post(self):
        op = self.g('op')
        dict = {}
        if op == "add":
            img = self.g("fileImg")
            img = pm.ProfileImage.CreateNew(owner=self.User.owner_profiles.get(), image=img, isDefault=False, _isAutoInsert=True)
            self.status="Image Added!"
            self.redirect(UserProfileHandler.get_url())
        if op == "show":
            if self.g('key'):
                if self.g('profileKey'):
                    self.response.headers['Content-Type'] = "image/png"
                    img = pm.ProfileImage.get(self.g('key'))
                    self.response.out.write(img.Image)
                else:
                    self.response.headers['Content-Type'] = "image/png"
                    img = pm.ProfileImage.get(self.g('key'))
                    self.response.out.write(img.Image)
            else:
                self.status = "No valid image is provided"
                self.respond()
#           self.response.out.write( post.Image )
        if op == "del":
            if self.g("key"):
                pm.ProfileImage.get(self.g("key")).delete()
                self.status = "Image deleted"
                self.respond()
                
    ### Get Method for the images
    ### Requires proper authentication
    def get(self):
        if self.User:
            if self.g('key'):
                if self.g('profileKey'):
                    self.response.headers['Content-Type'] = "image/png"
                    img = pm.ProfileImage.get(self.g('key'))
                    if self.g('mode') and self.g('mode') == 'thumb':
                        if not img.Thumbnail:
                            img.GenerateThumbnail(_isAutoInsert=True)
                        self.response.out.write(img.Thumbnail)
                    else:
                        self.response.out.write(img.Image)
                else:
                    self.response.headers['Content-Type'] = "image/png"
                    key = self.g('key')
                    img = pm.ProfileImage.get(key)
                    if self.g('mode') and self.g('mode') == 'thumb':
                        if not img.Thumbnail:
                            img.GenerateThumbnail(_isAutoInsert=True)
                        self.response.out.write(img.Thumbnail)
                    else:
                        self.response.out.write(img.Image)
            else:
                self.status = "No valid image is provided"
                self.respond()
        else:
            self.status="Must be authenticated in order to see images."
            