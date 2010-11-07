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

from Common import render_template

from Account import get_account_by_name

class ShowUser(webapp.RequestHandler):
  def get(self):
    user = urllib.unquote(self.request.path);
    account = get_account_by_name(user.replace("/~",""))
    ownedDiagrams = Diagram.all().filter("owner =", account).order('created').fetch(10)
    authoredDiagrams = Diagram.all().filter("author =", account).order('created').fetch(10)

    template_values = {
      'account'          : account,
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
