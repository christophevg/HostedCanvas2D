from google.appengine.ext import db

from Account import Account
from Account import get_account_for_current_user

import random
import string

class Diagram(db.Model):
  created       = db.DateTimeProperty(auto_now_add=True)
  updated       = db.DateTimeProperty(auto_now=True)
  lastAuthor    = db.ReferenceProperty(Account, collection_name="authored_diagrams")
  owner         = db.ReferenceProperty(Account, collection_name="owned_diagrams")
  tags          = db.StringListProperty()
  viewCount     = db.IntegerProperty(default=1)
  editCount     = db.IntegerProperty(default=1)
  voteUpCount   = db.IntegerProperty(default=0)
  voteDownCount = db.IntegerProperty(default=0)
  visibility    = db.StringProperty( default="public",
                                     choices=set(["public", "hidden"]) )
  status        = db.StringProperty( default="new",
                                     choices=set(["new", "updated", "ok", "nok"]) )
  @staticmethod
  def create(id=None, name="", source="", width=300, height=200,
             description="", notes="", tags=[], owner=None):
    if id == None or id == "": 
      while True:
        id = Diagram.generate_id()
        if Diagram.get_by_key_name(id) == None: break
      
    diagram = Diagram(key_name=id, owner=owner, tags=tags)
    diagram.add_version(owner, name, source, width, height, description, notes)
    return diagram

  @staticmethod
  def generate_id():
    return ''.join((random.choice(string.letters+string.digits) 
      for _ in xrange(random.randint(8,8))))

  @staticmethod
  def add_current(diagrams):
    if type(diagrams).__name__ == 'list':
      for diagram in diagrams:
        diagram.current = diagram.versions.order('-created').fetch(1)[0]
      return diagrams
    else:
      diagrams.current = diagrams.versions.order('-created').fetch(1)[0]
      return diagrams

  def add_version(self, author, name="", source="", width=300, height=200,
                  description="", notes="" ):
    version = DiagramVersion( parent      = self,
                              diagram     = self,
                              author      = author,
                              name        = name,
                              source      = source,
                              width       = width,
                              height      = height,
                              description = description,
                              notes       = notes );
    version.put()
    self.lastAuthor = author
    self.put()
    return version

class DiagramVersion(db.Model):
  diagram       = db.ReferenceProperty(Diagram, collection_name="versions")
  created       = db.DateTimeProperty(auto_now_add=True)
  author        = db.ReferenceProperty(Account, collection_name="authored_versions")
  name          = db.StringProperty()
  source        = db.TextProperty()
  width         = db.IntegerProperty()
  height        = db.IntegerProperty()
  description   = db.TextProperty(default="")
  notes         = db.TextProperty(default="")
