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

import urllib

class ShowUser(webapp.RequestHandler):
  def get(self):
    user = users.User(urllib.unquote(self.request.path).replace("/~",""))
    ownedDiagrams = Diagram.all().filter("owner =", user).order('created').fetch(10)
    authoredDiagrams = Diagram.all().filter("author =", user).order('created').fetch(10)

    template_values = {
      'user'             : user,
      'ownedDiagrams'    : ownedDiagrams,
      'authoredDiagrams' : authoredDiagrams,
      'url'              : construct_login_url(self.request),
      'url_linktext'     : construct_login_urltext()
    }

    path = os.path.join( os.path.dirname(__file__), 
                         'templates', 'ShowUser.html' )
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication( [( '.*', ShowUser ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
