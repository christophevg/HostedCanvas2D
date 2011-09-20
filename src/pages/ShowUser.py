import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram, DiagramVersion
from Account import get_account_by_name
from Common  import render_template

class ShowUser(webapp.RequestHandler):
  def get(self):
    user             = urllib.unquote(self.request.path);
    account          = get_account_by_name(user.replace("/~",""))
    ownedDiagrams    = account.owned_diagrams.order("created").fetch(10)
    # TODO: this should look at the versions and uniquely list diagrams
    #       to which this account has co-authored
    authoredDiagrams = account.authored_diagrams.order("created").fetch(10)

    template_values = {
      'account'          : account,
      'ownedDiagrams'    : ownedDiagrams,
      'authoredDiagrams' : authoredDiagrams
    }

    render_template( self, 'ShowUser', template_values )

application = webapp.WSGIApplication( [( '.*', ShowUser ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
