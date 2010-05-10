
from google.appengine.ext import db
from Models.BaseModels import Person
import datetime as dt
class Questionary(db.Model):
	
	Name = db.StringProperty(required=True)
	Text = db.TextProperty()
	Creator =db.ReferenceProperty(required=True)
	DateCreated =db.DateTimeProperty(required=True)
	DateShown = db.DateTimeProperty(required=True)
	DateOff=db.DateTimeProperty(required=True)
	IsShown =db.BooleanProperty(required=True)
	IsAnonymous =db.BooleanProperty(required=True)
	@classmethod
	def CreateNew(cls, name, creator, 
				  dateShown=dt.datetime.now(), dateOff=dt.datetime.now()+dt.timedelta(days=10), 
				  isShown=True, isAnonymous=True, _isAutoInsert=False):
		result = cls(
					Name = name,
					Creator =creator,
					DateCreated =dt.datetime.now(),
					DateShown = dateShown,
					DateOff=dateOff,
					IsShown =isShown,
					IsAnonymous=isAnonymous,
					)
		if _isAutoInsert:
			result.put()
		return result
	@classmethod
	def GetAllForDisplay(cls, limit=100, offset=0):
		result = cls.gql("WHERE IsShown =:s AND DateOff >: doff AND DateShown <:dshown", 
						 s=True, doff=dt.datetime.now(), dshown=dt.datetime.now()).fetch(limit=limit, offset=offset)
		return result
		
class QuestionType(db.Model):
	Code =db.StringProperty(required=True)
	Description =db.StringProperty(required=True)
	@classmethod
	def CreateNew(cls, code, description, _isAutoInsert=False):
		result=cls(Code=code, Description=description)
		if _isAutoInsert: result.put()
		return result
		
class Question(db.Model):
	Questionary = db.ReferenceProperty(Questionary, required=True, collection_name='questionary_questions' )
	Text = db.StringProperty(required=True)
	QuestionType = db.ReferenceProperty(QuestionType, required=True)
	
	@classmethod
	def CreateNew(cls, questionary, text, questionType, _isAutoInsert=False):
		result=cls(Questionary=questionary, Text=text, QuestionType=questionType)
		if _isAutoInsert: result.put()
		return result
	@classmethod
	def GetAllByQuestioniary(cls, questionary, limit=100, offset=0):
		return questionary.questionary_questions.fetch(limit=limit, offset=offset)
	
class Option(db.Model):
	Question = db.ReferenceProperty(Question, require=True, collection_name='question_options')
	Text = db.StringProperty(required=True)
	
	@classmethod
	def CreateNew(cls, question, text, _isAutoInsert=False):
		result=cls(Question=question, Text=text)
		if _isAutoInsert: result.put()
		return result
	
	@classmethod
	def GetAllByQuestion(cls, question, limit=100, offset=0):
		return question.question_options.fetch(limit, offset)
		

class Answer(db.Model):
	Value = db.StringProperty(required=True)
	Option = db.ReferenceProperty(required=True)
	Owner = db.ReferenceProperty(Person, required=True)
	DateAnswered=db.DateTimeProperty()
	@classmethod
	def CreateNew(cls, owner, value, option, _isAutoInsert=False):
		result=cls(Value=value, 
				Option=option,
				Owner=owner, 
				DateAnswered=dt.datetime.now()
				)
		if _isAutoInsert: 
			result.put()
		return result
	
	@classmethod
	def GetAllByUserByOption(cls, user, option, limit=100, offset=0):
		result= cls.gql("WHERE Owner =:o AND Option =:op", o=user, op=option).fetch(limit=limit, offset=offset)
		return result
	