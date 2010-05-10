from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
import Models.AccountingModels as am
import django.newforms.forms as forms
import django.newforms.fields as fields
class AccountForm(djangoforms.ModelForm):
	 class Meta():
		  model=am.Account
		  exclude = ['RecentTransactions']
class TransactionForm(djangoforms.ModelForm):
	 class Meta():
		  model=am.Transaction
class FinancialCardFrom(djangoforms.ModelForm):
	 class Meta():
		  model=am.FinancialCard
class TransactionBatchForm(djangoforms.ModelForm):
	 class Meta():
		  model=am.TransactionBatch