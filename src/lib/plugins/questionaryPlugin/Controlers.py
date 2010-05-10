'''
Created on 18.1.2010

@author: KMihajlov
'''
from Controllers.MyRequestHandler import MyRequestHandler as mrh
from lib.plugins.questionaryPlugin import Models as qpm
class QuestionaryHandler(mrh):
    def get(self):
       pass 
        
class AnswerAllQuestionaryHandler(mrh):
    def post(self):
        if self.g('key'):
            questionary = qpm.Questionary.get(self.g('key'))
            if questionary:
                questions= qpm.Question.GetAllByQuestioniary(questionary)
                options=[]
                for q in questions:
                    options.extend( qpm.Option.GetAllByQuestion(q) )
                    
                for op in options:
                    option_answer = self.g(str(op.key))
                    if option_answer:
                        qpm.Answer.CreateNew(self.User, option_answer, op, _isAutoInsert=True)
                        
class ResultsQuestionaryHandler(mrh):
    def get(self, key):
        if self.g('key'):
            questionary = qpm.Questionary.get(self.g('key'))
            if questionary:
                questions= qpm.Question.GetAllByQuestioniary(questionary)
                options=[]
                for q in questions:
                    options.extend( qpm.Option.GetAllByQuestion(q) )
                for op in options:
                    option_answer = self.g(str(op.key))
                    if option_answer:
                        
                        