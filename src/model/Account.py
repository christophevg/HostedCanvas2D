from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import namespace_manager

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

def get_account_for_current_user():
  return get_account_for_user( users.get_current_user() )
