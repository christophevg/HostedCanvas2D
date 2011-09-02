from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Diagram import Diagram 
from Common import render_template

class ListDiagrams(webapp.RequestHandler):
  def get(self):
    updated = Diagram.all().order('-updated').fetch(10);
    viewed  = Diagram.all().order('-viewCount').fetch(10);

    for diagram in updated: diagram.load_current();
    for diagram in viewed:  diagram.load_current();

    template_values = {
      'updated' : updated,
      'viewed'  : viewed
    }
    render_template( self, 'ListDiagrams', template_values )

application = webapp.WSGIApplication( [( '.*', ListDiagrams )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
