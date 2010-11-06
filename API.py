import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Model import Account

class UserAPI(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    account = Account.get_by_key_name( self.request.get('name') )
    if account: self.response.out.write(account.key().name())

application = webapp.WSGIApplication( [( '/api/user', UserAPI )], debug = True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
