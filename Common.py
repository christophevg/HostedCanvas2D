from google.appengine.api import users

import urllib

def construct_login_url(request):
  if users.get_current_user():
    return users.create_logout_url(urllib.unquote(request.path))
  else:
    return users.create_login_url(urllib.unquote(request.path))

def construct_login_urltext():
  if users.get_current_user():
    return 'logout'
  else:
    return 'login'
