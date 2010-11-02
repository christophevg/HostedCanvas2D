import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.template import create_template_register

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Model import Diagram

from Common import construct_login_url
from Common import construct_login_urltext

class ListDiagrams(webapp.RequestHandler):
  def get(self):
    diagrams = Diagram.all().order('created').fetch(10)

    template_values = {
      'diagrams'     : diagrams,
      'url'          : construct_login_url(self.request),
      'url_linktext' : construct_login_urltext()
    }

    path = os.path.join( os.path.dirname(__file__), 
                         'templates', 'ListDiagrams.html' )
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication( [( '.*', ListDiagrams )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
