from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

from Diagram import Diagram
from Common import render_template

# global method to get a diagram, increase the viewCount and keep a reference
# in a session cookie to avoid increasing the viewCount when simply refreshing 
def get_and_count_diagram(key, request, response):
  diagram = Diagram.get(key);
  seen = '';
  if 'seen' in request.cookies: seen = request.cookies['seen'];
  if not "/" + key + "/" in seen:
    diagram.increase_view_count();
    seen += "/" + key + "/";
    response.headers.add_header( 'Set-Cookie','seen=' + seen + ';' );
  return diagram;

# serve the diagram in ADL format
class ServeADL(webapp.RequestHandler):
  def get(self, key, delim):
    diagram = get_and_count_diagram(key, self.request, self.response);

    self.response.headers['Content-Type'] = "application/adl";
    self.response.out.write(diagram.current.source);

# serve the diagram in JSON format, optionally embed it in a callback method
# to allow JSONP requests from other domains
class ServeJSON(webapp.RequestHandler):
  def get(self, key, delim):
    diagram = get_and_count_diagram(key, self.request, self.response);

    response = simplejson.dumps(diagram.to_hash());
    mime = "json";
    
    handler = self.request.get( 'f' );
    if handler: response = handler + "( " + response + " );";

    self.response.headers['Content-Type'] = "application/" + mime;
    self.response.out.write(response);

# serve the diagram as JavaScript that embeds the diagram with a Hosted
# frame
class ServeJS(webapp.RequestHandler):
  def get(self, key, delim):
    diagram = get_and_count_diagram(key, self.request, self.response);

    template_values = {
      'diagram' : diagram
    }

    render_template( self, 'EmbedJS', template_values )

# a catch-all that shouldn't be reached, simply returning the requested path
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
