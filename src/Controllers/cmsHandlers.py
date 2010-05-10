'''
Created on Jan 31, 2010

@author: KMihajlov
'''
import yaml
import Models.CMSModels as cms
from Controllers.baseHandlers import LoginHandler
from MyRequestHandler import MyRequestHandler

from google.appengine.api import memcache
from lib import messages
from Controllers.baseHandlers import LoginHandler
handlerType = "cms"
class CMSLinksHandler(MyRequestHandler):
    def get(self):
        cmsLinks = cms.CMSLink.GetLinkTree()
        contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
        self.respond({'cmsLinks':cmsLinks, 'contents':contents})
    def post(self):
        if self.User and self.User.IsAdmin:
            if self.g('op'):
                if self.g('op')=='add':
                    addressName = self.g('addressName')
                    name = self.g('name')
                    parent=self.g('parentLink')
                    if parent:
                        parent = cms.CMSLink.get(parent)
                    else: 
                        parent = None
                    order= int(self.g('order'))
                    content=self.g('content')
                    if content:
                        content = cms.CMSContent.get(content)
                    creator= self.User
                    cms.CMSLink.CreateNew(addressName, name, parent, order, content, creator, _isAutoInsert=True)
                elif self.g('op')=='del':
                    lnk=cms.CMSLink.get(self.g('key'))
                    if lnk:
                        if lnk.Content.content_cms_links.count()==1:
                            lnk.Content.delete()
                        lnk.delete()
                    else:
                        self.status="Link is invalid";
                        self.redirect(LoginHandler.get_url())
            if not self.isAjax:
                cmsLinks = cms.CMSLink.GetLinkTree()
                yaml.load()                
                contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
                self.respond({'cmsLinks':cmsLinks, 'contents':contents})
        else:
            self.status = messages.not_allowed_to_access
            self.respond('/Login')

class CMSContentHandler(MyRequestHandler):
    def get(self):
        self.SetTemplate(handlerType, 'CMSContent.html')
        if self.User and self.User.IsAdmin:
            contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
            self.respond({'contents':contents})
        else:
            self.status = messages.not_allowed_to_access
            self.redirect(LoginHandler.get_url())
            
    def post(self):
        if self.User and self.User.IsAdmin:
            if self.g('op'):
                if self.g('op')=='add':
                    title = self.g('title')
                    content = self.g('content')
                    creator=self.User
                    cms.CMSContent.CreateNew(title=title, content= content, creator=creator, _isAutoInsert=True)
                    contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
                    self.respond({'contents':contents})
                elif(True):
                    contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
                    self.respond({'contents':contents})
        else:
            self.status = messages.not_allowed_to_access
            self.redirect('/Login')

class CMSPageHandler(MyRequestHandler):
    def get(self, pagepath):
        lnk = cms.CMSLink.GetLinkByPath(pagepath)
        if lnk:
            self.respond({'link':lnk})
        else:
            self.status ="Not Valid Page"
            self.redirect(LoginHandler.get_url())
    def post(self, pagepath):
        pass