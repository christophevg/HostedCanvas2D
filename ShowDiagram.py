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
from Common import render_template

class ShowDiagram(webapp.RequestHandler):
  def get(self):
    key     = self.request.path.replace("/","");
    diagram = Diagram.get_by_key_name(key);

    template_values = {
      'diagram'      : diagram,
      'url'          : construct_login_url(self.request),
      'url_linktext' : construct_login_urltext()
    }

    render_template( self.response, 'ShowDiagram', template_values )

application = webapp.WSGIApplication( [( '.*', ShowDiagram ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
