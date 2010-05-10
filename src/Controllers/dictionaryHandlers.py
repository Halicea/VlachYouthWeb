'''
Created on 28.12.2009

@author: KMihajlov
'''
import Models.DictionaryModels as dm
from MyRequestHandler import MyRequestHandler
from Controllers.baseHandlers import LoginHandler

handlerType="dictionary"
class TranslateHandler(MyRequestHandler):
    def get(self):
        respondDict = {}
        if not self.isAjax:
            respondDict.update(self.getStaticData() or {})
            respondDict.update(self.ajaxSearchResults() or {})
        else:
            self.SetTemplate(handlerType, 'dict_Translate.inc.html')
            respondDict.update(self.ajaxSearchResults() or {})
            
        self.respond(respondDict)
            
    def getStaticData(self):
        languages = dm.Language.GetAll()
        if languages: return {"languages":languages}
        else: return None
    
    def ajaxSearchResults(self):
        fromL, toL, searchItem = self.g('fromL'), self.g('toL'), self.g('searchItem') 
        fromL, toL = dm.Language.Get(fromL), dm.Language.Get(toL)
        if fromL and toL:
            fromResults = dm.DictionaryItem.GetList(fromL, searchItem)
            translation = [[w.Description, w.TranslateList(toL)] for w in fromResults]
            return {'DictionaryItemResults' : translation}
        else:
            return None

class WordHandler(MyRequestHandler):
    def get(self, language, word):
        if self.isAjax:  
            self.SetTemplate(handlerType, "dict_Word.inc.html")
        l = dm.Language.Get(language)
        responseDict= {'wordResults': dm.DictionaryItem.GetList(l, word)}
        self.respond(responseDict)
        
class AddDictonaryItemHandler(MyRequestHandler):
    isAjax = False
    def get(self, langCode):
        if self.User and self.User.IsAdmin:
            if self.isAjax:
                self.SetTemplate(handlerType, 'dict_AddDictionaryItem.inc.html') 
            value, description, vItemCode = self.g('value'), self.g('description'), self.g('vItemCode')
            word = self.AddDictionaryItem(vItemCode, langCode, value, description)
            if word: self.status="word is added!"
            else: self.status="word is not added"
            self.respond({'new_word':word})
        else:
            self.redirect(LoginHandler.get_url()) 
            
    def AddDictionaryItem(self, langCode, vItemCode, value, description):        
        vItem=dm.VirtualLanguageItem.get(vItemCode)
        language=dm.Language.Get(langCode)
        return dm.DictionaryItem.CreateNew(self.User, language, vItem, 
                                           value, description, 
                                           _autoInsert=True)

class LanguagesHandler(MyRequestHandler):
    def get(self):
        if self.User and self.User.IsAdmin:
            op = self.g('op')
            lang_name, lang_code = self.g('languageName'), self.g('languageCode')
            if op:
                if op == 'add' and lang_name and lang_code:
                    if self.isAjax:
                        self.SetTemplate(handlerType, 'blocks/dict_Languages.inc.html')
                        dm.Language.CreateNew(self.User, lang_name, lang_code, _autoInsert=True)
                        self.respond({'LanguageResults':dm.Language.GetAll()});
                    else:
                        dm.Language.CreateNew(self.User, lang_name, lang_code, _autoInsert=True)
                        self.respond({'LanguageResults':dm.Language.GetAll()});
                    self.status = "new language is added in the system"
                elif op == 'del' and lang_code:
                    lang = dm.Language.Get(lang_code)
                    for item in lang.language_dictionary_items.fetch(100):
                        item.delete()
                    self.status = 'Language is deleted!'
                    lang.delete()
                    self.respond({'LanguageResults':dm.Language.GetAll()})
            else:
                self.respond({'LanguageResults':dm.Language.GetAll()})
        else:
            self.status = 'You must be loged in as admin in order to add new languages'
            self.redirect('/Login')
