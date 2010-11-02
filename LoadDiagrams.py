import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Model import Diagram

class LoadData(webapp.RequestHandler):
  def get(self):
    db.put( Diagram( key_name = "diagram1",
                     name     = "first diagram",
                     source   = '''
                     diagram secondDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="green"; 
                     }''',
                     width    = 300,
                     height   = 200,
                     tags     = [ "example", "first" ] ) )

    db.put( Diagram( key_name = "diagram2",
                     name     = "second diagram",
                     source   = '''
                     diagram secondDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="red";
                     }''' ,
                     width    = 300,
                     height   = 200,
                     tags     = [ "example", "second" ] ) )
    self.redirect('/')

application = webapp.WSGIApplication( [( '.*', LoadData )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
