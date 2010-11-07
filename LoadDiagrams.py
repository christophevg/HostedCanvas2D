import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram
from Account import get_account_by_name

class LoadData(webapp.RequestHandler):
  def get(self):
    db.put( Diagram( key_name = "diagram1",
                     owner    = get_account_by_name( 'christophe.vg' ),
                     author   = get_account_by_name( 'christophe.vg' ),
                     name     = "first diagram",
                     source   = '''
                     diagram secondDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="green"; 
                     }''',
                     width    = 300,
                     height   = 200,
                     tags     = [ "example", "first" ] ) )

    db.put( Diagram( key_name = "diagram2",
                     owner    = get_account_by_name( 'christophe.vg' ),
                     author   = get_account_by_name( 'christophe.vg' ),
                     name     = "second diagram",
                     source   = '''
                     diagram secondDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="red";
                     }''' ,
                     width    = 300,
                     height   = 200,
                     tags     = [ "example", "second" ] ) )

    db.put( Diagram( key_name = "xyz",
                     name     = "anonymous diagram",
                     source   = '''
                     diagram anonymousDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="blue"; 
                     }''',
                     width    = 300,
                     height   = 200,
                     tags     = [ "example", "anonymous" ] ) )

    self.redirect('/')

application = webapp.WSGIApplication( [( '.*', LoadData )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
