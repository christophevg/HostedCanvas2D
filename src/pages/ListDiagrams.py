from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Diagram import Diagram 
from Common import render_template

class ListDiagrams(webapp.RequestHandler):
  def get(self):
    diagrams = Diagram.add_current(Diagram.all().order('-updated').fetch(10))

    template_values = {
      'diagrams' : diagrams
    }

    render_template( self, 'ListDiagrams', template_values )

application = webapp.WSGIApplication( [( '.*', ListDiagrams )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
