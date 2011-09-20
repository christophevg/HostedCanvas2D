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

  # method to get the submitted source from the request, parse it and return
  # the parse tree back as cleanly re-generated ADL code (==sanity check)
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
      
  def save(self, data):
    diagram = None
    
    # try to retrieve an existing diagram
    if data['id'] != None and data['id'] != "":
      diagram = Diagram.get_by_key_name(data['id']) 
    
    # if we don't have on, create a new one
    if diagram == None:
      diagram = Diagram.create( id          = data['id'],
                                name        = data['name'],
                                source      = data['source'],
                                width       = data['width'],
                                height      = data['height'],
                                description = data['description'],
                                notes       = data['notes'],
                                owner       = data['author'] )
    else:  
      # update the relevant data
      diagram.name       = data['name'];
      diagram.source     = data['source'];
      diagram.width      = data['width'];
      diagram.height     = data['height'];
      diagram.descripton = data['description'];
      diagram.notes      = data['notes'];

    # persist the diagram, which will trigger the generation of a version
    diagram.persist();

    self.redirect( "/" + diagram.key().name() )

application = webapp.WSGIApplication( [ ('.*', SubmitDiagram) ], debug=True )

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
