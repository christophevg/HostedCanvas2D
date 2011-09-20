import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram, DiagramVersion

class ClearDiagrams(webapp.RequestHandler):
  def get(self):
    for diagram in Diagram.all(): db.delete(diagram.key())
    for version in DiagramVersion.all(): db.delete(version.key())
    self.redirect('/')

application = webapp.WSGIApplication( [( '.*', ClearDiagrams )], debug = True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
