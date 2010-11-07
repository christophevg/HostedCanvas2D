from google.appengine.ext import db
from google.appengine.api import namespace_manager

class Diagram(db.Model):
  owner         = db.UserProperty(auto_current_user_add=True)
  author        = db.UserProperty(auto_current_user=True)
  name          = db.StringProperty()
  source        = db.TextProperty()
  width         = db.IntegerProperty()
  height        = db.IntegerProperty()
  description   = db.TextProperty(default="")
  tags          = db.StringListProperty()
  created       = db.DateTimeProperty(auto_now_add=True)
  updated       = db.DateTimeProperty(auto_now=True)
  viewCount     = db.IntegerProperty(default=1)
  editCount     = db.IntegerProperty(default=1)
  voteUpCount   = db.IntegerProperty(default=0)
  voteDownCount = db.IntegerProperty(default=0)
  notes         = db.TextProperty(default="")
  visibility    = db.StringProperty( default="public",
                                     choices=set(["public", "hidden"]) )
  status        = db.StringProperty( default="new",
                                     choices=set(["new", "updated", "ok", "nok"]) )

class Account(db.Model):
  user = db.UserProperty(auto_current_user=True)

def get_account_by_name(name):
  namespace = namespace_manager.get_namespace();
  try:
    namespace_manager.set_namespace("-global-")
    account = Account.get_by_key_name(name)
  finally:
    namespace_manager.set_namespace(namespace);

  return account

def create_account(key_name, user):
  namespace = namespace_manager.get_namespace();
  try:
    namespace_manager.set_namespace("-global-")
    account = Account( key_name = key_name, user = user )
  finally:
    namespace_manager.set_namespace(namespace);

  return account

def get_account_for_user(user):
  namespace = namespace_manager.get_namespace();
  try:
    namespace_manager.set_namespace("-global-")
    account = Account.all().filter( 'user =', user ).fetch(1);
  finally:
    namespace_manager.set_namespace(namespace);

  return account[0] if len(account) > 0 else None
