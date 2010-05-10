'''
Created on Sep 8, 2009

@author: kosta halicea
'''

###########
from google.appengine.ext import db
from Models.BaseModels import Person
import datetime as dt
from google.appengine.ext.db import djangoforms
###########
class Account(db.Model):
	AccountNumber = db.StringProperty(required=True)
	BankName = db.StringProperty(required=True)
	Owner = db.ReferenceProperty(reference_class=Person, required=True, collection_name='owner_accounts')
	DateCreated = db.DateTimeProperty()
	Balance = db.FloatProperty()
	
	def getRecentTransactions(self):
		return self.owner_account_transactions.order('-EntryTime').fetch(100)
	RecentTransactions = property(getRecentTransactions)
	
	@classmethod
	def CreateNew(cls, accountNumber, bankName, owner, balance, _isAutoSave=False):
		result = cls(AccountNumber=accountNumber, BankName=bankName, Owner=owner, DateCreated=dt.datetime.now(), Balance=float(balance))
		if _isAutoSave:
			result.put()
		return result
class TransactionModes(object):
	debit = 'debit'
	credit = 'credit'

class TransactionTypeGroup(db.Model):
	Code = db.StringProperty()
	Description = db.TextProperty()
	UsedId = db.StringListProperty()
	DateCreated = db.DateTimeProperty()
	@classmethod
	def CreateNew(cls, code, description, userId, _isAutoInsert=False):
		result = cls(Code=code, Description=description, UserId=userId, dateCreated=dt.datetime.now())
		if _isAutoInsert: result.put()
		return result

class TransactionType(db.Model):
	Code = db.StringProperty(required=True)
	TypeGroup = db.ReferenceProperty(reference_class=TransactionTypeGroup, collection_name='type_group_transaction_types')
	Description = db.TextProperty()
	DateCreated = db.DateTimeProperty()

class TransactionBatch(db.Model):
	DateCreated = db.DateTimeProperty(required=True)
	Owner = db.ReferenceProperty(Person, collection_name='owner_transaction_batches')
	Account = db.ReferenceProperty(Account, collection_name='account_transaction_batches')

class Transaction(db.Model):
	OwnerAccount = db.ReferenceProperty(Account, required=True, collection_name='owner_account_transactions')
	ReferentAccount = db.ReferenceProperty(Account, required=True, collection_name='referent_account_transactions')
	TransactionMode = db.StringProperty(required=True, choices=set([TransactionModes.debit, TransactionModes.credit]))
	TransactionType = db.ReferenceProperty(TransactionType, collection_name='transaction_type_transactions')
	Batch = db.ReferenceProperty(TransactionBatch, collection_name='batch_transactions')
	Ammount = db.FloatProperty(required=True, default=0.0)
	Description = db.TextProperty()
	TransactionTime = db.DateTimeProperty(required=True)
	EntryTime = db.DateTimeProperty(required=True)
	VerifiedByReferentEntityStatus = db.StringProperty()
	TimeOfVerification = db.DateTimeProperty()

	def put(self):
		super(Transaction, self).put()
		ref_financial_card = FinancialCard.GetByOwnerByUser(self.OwnerAccount.Owner, self.ReferentAccount.Owner)
		
		if ref_financial_card.Balance == None: ref_financial_card.Balance = 0.0
		if self.TransactionMode == TransactionModes.credit:
			self.OwnerAccount.Balance += self.Ammount
			ref_financial_card.Balance -= self.Ammount
		elif self.TransactionMode == TransactionModes.debit:
			self.OwnerAccount.Balance -= self.Ammount
			ref_financial_card.Balance += self.Ammount
		else:
			raise Exception("Not Valid Transaction Mode")
		self.OwnerAccount.save()
		ref_financial_card.save()
	@classmethod
	def CreateNew(cls, ownerAccount, referentAccount, transactionMode, transactionType,
				  ammount, description, transactionTime, verifiedByReferentEntityStatus=False,
				  timeOfVerification=None, _isAutoInsert=False):
		result = cls(
					 OwnerAccount=ownerAccount,
					 ReferentAccount=referentAccount,
					 TransactionMode=transactionMode,
					 TransactionType=transactionType,
					 Ammount=float(ammount),
					 Description=description,
					 TransactionTime=transactionTime,
					 EntryTime=dt.datetime.now(),
					 VerifiedByReferentEntityStatus=verifiedByReferentEntityStatus,
					 TimeOfVerification=timeOfVerification
					 )
		if _isAutoInsert:
			result.put()
		return result

class FinancialCard (db.Model):
	DateCreated = db.DateTimeProperty (required=True)
	Owner = db.ReferenceProperty(Person, required=True, collection_name='owner_financial_cards')
	ReferentEntity = db.ReferenceProperty(Person, required=True, collection_name='referent_entity_financial_cards')
	Balance = db.FloatProperty(default=0.0)
	
	def Recalculate(self, _isAutoUpdate=False):
		refAccounts = self.ReferentEntity.owner_accounts
		result = []
		#Potential Big Loop
		for acc in self.Owner.owner_accounts:
			for ref_acc in refAccounts:
				result.extend(Transaction.gql("WHERE OwnerAccount =:oa AND ReferentAccount =:ra", oa=acc, ra=ref_acc))	 
		balance = 0.0
		for trans in result:
			if trans.TransactionMode == TransactionModes.debit:
				balance -= trans.Ammount
			elif trans.TransactionMode == TransactionModes.credit:
				balance += trans.Ammount
		self.Balance = float(balance)
		if _isAutoUpdate:
			self.save()
		return self
	@classmethod
	def CreateNew(cls, owner, referentEntity, balance=0.0, _autoInsert=False):
		result = cls(
				   DateCreated=dt.datetime.now(),
				   Owner=owner,
				   ReferentEntity=referentEntity,
				   Balance=float(balance)
				   )
		# set None to 0
		if result.Balance == None: result.Balance = 0.0
		if _autoInsert:
			result.put()
		return result
	@classmethod
	def GetByOwnerByUser(cls, owner, referentEntity):
		result = cls.all().filter('Owner =', owner).filter('ReferentEntity =', referentEntity).get()
		if result == None:
			result = cls.CreateNew(owner, referentEntity, True)
		return result
	@classmethod
	def RecalculateFinancialCard(cls, owner, referentEntity, _isAutoUpdate=False):
		fcard = cls.gql("WHERE Owner =:o AND ReferentEntity =:re", o=owner, re=referentEntity)
		return fcard.Recalculate(_isAutoUpdate=_isAutoUpdate)
		
	#----------------------

class TransactionVerificationRequest(db.Model):
	''' Object that is stored when a mail is sent to a person that need to verify some transaction'''
	UrlCode = db.StringProperty(required=True)
	Sender = db.ReferenceProperty(reference_class=Person, collection_name='sender_transaction_verification_requests')
	Reciever = db.ReferenceProperty(reference_class=Person, collection_name='reciever_transaction_verification_requests')
	Transaction = db.ReferenceProperty(Transaction, collection_name='transaction_transaction_verification_requests')
	SendDate = db.DateTimeProperty()
	@classmethod
	def CreateNew(cls, transaction, _autoInsert=False):
		# @type cls TransactionVerificationRequest
		url_code = transaction.key().__str__()
		result = cls(
					UrlCode=url_code,
					Sender=transaction.OwnerAccount.Owner,
					Reciever=transaction.ReferentAccount.Owner,
					Transaction=transaction,
					SendDate=dt.datetime.now()
					)
		if _autoInsert: 
			result.put()
		return result
