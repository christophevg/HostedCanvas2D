from google.appengine.ext import db

from Account import Account
from Account import get_account_for_current_user
from Account import get_account_for_user

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
  def get(key):
    diagram = Diagram.get_by_key_name(key);
    if not diagram:
      diagram = Diagram.get_by_key_name( "unknown" );
    if diagram:
    	return diagram.load_current();

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

  def load_current(self):
    self.current = self.versions.order("-created").fetch(1)[0];
    return self;

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

  def asHash(self):
    self.load_current();
    return {
      "id"    : self.key().name(),
      "name"  : self.current.name,
      "descr" : self.current.description,
      "src"   : self.current.source,
      "width" : self.current.width,
      "height": self.current.height,
      "owner" : self.owner.key().name(),
      "author": self.current.author.key().name(),
      "notes" : self.current.notes,
      "views" : self.viewCount,
      "edits" : self.editCount,
      "auth"  : self.owner == get_account_for_current_user()
    };

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
