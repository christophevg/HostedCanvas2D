from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

from Diagram import Diagram
from Common import render_template

class ServeADL(webapp.RequestHandler):
  def get(self, key, delim):
    diagram = Diagram.get(key);

    self.response.headers['Content-Type'] = "application/adl";
    self.response.out.write(diagram.current.source);

class ServeJSON(webapp.RequestHandler):
  def get(self, key, delim):
    diagram = Diagram.get(key);
    response = simplejson.dumps(diagram.asHash());
    mime = "json";
    
    handler = self.request.get( 'f' );
    if handler: response = handler + "( " + response + " );";

    self.response.headers['Content-Type'] = "application/" + mime;
    self.response.out.write(response);

class ServeJS(webapp.RequestHandler):
  def get(self, key, delim):
    diagram = Diagram.get(key);

    template_values = {
      'diagram' : diagram
    }

    render_template( self, 'EmbedJS', template_values )
    
class ServeDefault(webapp.RequestHandler):
  def get(self):
    self.response.out.write(self.request.path);
    
application = webapp.WSGIApplication( [
                                        ( '/(.*)(\.|%3A)json',   ServeJSON )
                                      , ( '/(.*)(\.|%3A)adl',    ServeADL  )
                                      , ( '/(.*)(\.|%3A)js',     ServeJS   )
                                      , ( '/(.*)(\.|%3A)script', ServeJS   )
                                      , ( '/(.*)',               ServeDefault )
                                      ], debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
