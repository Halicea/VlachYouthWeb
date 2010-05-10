'''
Created on Oct 16, 2007

@author: Kosta
'''
from MyRequestHandler import MyRequestHandler
from MyRequestHandler import __mode__

import Models.AccountingModels as am
import Models.DictionaryModels as dm
import Forms.accountingForms as af
import Forms.baseForms as bf
import datetime as dt
import accountingHandlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler
class DjangoFormTestHandler(MyRequestHandler):
	 def get(self):
		  f = bf.PersonForm(instance=self.User)
		  #f = af.AccountForm()
		  self.respond({'f':f})
class TestHandler(MyRequestHandler):
    def get(self):
        self.respond({"test": af.AccountForm()})
        #all_acc = am.Account.all()
    def post(self):
        data= am.AccountForm(data=self.request.POST)
        if data.is_valid():
            newAcc = data.save(commit=False)
            newAcc.put()
            self.response.out.write("Item is Saved")
            self.response.out.write(data)
        else:
            self.response.out.write("Invalid Data Was Passed")
            self.response.out.write(data)
        
class TestOldHandler (MyRequestHandler):
    def get(self):
        if __mode__ == 'Debug':
            pass        
    def insert_primary_language(self):
        status = ''
        lang= dm.PrimaryLanguage.all().get()
        if(lang):
            lang.delete()
            status+='Old Language was deleted and '
        lang = dm.Language(
                    DateCreated = dt.datetime.now(),
                    Creator = self.User,
                    LanguageName = 'English',
                    LanguageCode = 'en'
                           )
        lang.put()
        prim_lang = dm.PrimaryLanguage(
                                       DateModified =dt.datetime.now(),
                                       Language=lang
                                       )
        prim_lang.put()
        return status+"English as primary language is added!"
    def delete_account_data(self):
        cont_d = True
        cont_b = True
        cont_c = True
        bcount = 0
        dcount = 0
        ccount = 0
        while cont_d:
            dolgovi = am.Transaction.all().fetch(100)
            if len(dolgovi) < 100:
                cont_d = False
            for d in dolgovi:
                d.delete()
                dcount += 1
        while cont_b:
            balansi = am.Account.all().fetch(100)
            if len(balansi) < 100:
                cont_b = False
            for b in balansi:
                b.delete()
                bcount += 1
        while cont_c:
            kartici = am.FinancialCard.all().fetch(100)
            if len(kartici) < 100:
                cont_c = False
            for c in kartici:
                c.delete()
                ccount += 1

        return 'Deleted all items---<br/>' + 'Balances: ' + str(bcount) + '<br/>Depts: ' + str(dcount) + '<br/> Financial Cards: ' + str(ccount)
    def list_users(self):
        users = bm.Person.all().fetch(100)
        response = '<p><h1>User List:</h1></p><br/>'
        response += '''<table border="1">
            <tr style="font-size: 20px; background-color:gray; color:white; text-align:center">
                <td width=150>Full Name</td><td width=200>Email</td><td width=60>Admin</td><td>Pass</td>
            </tr>

        '''
        response += ' '.join(['<tr><td>' + u.Name + ' ' + u.Surname + '</td><td>' + u.Email + '</td><td>' + str(u.IsAdmin) + '</td><td>' + u.Password + '</td></tr>' for u in users])
        response += '</table>'
        return response
    def delete_user(self, uname):
        user = bm.Person.all().filter('UserName=', uname).get()
        user.delete()
    def show_user(self, uname, passwd):
        us = bm.Person.all().filter('Email=', uname).filter('Password=', passwd).get()
        users = [us, ]
        response = '<p><h1>User List:</h1></p><br/>'
        response += '''<table border="1">
            <tr style="font-size: 20px; background-color:gray; color:white; text-align:center">
                <td width=150>Full Name</td><td width=200>Email</td><td width=60>Admin</td><td>Pass</td>
            </tr>

        '''
        response += ' '.join(['<tr><td>' + u.Name + ' ' + u.Surname + '</td><td>' + u.Email + '</td><td>' + str(u.IsAdmin) + '</td><td>' + u.Password + '</td></tr>' for u in users])
        response += '</table>'
        return response
    def get_current_session_user(self):
        #self.response.out.write( 'Test out:' )
        u = self.session.get('user', None)
        if u:
            self.response.out.write(u.Name + '<br/>' + u.Email + '<br/>')
        else:
            self.response.out.write('No User loged in currently')

    def set_admin(self):
        pers = bm.Person(
                        Name='Kosta',
                        Surname='Mihajlov',
                        Email='kosta.halicha@gmail.com',
                        Password='halicha$123',
                        Public=True,
                        Notify=True,
                        DateAdded=dt.datetime.now(),
                        IsAdmin=True
                        )
        pers.put()
        return 'Created user Kosta'

class TestLayoutHandler(MyRequestHandler):
    def get(self):
        self.SetTemplate("",'Views\\testLayout.html')
        self.response.out.write(self.Template)

import Models.BaseModels as bm