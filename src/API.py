import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Account import get_account_by_name

# this API module provides REST interfaces to the underlying datamodel
# currently supported calls include
# /api/user?name=someusername - returns someusername if the user exists
# TODO: change this to returning a JSON object representing the user
# TODO: change this to a similar interface with extensions on user
#       e.g. /~someuser.json

class UserAPI(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    account = get_account_by_name( self.request.get('name') )
    if account: self.response.out.write(account.key().name())

application = webapp.WSGIApplication( [( '/api/user', UserAPI )], debug = True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
