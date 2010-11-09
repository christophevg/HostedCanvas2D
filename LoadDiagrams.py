import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram
from Account import get_account_by_name

class LoadData(webapp.RequestHandler):
  def get(self):
    Diagram.create( id          = "diagram1",
                    owner       = get_account_by_name( 'christophe.vg' ),
                    name        = "first diagram",
                    description = "description of first diagram",
                    notes       = "notes of first diagram",
                    source      = '''
diagram secondDiagram { 
  rectangle r +width=50 +height=50 +lineColor="green"; 
}''',
                    width       = 300,
                    height      = 200,
                    tags        = [ "example", "first" ] )

    Diagram.create( id          = "diagram2",
                    owner       = get_account_by_name( 'christophe.vg' ),
                    name        = "second diagram",
                    description = "description of second diagram",
                    notes       = "notes of second diagram",
                    source      = '''
diagram secondDiagram { 
  rectangle r +width=50 +height=50 +lineColor="red";
}''' ,
                    width       = 300,
                    height      = 200,
                    tags        = [ "example", "second" ] )

    Diagram.create( name        = "anonymous diagram",
                    description = "description of anonymous diagram",
                    notes       = "notes of anonymous diagram",
                    source      = '''
diagram anonymousDiagram { 
  rectangle r +width=50 +height=50 +lineColor="blue"; 
}''',
                    width       = 300,
                    height      = 200,
                    tags        = [ "example", "anonymous" ] )

    self.redirect('/')

application = webapp.WSGIApplication( [( '.*', LoadData )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
