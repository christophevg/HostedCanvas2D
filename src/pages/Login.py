from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Common import render_template

class Login(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      self.redirect("/");
    else:
      providers = [
        { 'name': 'Google',   'url': users.create_login_url(dest_url="/home", federated_identity='google.com/accounts/o8/id') },
        { 'name': 'Yahoo',    'url': users.create_login_url(dest_url="/home", federated_identity='yahoo.com') },
        { 'name': 'MySpace',  'url': users.create_login_url(dest_url="/home", federated_identity='myspace.com') },
        { 'name': 'MyOpenID', 'url': users.create_login_url(dest_url="/home", federated_identity='myopenid.com') }
      ];

      template_values = {
        'providers'    : providers,
        'url'          : "/login",
        'url_linktext' : "login"
      }

      render_template( self, 'Login', template_values )

application = webapp.WSGIApplication( [ ('.*', Login) ], debug=True )

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
