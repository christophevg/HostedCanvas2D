import os
from google.appengine.ext.webapp import template

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram

from Common import construct_login_url
from Common import construct_login_urltext

class ShowDiagram(webapp.RequestHandler):
  def get(self):
    key     = self.request.path.replace("/","");
    diagram = db.get(key);

    template_values = {
      'diagram'      : diagram,
      'url'          : construct_login_url(self.request),
      'url_linktext' : construct_login_urltext()
    }

    path = os.path.join( os.path.dirname(__file__), 
                         'templates', 'ShowDiagram.html' )
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication( [( '.*', ShowDiagram ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
