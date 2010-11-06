from google.appengine.ext import db

class Diagram(db.Model):
  owner         = db.UserProperty(auto_current_user_add=True)
  author        = db.UserProperty(auto_current_user=True)
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

class Account(db.Model):
  user = db.UserProperty(auto_current_user=True)
