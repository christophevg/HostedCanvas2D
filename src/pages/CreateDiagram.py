from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Common import construct_login_url
from Common import construct_login_urltext

from Common import render_template

class CreateDiagram(webapp.RequestHandler):
  def get(self):
    render_template( self, 'CreateDiagram' )

application = webapp.WSGIApplication( [( '.*', CreateDiagram ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
