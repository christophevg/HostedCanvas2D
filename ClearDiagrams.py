import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class ClearDiagrams(webapp.RequestHandler):
  def get(self):
    try:
      while True:
        q = db.GqlQuery("SELECT __key__ FROM Diagram")
        assert q.count();
        db.delete(q.fetch(200))
    except Exception, e:
        self.redirect('/')

application = webapp.WSGIApplication( [( '.*', ClearDiagrams )], debug = True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
