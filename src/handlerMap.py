'''
Created on Jul 26, 2009
@author: kosta
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.gaesessions import SessionMiddleware
########
import Controllers.adminHandlers as ah
import Controllers.baseHandlers as bh
import Controllers.postHandlers as ph
import Controllers.staticHandlers as sh
import Controllers.profileHandlers as prh
import Controllers.testHandlers as th
import Controllers.accountingHandlers as acch
import Controllers.dictionaryHandlers as dh
import Controllers.cmsHandlers as cms

#"""Load custom Django template filters"""
#webapp.template.register_template_library('lib.customFilters')

debug=True
application = webapp.WSGIApplication(
			[
			 ('/djangotest', th.DjangoFormTestHandler),
			 ('/Test', th.TestHandler),
			 ('/TestLayout', th.TestLayoutHandler),
			 ##########
			 
			 ## Standard Handlers
			 ('/testis', bh.testHandler),
			 ('/Login', bh.LoginHandler),
			 ('/Logout', bh.LogoutHandler),
			 ('/AddUser', bh.AddUserHandler),
			 ('/WishList', bh.WishListHandler),
			 ###########
			 
			 ## Post Handlers
			 ('/', ph.HomeHandler),
			 ('/post', ph.PostHandler),
			 ('/comment', ph.CommentHandler),
			 #(r'/images/(.*)', ph.PostImageHandler),
			 ('/quote', ph.QuoteHandler),
			 ###########
			 
			 ## Dictionary Handlers
			 ('/dictionary/translate',		  dh.TranslateHandler),
			 ('/dictionary/languages',		  dh.LanguagesHandler),
			 ('/dictionary/(.*)',			   dh.WordHandler),
			 ('/dictionary/words/(.*)/(.*)',	dh.WordHandler),
			 ('/dictionary/addWord/(.*)',	   dh.AddDictonaryItemHandler),
			 ###########
			 
			 ## Profile Handlers
			 (r'/Profile', prh.UserProfileHandler),
			 ('/Profile/Images', prh.ProfileImagesHandler),
			 ###########
			 
			 ## Administrator Handlers
			 ('/admin/SearchUsers', ah.UserSearchHandler ),
			 ('/admin/SearchResults', ah.SearchResultsHandler ),
			 ('/admin/AddAdmin', ah.AddAdminHandler),
			 ('/admin/ListAdmins', ah.ListAdminsHandler),
			 ('/admin/ListUsers', ah.ListUsersHandler),
			 ###########
			
			 ## Static Handlers
			 ('/About', sh.AboutHandler),
			 ('/Links', sh.LinksHandler),
			 ('/Contact', sh.ContactHandler),
			 ('/NotAuthorized', sh.NotAuthorizedHandler),
			 ###########
			
			 ## Accounting Handlers
			 ('/accounting/Account', acch.AccountHandler),
			 ('/accounting/Transaction', acch.TransactionHandler),
			 ('/accounting/TransactionList', acch.UserTransactionListHandler),
			 ('/accounting/FinancialCard', acch.FinancialCardHandler),
			 (r'/accounting/trans_verification/(.*)', acch.TransactionVerificationHandler),
			 ('/accounting/admin/TransactionTypeGroup', acch.TransactionTypeGroupHandler),
			 ('/accounting/admin/TransactionType', acch.TransactionTypeHandler),
			 ('/accounting', acch.TransactionHandler),
			 ###########
			 
			 ## CMS Handlers
			 ('/cms/links', cms.CMSLinksHandler),
			 ('/cms/content', cms.CMSContentHandler),
			 ('/cms/pages/(.*)', cms.CMSPageHandler),   
			 ###########
			 
			 ('/(.*)', sh.NotExistsHandler),
			], debug=debug)
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app)
    return app
def main():
	run_wsgi_app(\
					 webapp_add_wsgi_middleware(application)\
					)

if __name__ == "__main__":
	main()