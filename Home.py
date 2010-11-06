from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Common import render_template

from Model import Account

class Home(webapp.RequestHandler):
  def get(self):
    user    = self.get_logged_on_user()
    account = self.get_account_for_user(user)
    self.render( account );

  def post(self):
    user    = self.get_logged_on_user()
    account = self.get_account_for_user(user)
    
    name    = self.request.get("name");
    if name:
      if account: 
        self.render( account, "Cannot update name." )
        return

      if Account.get_by_key_name(name):
        # an account is already registered using this name
        self.render( account, "Name is not available" )
        return
      
      # register the user with the new name
      account = Account( key_name = name, user = user )
      account.put()

    self.render( account );
      
  def get_logged_on_user(self):
    user = users.get_current_user()
    if not user: self.redirect("/");
    return user
  
  def get_account_for_user(self, user):
    account = Account.all().filter( 'user =', user ).fetch(1);
    return account[0] if len(account) > 0 else None

  def render(self, account, msg = None):
    template_values = { 
      'account'      : account,
      'msg'          : msg,
      'url'          : users.create_logout_url("/"),
      'url_linktext' : "logout"
    }
    # if the user has already an account, show its home else provision him
    template_name = 'Home' if account else 'Provision'
    render_template( self.response, template_name, template_values )

application = webapp.WSGIApplication( [ ('.*', Home) ], debug=True )

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
