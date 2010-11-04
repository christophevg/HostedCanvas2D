import os
from google.appengine.ext.webapp import template

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Model import Diagram

from Common import construct_login_url
from Common import construct_login_urltext

import urllib

from Common import render_template

class ShowUser(webapp.RequestHandler):
  def get(self):
    user = urllib.unquote(self.request.path);
    # gmail accounts drop the @gmail.com part to create a nickname
    if user.find( "@" ) < 0: user = user + "@gmail.com"
    user = users.User(user.replace("/~",""))
    ownedDiagrams = Diagram.all().filter("owner =", user).order('created').fetch(10)
    authoredDiagrams = Diagram.all().filter("author =", user).order('created').fetch(10)

    template_values = {
      'user'             : user,
      'ownedDiagrams'    : ownedDiagrams,
      'authoredDiagrams' : authoredDiagrams,
      'url'              : construct_login_url(self.request),
      'url_linktext'     : construct_login_urltext()
    }

    render_template( self.response, 'ShowUser', template_values )

application = webapp.WSGIApplication( [( '.*', ShowUser ) ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
