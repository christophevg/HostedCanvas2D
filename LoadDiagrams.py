import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram

class LoadData(webapp.RequestHandler):
  def get(self):
    db.put( Diagram( key_name = "diagram1",
                     author   = users.get_current_user(),
                     title    = "first diagram",
                     source   = '''
                     diagram secondDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="green"; 
                     }''' ) )

    diag2 = Diagram( key_name = "diagram2",
                     author   = users.get_current_user(),
                     title    = "second diagram",
                     source   = '''
                     diagram secondDiagram { 
                       rectangle r +width=50 +height=50 +lineColor="red";
                     }''' )
    diag2.put();
    self.redirect('/')

application = webapp.WSGIApplication( [( '.*', LoadData )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
