from google.appengine.api import users

def construct_login_url(request):
  if users.get_current_user():
    return users.create_logout_url(request.uri)
  else:
    return users.create_login_url(request.uri)

def construct_login_urltext():
  if users.get_current_user():
    return 'logout'
  else:
    return 'login'
