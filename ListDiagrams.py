import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.template import create_template_register

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from Diagram import Diagram

class ListDiagrams(webapp.RequestHandler):
    def get(self):
        diagram_query = Diagram.all().order('created')
        diagrams = diagram_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'login'

        template_values = {
            'diagrams': diagrams,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join( os.path.dirname(__file__), 
                             'templates', 'ListDiagrams.html' )
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication( [( '.*', ListDiagrams )], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
