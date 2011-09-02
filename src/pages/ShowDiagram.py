from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Diagram import Diagram
from Common import render_template

class ShowDiagram(webapp.RequestHandler):
  def get(self):
    key     = self.request.path.replace("/","");
    diagram = Diagram.get(key);

    if diagram:
      template_values = {
        'diagram' : diagram
      }

      render_template( self, 'ShowDiagram', template_values )

application = webapp.WSGIApplication( [( '.*', ShowDiagram ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
