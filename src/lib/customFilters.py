from google.appengine.ext import webapp
 
register = webapp.template.create_template_register()

# access a dictionary
def hash(h, key):
    return h[key] 

