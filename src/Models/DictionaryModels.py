'''
Created on 28.12.2009

@author: KMihajlov
'''

from google.appengine.ext import db
import Models.BaseModels as bm
from datetime import datetime as dt
class Language(db.Model):
    DateCreated = db.DateTimeProperty(required=True);
    Creator = db.ReferenceProperty(bm.Person, required=True, collection_name='creator_languages')
    LanguageName = db.StringProperty(required=True)
    LanguageCode = db.StringProperty(required=True)
    
    ## Static Methods
    @classmethod
    def Get(cls, code):
        return cls.gql("WHERE LanguageCode =:c", c=code).get()
    @classmethod
    def GetAll(cls):
        return cls.all().fetch(100)
    @classmethod
    def CreateNew(cls, creator, lang_name, lang_code, _autoInsert=False):
        result = cls(
                        DateCreated=dt.now(),
                        Creator=creator,
                        LanguageName=lang_name,
                        LanguageCode=lang_code
                        )
        if _autoInsert:
            result.put()
        return result
        
class PrimaryLanguage(db.Model):
    ''' 
    Primary Language used for translation
    This language must be most complete of all
    Possibly to use some web service in order to retrieve it's items instead of storing them in datastore
    '''
    DateModified = db.DateTimeProperty(required=True)
    Language = db.ReferenceProperty(Language, required=True, collection_name='language_primary_language')
    @classmethod
    def Change(cls, new_language):
        if new_language:
            current = cls.all().get()
            if current:
                current.Language = new_language
                current.DateModified = dt.now()
            else:
                current = cls(DateModified=dt.now(), Language=new_language)
            current.put()
            return current
        else:
            raise('None returned as a parameter for the new language')
    @classmethod
    def GetCurrent(cls):
        return cls.all().get()   
class VirtualLanguageItem(db.Model):
    DateCreated = db.DateTimeProperty(required=True);
    Creator = db.ReferenceProperty(bm.Person, required=True, collection_name='creator_virtual_language_items')
    Code = db.StringProperty(required=True)
    @classmethod
    def CreateNew(cls, creator, code, _autoInsert=True):
        result = cls(
                    DateCreated=dt.now(),
                    Creator=creator,
                    Code = code
                    )
        if _autoInsert:
            result.put()
        return result
    
    @classmethod
    def Get(cls, code):
        return cls.gql("WHERE Code =:c", c=code).get()
        
class DictionaryItem(db.Model):
    DateCreated = db.DateTimeProperty(required=True);
    Creator = db.ReferenceProperty(bm.Person, collection_name='creator_dictionary_items')
    Language = db.ReferenceProperty(Language, required=True, collection_name='language_dictionary_items')
    VItem = db.ReferenceProperty(VirtualLanguageItem, required=True, collection_name='vitem_dictionary_items')
    Value = db.StringProperty(required=True)
    Description = db.StringProperty(required=True)

    ## Static methods
    @classmethod
    def GetList(cls, language, word, limit=100, offset=0):
        '''List of all words with same value but different meaning'''
        return cls.gql("WHERE Language =:l AND Value =:v", l=language, v=word).fetch(limit, offset)
    @classmethod
    def GetAllByVItemLang(cls, vItem, language, limit=5,  offset=0):
        '''Get the list of synonyms that has the meaning of the virtual item given'''
        return vItem.vitem_dictionary_items.all().filter('Language =', language).fetch(limit=limit, offset=offset)
    @classmethod
    def GetFirstByVItemLang(cls, vItem, language):
        '''Get the first word that has the meaning of the virtual item given'''
        return vItem.vitem_dictionary_items.all().filter('Language =', language).get()
    @classmethod
    def GetByVItemByLangByValue(cls, vItem, language, value):
        '''Get the first word that has the meaning of the virtual item given'''
        return vItem.vitem_dictionary_items.all().filter('Language=', language).filter('Value=', value).get()
    @classmethod
    def CreateNew(cls, creator, language, vItem, value, description, _autoInsert=False):
        if not cls.DictionaryItem.GetByVItemByLangByValue(vItem, language, value):
            result = cls(
                            DateCreated=dt.now(),
                            Creator=creator,
                            Language=language,
                            VItem=vItem,
                            Value=value,
                            Description=description
                            )
            if _autoInsert:
                result.put()
            return result
        else:
            return None
    
    #Methods
    def TranslateList(self, language, limit=10, offset=0):
        '''
        Translate the word to another language if possible
        Return the list of all synonyms.
        '''
        return DictionaryItem.gql("WHERE VItem =:v AND Language =:l", v=self.VItem, l=language).fetch(limit=limit, offset=offset)
          
