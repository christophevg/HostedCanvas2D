from google.appengine.api import namespace_manager

import os

def namespace_manager_default_namespace_for_request():
  return os.environ['SERVER_NAME']
