from google.appengine.ext import db

class Diagram(db.Model):
  author   = db.UserProperty()
  title    = db.StringProperty()
  source   = db.StringProperty(multiline=True)
  created  = db.DateTimeProperty(auto_now_add=True)
