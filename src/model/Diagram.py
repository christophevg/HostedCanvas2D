from google.appengine.ext import db

from Account import Account
from Account import get_account_for_current_user
from Account import get_account_for_user
from Account import get_account_by_name

import random
import string
import datetime

# the diagram Model class contains the _current_ instance of a Diagram
# with all properties
class Diagram(db.Model):
  created       = db.DateTimeProperty(auto_now_add=True)
  updated       = db.DateTimeProperty()
  owner         = db.ReferenceProperty(Account, collection_name="owned_diagrams")
  author        = db.ReferenceProperty(Account, collection_name="authored_diagrams")
  name          = db.StringProperty()
  source        = db.TextProperty()
  width         = db.IntegerProperty()
  height        = db.IntegerProperty()
  description   = db.TextProperty(default="")
  notes         = db.TextProperty(default="")
  tags          = db.StringListProperty()
  viewCount     = db.IntegerProperty(default=1)
  editCount     = db.IntegerProperty(default=1)
  voteUpCount   = db.IntegerProperty(default=0)
  voteDownCount = db.IntegerProperty(default=0)
  visibility    = db.StringProperty( default="public",
                                     choices=set(["public", "hidden"]) )
  status        = db.StringProperty( default="new",
                                     choices=set(["new", "updated", "ok", "nok"]) )

  # static get/factory method to retrieve a Diagram or return a Diagram
  # representing the unknown diagram
  @staticmethod
  def get(key):
    diagram = Diagram.get_by_key_name(key);
    # load the unknown diagram from the store
    if not diagram: diagram = Diagram.get_by_key_name( "unknown" );
    # no diagram available, generate one
    if not diagram: diagram = Diagram.create_unknown_diagram();
    return diagram;

  # static factory method to create a default unknown diagram diagram
  # TODO: remove personal account reference
  @staticmethod
  def create_unknown_diagram():
    return Diagram.create(
        id          = "unknown",
        owner       = get_account_by_name( 'christophe.vg' ),
        name        = "Unknown Diagram",
        source      = '''
diagram UnknownDiagram {
  [@60,60]
  note error +text="Unknown Diagram";
}''',
        description = '''This a placeholder for unknown diagrams.
The diagram referenced by the given name was not found in our repository.''',
        width       = 250,
        height      = 200 )

  # static factory method to create a new Diagram (not persisted yet!)
  # it generates a random ID if none is provided
  @staticmethod
  def create(id=None, name="", source="", width=300, height=200,
             description="", notes="", tags=[], owner=None):
    if id == None or id == "": 
      while True:
        id = Diagram.generate_id()
        if Diagram.get_by_key_name(id) == None: break
    
    # create the new Diagram
    return Diagram( key_name=id, name=name, source=source, 
                    width=width, height=height, description=description, 
                    notes=notes, owner=owner, tags=tags )

  # static method to generate random IDs
  @staticmethod
  def generate_id():
    return ''.join((random.choice(string.letters+string.digits) 
      for _ in xrange(random.randint(8,8))))

  # instance method to persist any changes to the diagram to the datastore,
  # while creating an additional version
  # the updated field is updated to reflect the current time of the change
  # a simple put will not do this (e.g. using auto_now) because we want to be
  # able to make changes without updating this updated field (see below when
  # increasing the viewCount property)
  def persist(self):
    self.updated = datetime.datetime.today();
    super(Diagram, self).save(); # don't remember why not use .put() here ?!
    # create a corresponding version with a copy of all fields
    version = DiagramVersion(
      parent         = self,
      diagram        = self,
      created        = self.created,
      owner          = self.owner,
      author         = self.author,
      name           = self.name,
      source         = self.source,
      width          = self.width,
      height         = self.height,
      description    = self.description,
      notes          = self.notes,
      tags           = self.tags,
      viewCount      = self.viewCount,
      editCount      = self.editCount,
      voteUpCount    = self.voteUpCount,
      voteDownCount  = self.voteDownCount,
      visibility     = self.visibility,
      status         = self.status
    );
    version.put();
    return self;

  # instance method to create a hash of relevant properties
  # this is used to send back to the Canvas2D client
  def to_hash(self):
    owner  = "An anonymous user";
    author = "An anonymous user";
    if self.owner  != None: owner  = self.owner.key().name();
    if self.author != None: author = self.author.key().name();
    return {
      "id"    : self.key().name(),
      "name"  : self.name,
      "descr" : self.description,
      "src"   : self.source,
      "width" : self.width,
      "height": self.height,
      "owner" : owner,
      "author": author,
      "notes" : self.notes,
      "views" : self.viewCount,
      "edits" : self.editCount,
      "auth"  : self.owner == get_account_for_current_user()
    };

  # instance method to increase the viewCount and save the diagram
  # this won't update the updated property
  def increase_view_count(self):
    self.viewCount += 1;
    self.put();
    return self;

class DiagramVersion(db.Model):
  diagram       = db.ReferenceProperty(Diagram, collection_name="versions")
  created       = db.DateTimeProperty()
  updated       = db.DateTimeProperty(auto_now_add=True)
  owner         = db.ReferenceProperty(Account)
  author        = db.ReferenceProperty(Account, collection_name="authored_versions")
  name          = db.StringProperty()
  source        = db.TextProperty()
  width         = db.IntegerProperty()
  height        = db.IntegerProperty()
  description   = db.TextProperty(default="")
  notes         = db.TextProperty(default="")
  tags          = db.StringListProperty()
  viewCount     = db.IntegerProperty(default=1)
  editCount     = db.IntegerProperty(default=1)
  voteUpCount   = db.IntegerProperty(default=0)
  voteDownCount = db.IntegerProperty(default=0)
  visibility    = db.StringProperty( default="public",
                                     choices=set(["public", "hidden"]) )
  status        = db.StringProperty( default="new",
                                     choices=set(["new", "updated", "ok", "nok"]) )
