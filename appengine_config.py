from google.appengine.api import namespace_manager

def namespace_manager_default_namespace_for_request():
  import os
  return os.environ['SERVER_NAME']
