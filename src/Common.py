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
  return 'logout' if users.get_current_user() else 'login'

def render_template( handler, name, values = {} ):
  values["url"] = construct_login_url(handler.request)
  values["url_linktext"] = construct_login_urltext()

  path = os.path.join( os.path.dirname(__file__), 
                       'templates', namespace_manager.get_namespace(), 
                       name + '.html' )
  handler.response.out.write(template.render(path, values))
