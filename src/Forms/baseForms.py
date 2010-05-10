#!/usr/bin/env python
from google.appengine.ext import db
import django.newforms.forms as forms
import django.newforms.fields as fileds
from google.appengine.ext.db import djangoforms
from Models.BaseModels import Person
from Models.BaseModels import WishList

class PersonForm(djangoforms.ModelForm):
	class Meta():
		model=Person

class WishListForm(djangoforms.ModelForm):
	class Meta():
		model=WishList
