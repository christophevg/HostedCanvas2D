from google.appengine.ext import db
from Account import Account

class Diagram(db.Model):
  owner         = db.ReferenceProperty(Account, collection_name="owner")
  author        = db.ReferenceProperty(Account, collection_name="author")
  name          = db.StringProperty()
  source        = db.TextProperty()
  width         = db.IntegerProperty()
  height        = db.IntegerProperty()
  description   = db.TextProperty(default="")
  tags          = db.StringListProperty()
  created       = db.DateTimeProperty(auto_now_add=True)
  updated       = db.DateTimeProperty(auto_now=True)
  viewCount     = db.IntegerProperty(default=1)
  editCount     = db.IntegerProperty(default=1)
  voteUpCount   = db.IntegerProperty(default=0)
  voteDownCount = db.IntegerProperty(default=0)
  notes         = db.TextProperty(default="")
  visibility    = db.StringProperty( default="public",
                                     choices=set(["public", "hidden"]) )
  status        = db.StringProperty( default="new",
                                     choices=set(["new", "updated", "ok", "nok"]) )
