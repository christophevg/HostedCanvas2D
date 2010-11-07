import os
import urllib

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import namespace_manager

def construct_login_url( request ):
  if users.get_current_user():
    return users.create_logout_url(urllib.unquote(request.path))
  else:
    return "/login";

def construct_login_urltext():
  if users.get_current_user():
    return 'logout'
  else:
    return 'login'

def render_template( response, name, values = {} ):
  path = os.path.join( os.path.dirname(__file__), 
                       'templates', namespace_manager.get_namespace(), 
                       name + '.html' )
  response.out.write(template.render(path, values))
