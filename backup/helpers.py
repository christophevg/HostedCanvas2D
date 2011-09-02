from google.appengine.api import datastore

def create_foreign_key(kind, namespace=None, key_is_id=False):
  """A method to make one-level Key objects.

  These are typically used in ReferenceProperty in Python, where the reference
  value is a key with kind (or model) name name.

  This helper method does not support keys with parents. Use create_deep_key
  instead to create keys with parents.

  Args:
    kind: The kind name of the reference as a string.
    namespace: The namespace of the reference
    key_is_id: If true, convert the key into an integer to be used as an id.
      If false, leave the key in the input format (typically a string).

  Returns:
    Single argument method which parses a value into a Key of kind entity_kind.
    
  Original code take from transform.py
  Added namespace support to allow creating foreign keys to other namespaces
  Added support for empty values
  """

  def generate_foreign_key_lambda(value):
    if value is None or value == '' or value == []:
      return None

    if key_is_id:
      value = int(value)

    return datastore.Key.from_path( kind, value, namespace=namespace )

  return generate_foreign_key_lambda
