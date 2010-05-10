'''
Created on Sep 8, 2009
@author: kosta halicea
'''
import datetime as dt
from MyRequestHandler import MyRequestHandler as mrh
from Controllers.baseHandlers import LoginHandler
from Models.BaseModels import Person
import Models.AccountingModels as am
from google.appengine.api import mail
from google.appengine.ext.webapp import template
import lib.messages as message
import lib.paths as paths
from Forms.accountingForms import AccountForm
#import pdb
handlerType = 'accounting'

class AccountingHandler(mrh):
	def respond(self, dict={}):
		if dict == None:
			dict = {}
		if not dict.has_key("financial_cards"):
			dict["financial_cards"] = self.User.owner_financial_cards.fetch(limit=10)
		if not dict.has_key('accounts'):
			dict['accounts'] = self.User.owner_accounts
		if not dict.has_key('new_account'):
			dict['new_account']= AccountForm()
		self.response.out.write(template.render(self.Template, self.render_dict(dict)))
	def redirect_login(self):
		self.redirect(LoginHandler.get_url())

class AccountHandler(AccountingHandler):
	def get(self):
		local = {}
		if self.User:
			if self.g("key"):
				acc = am.Account.get(self.g('key'))
				if acc:
					local["currentAccount"] = AccountForm(data = acc)
			self.respond(local)
		else:
			self.status = message.must_be_loged
			self.redirect(LoginHandler.get_url())
	def post(self):
		#self.TemplateType="accounting"
		#import rpdb2; rpdb2.start_embedded_debugger('test')
		if self.User:
			if self.g('op') == 'new':
				form=AccountForm(self.request.POST)
				if form.is_valid():
					result=form.save(commit=False)
					result.put()
				#accountNumber = self.g("AccountNumber")
				#bankName = self.g("BankName")
				#balance = float(self.g("Balance"))
				#owner = self.User
				#if accountNumber and bankName and balance:
					self.status = message.item_is_saved
				#	am.Account.CreateNew(accountNumber, bankName, owner, balance, _isAutoSave=True)
				else:
					self.status = message.invalid_data_passed+ '</br>' + str(form.AccountNumber) + str(form.BankName)+str(form.Balance) 
			self.respond()
		else:
			self.status = message.must_be_loged
			self.redirect(LoginHandler.get_url())

class TransactionTypeGroupHandler(AccountingHandler):
	def get(self):
		if self.request.get('action'):
			if self.g('action') == 'delete' and self.g('key'):
				del_item = am.TransactionTypeGroup.get(self.request.get('key'))
				if del_item:
					del_item.delete()
					self.status = 'Item Deleted'
				else:
					self.status = 'Such Item Does Not exists!'
			else:
				self.status = 'Not valid Request Key'
				transaction_type_groups = am.TransactionTypeGroup.all().fetch(limit=100)
			self.respond(locals())
		elif self.request.get('Code'):
			new_item = am.TransactionTypeGroup(
							   Code=self.request.get('Code'),
							   Description=self.request.get('Description'),
							   DateCreated=dt.datetime.now()
							   )
			new_item.put()
			transaction_type_groups = am.TransactionTypeGroup.all().fetch(limit=100)
			self.respond(locals())
		else:
			transaction_type_groups = am.TransactionTypeGroup.all().fetch(limit=100)
			self.respond(locals())

class TransactionTypeHandler(AccountingHandler):
	def get(self):
		if self.request.get('action'):
			if self.request.get('action') == 'delete' and self.request.get('key'):
				del_item = am.TransactionType.get(self.request.get('key'))
				if del_item:
					del_item.delete()
					self.status = ' Item Deleted'
				else:
					self.status = ' Such Item Does Not exists! '
			else:
				self.status = 'Not valid Request Key'
			transaction_type_groups = am.TransactionTypeGroup.all()
			transaction_types = am.TransactionType.all()
			self.respond(locals())
		elif self.request.get('Code') and self.request.get('TypeGroup'):
			gr = am.TransactionTypeGroup().get(self.request.get('TypeGroup'))
			new_item = am.TransactionType(
						  Code=self.request.get('Code'),
						  TypeGroup=gr,
						  Description=self.request.get('Description'),
						  DateCreated=dt.datetime.now()
						  )
			new_item.put()
	
			transaction_type_groups = am.TransactionTypeGroup.all()
			transaction_types = am.TransactionType.all()
	
			self.respond(locals())
		else:
			transaction_type_groups = am.TransactionTypeGroup.all()
			transaction_types = am.TransactionType.all()
			self.respond(locals())

