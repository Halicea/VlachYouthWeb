'''
Created on 04.1.2010

@author: KMihajlov
'''
import os.path as p

def GetTemplateDir(template_type):
    # @type template_type:str 
    return p.join('Views', 'pages', template_type)

def GetBasesDict():
    return __basesDict__    

def GetMenusDict():
    return __menusDict__

def GetBlocksDict():
    return __blocksDict__

def GetPluginsDict():
    return __pluginsDict__

def GetLinks():
    pass
    
__basesDict__={
        "blog_base":        "../../bases/blog_base.html",
        "accounting_base":  "../../bases/accounting_base.html",
        "admin_base":       "../../bases/admin_base.html",
        "base":             "../../bases/base.html",
        "darkness_base":    "../../bases/darkness_base.html",
        "cms_base":         "../../bases/cms_base.html",
        "mail_base":		"../../bases/mail_base.html",
        }

__menusDict__={
       "mnAccountingSidebar":   "../../menus/accounting_sidebar.inc.html",
       "mnBlogSidebar":         "../../menus/blog_sidebar.inc.html",
       "mnTopMenuAccounting":   "../../menus/top_menu_acc.inc.html",
       "mnTopMenu":             "../../menus/top_menu.inc.html",
       "mnTransactionList":     "transaction_list.inc.html",
       }

__blocksDict__={
        "blLogin":          "../../blocks/login_menu.inc.html",
        "blLanguages":      "../../blocks/dict_Languages.inc.html",
        "blTranslate":      "../../blocks/dict_Translate.inc.html",
        "blPost":           "../../blocks/post.inc.html",
        "blComment":        "../../blocks/comment.inc.html",
        "blWord":           "../../blocks/word.inc.html",
        ### Menu Blocks
        "blAdminMenu":      "../../blocks/menu_links/admin.inc.html",
        "blLogedUserMenu":  "../../blocks/menu_links/loged_user.inc.html",
        "blDefaultMenu":    "../../blocks/menu_links/default.inc.html",
        'blMembersGadget':     "../../blocks/google-ajax-api/members_gadget.html",
        'blTransactionVerification': "../../mail_templates/transaction_verification.html",
        }

__pluginsDict__={
                 'plQuestionarySmall': {'path': '../../lib/plugins/questionaryPlugin',
                                        'view': 'questionaryView.html',
                                        'controller': '',
                                        },
                 }