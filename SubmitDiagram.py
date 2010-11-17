from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Common import render_template

from Account import get_account_for_user

from Home import Home
from Diagram import Diagram

from adl import adl

class SubmitDiagram(webapp.RequestHandler):
  def get(self):
    # nothing to get here ...
    self.redirect("/");

  def get_source(self):
    model = adl.parse(self.request.get("src"))
    return "\n".join(["%s" % (s) for s in model])

  def post(self):
    user    = users.get_current_user()
    account = get_account_for_user(user)

    # if the user is logged on, but we find no account, provision him first
    if user != None and account == None:
      Home.show( account, self, "A complete account is needed to submit." );
      return

    diagram = {
      'author'      : account,
      'id'          : self.request.get("id"),
      'source'      : self.get_source(),
      'name'        : self.request.get("name"),
      'description' : self.request.get("descr"),
      'width'       : int(self.request.get("width", default_value="300")),
      'height'      : int(self.request.get("height",default_value="200")),
      'notes'       : self.request.get("notes")
    }
    
    if self.request.get('action') == "save":
      self.save( diagram )
    else:
      template_values = { 
        'diagram' : diagram
      }
      render_template( self, "SubmitDiagram", template_values )
      
  def save(self, diagram):
    prev_diagram = None
    if diagram['id'] != None and diagram['id'] != "":
      prev_diagram = Diagram.get_by_key_name(diagram['id']) 
    
    if prev_diagram == None:
      new_dia = Diagram.create( id          = diagram['id'],
                                name        = diagram['name'],
                                source      = diagram['source'],
                                width       = diagram['width'],
                                height      = diagram['height'],
                                description = diagram['description'],
                                notes       = diagram['notes'],
                                owner       = diagram['author'] )
    else:  
      version = prev_diagram.add_version( name        = diagram['name'],
                                          source      = diagram['source'],
                                          width       = diagram['width'],
                                          height      = diagram['height'],
                                          description = diagram['description'],
                                          notes       = diagram['notes'],
                                          owner       = diagram['author'] )
      new_dia = version.diagram

    self.redirect( "/" + new_dia.key().name() )

application = webapp.WSGIApplication( [ ('.*', SubmitDiagram) ], debug=True )

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