class TransactionHandler(AccountingHandler):
	def get(self):
		allUsers = Person.all()
		ownerAccount = None
		isCash = False
		if self.User:
			if self.g('OwnerAccount'):
				if self.g('op') == 'new':
					ownerAccount = am.Account.get(self.g('OwnerAccount'))
					if str(ownerAccount.Owner.key()) != str(self.User.key()):
						ownerAccount = None
				elif self.g('op') == 'search':
					allUsers = Person.all()
					self.respond(locals())
				elif self.g('op') == 'cash':
					IsCash=True
				self.respond(locals())
			else:
				self.status = message.invalid_data_passed
				self.redirect(AccountHandler.get_url())
		else:
			self.status = message.must_be_loged
			self.redirect(LoginHandler.get_url())

	def validate_retrieve(self):
		OwnerAccountKey = self.g('OwnerAccountKey')
		ReferentAccountKey = self.g('ReferentAccountKey')
		TransactionMode = self.g('TransactionMode')
		TransactionType = am.TransactionType.all().get() #self.g('TransactionType')
		BatchKey = None #self.g('BatchKey')
		Ammount = self.g('Ammount')
		Description = self.g('Description')
		TransactionTime = dt.datetime.strptime(self.g('TransactionTime'), '%m/%d/%Y')
		EntryTime = dt.datetime.now()
		VerifiedByReferentEntityStatus = "Yes"
		NotifySecondParty = True #self.request.get( 'Notify' ) == u'on'
		TimeOfVerification = None
		mess = str(locals())
		result = None
		try:
			if TransactionMode and Ammount and TransactionTime and Description and EntryTime and ReferentAccountKey and OwnerAccountKey:
				ReferentAccount = am.Account.get(ReferentAccountKey)
				OwnerAccount = am.Account.get(OwnerAccountKey)
				BatchKey = BatchKey and am.TransactionBatch.get(BatchKey) or None
				result = am.Transaction.CreateNew(
								  OwnerAccount, ReferentAccount, TransactionMode, TransactionType,
								  Ammount, Description, TransactionTime, VerifiedByReferentEntityStatus,
								  TimeOfVerification,
								  _isAutoInsert=True)
				return (result, NotifySecondParty, '')
			else:
				return (None, False, mess)
		except Exception, ex:
			mess += ',exception:' + str(ex)
			return (result, False, mess)

	#Process the request here
	def post(self):
		if self.User:
			result, notify, message = self.validate_retrieve()
			if result:
				#if notify:
				#	self.notify_second_party(result)
				self.status = "The transaction is added!"
				self.redirect(UserTransactionListHandler.get_url())
			else:
				self.status = 'You did not passed valid parameters, Message:' + message
				self.respond(locals())
		else:
			self.status = 'You Must be loged in in order to manage your Account'
			self.redirect(LoginHandler.get_url())

	def notify_second_party(self, transaction):
		acc = am.TransactionVerificationRequest.CreateNew(transaction, _autoInsert=True)
		dict = {}
		dict['verification'] = acc
		body = template.render(paths.GetBlocksDict()["blTransactionVerification"], dict)
	
		message = mail.EmailMessage()
		message.subject = 'Transaction Acceptance Form'
		message.sender = 'kosta.mihajlov@gmail.com'
		message.to = acc.Reciever.Email
		message.html = body
		message.Send()

class UserTransactionListHandler(AccountingHandler):
	def get(self):
		result = None
		if self.User:
			if self.User.owner_accounts.get():
				transaction_results = self.User.owner_accounts.get().owner_account_transactions.fetch(limit=10)
			allUsers = Person.all()
			self.respond(locals())
		else:
			self.status = 'You Must be LogedIn in order to see your Balance'
			self.redirect(LoginHandler.get_url())

class FinancialCardHandler(AccountingHandler):
	def get(self):
		if self.User:
			self.respond(self.base_params())
		else:
			self.status = 'You must be loged in in order to use the Accounting Service'
			self.redirect(LoginHandler.get_url())
	def post(self):
		if self.User:
			d = self.base_params()
			if self.request.get('UserKey'):
				if self.request.get('From') and self.request.get('From'):
					zd = Person.get(self.request.get('UserKey'))
					#search_result = am.Dolg.gql( 'WHERE (zel = :zd OR dal = :zd) AND owner:ow', zd=zd, ow=self.User ).fetch( limit=100 )
					transaction_results = am.Transaction.all().filter('OwnerAccouny=', self.User).filter('ReferentAccouny=', zd).fetch(limit=100)
					#search_result = db.GqlQuery("SELECT * FROM Dolg WHERE owner= :1 AND (zel= :2 OR dal= :2)", self.User, zd)
					d['transaction_results'] = transaction_results
					self.respond(d)
		else:
			self.status = 'You must be loged in in order to use the Accounting Service'
			self.redirect(LoginHandler.get_url())

	def base_params(self):
		financialCard = None
		refUser = None
		allUsers = Person.all().fetch(100)
		if self.g('UserKey'):
			refUser = Person.get(self.request.get('UserKey'))
			if refUser:
				financialCard = am.FinancialCard.GetByOwnerByUser(self.User, refUser)	
				#if there is no initial balance or recalculation is asked , run recalculate
				if financialCard and (financialCard.Balance == None or (self.g('op') and self.g('op') == 'recalc')):
					financialCard.Recalculate(True)
			else:
				self.status = 'There is not transaction card for this User'
		else:
			self.status = 'Invalid Data'
		return {"financialCard":financialCard, "refUser":refUser, "allUsers":allUsers}

class TransactionVerificationHandler(AccountingHandler):
	def get(self, verification_key):
		verification = am.TransactionVerificationRequest.get(verification_key)
		#change the user login now
		if verification and verification.Reciever != self.User:
			self.User = verification.Reciever
		if self.User and verification:
			if self.request.get('yesno'):
				accept = self.request.get('yesno') == 'true'
				tr = verification.Transaction
				tr.Verified = accept
				tr.save()
				verification.delete()
				self.status = 'Transaction is Updated as ' + str(accept)
				self.redirect(TransactionHandler.get_url())
			else:
				self.status = 'You Must Choose whether you accept or reject the Transaction'
				self.redirect(TransactionHandler.get_url() + '?op=new')
		else:
			if not self.User:
				self.status = 'You must be loged in in order to verify some transaction!'
				self.redirect(LoginHandler.get_url(), permanent=False)
			elif verification:
				self.status = 'Verification is not instantiated'
				self.redirect(TransactionHandler.get_url())
			else:
				self.status = 'You\'re loged in as other User so you\'ve been loged out and then loged in as'
