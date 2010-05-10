'''
Created on 18.1.2010

@author: KMihajlov
'''
from lib.appengine_utilities import sessions
def extend_exception(ex, obj):
    ex.args="Happened at: "+str(obj.__class__)+" . The original message:\n%s" % ex.args
    
def get_cvn():
    '''Gets Current Visitors Number'''
    cvn = sessions._AppEngineUtilities_Session.all().count()
    return cvn
