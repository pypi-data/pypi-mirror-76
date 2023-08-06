'''
Nested models are serializeable objects that can be converted to formats like JSON and YAML while providing functionality such as deserialization, cleaning and dynameic defaults.


Examples...

class DataMeta(NestedModel):
    fields = ['uuid']


class PathDraft(NestedModel):
    fields = ['meta', 'name', 'tag'] 
    tag = "stuff"

    def deserialize_meta(self, meta):
        return self.to_object(meta, DataMeta)

> draft.to_dict()
{'meta': {'version': 'v1.0'}, 'name': 'bob', 'tag': 'stuff'}
'''

class ValidationError(Exception):
    pass

class NestedModel():
    '''
    Serializeable objects that can be used to validate dictionary structures
    and go to/from JSON or YAML (or anything that can serialize a dict).

    TODO: Add support for processing objects in lists?  Might best be handled by the serialize/deserialize method.
    TODO: Add support for processing objects nested in dicts
    TODO: Add Validate Method(s)
    '''

    # Allowed Fields
    fields = []          # This controls what attributes are allowed in the serializer

    def __init__(self, **kwargs):
        for key in self.fields:       # Check for all fields
            if key in kwargs:         # If a value is being passed in, use that
                deserializer = "deserialize_{}".format(key)
                if hasattr(self, deserializer):
                    value = getattr(self, deserializer)(kwargs[key])
                else:
                    value = kwargs[key]
                setattr(self, key, value)
            else:                       # If it was not passed in but there is a default setting use that
                default = "default_{}".format(key)
                if hasattr(self, default):
                    value = getattr(self, default)()
                    setattr(self, key, value)

    def __iter__(self):
        for key in self.fields:                    # Attributes to return in the dict
            if hasattr(self, key):
                processor = "serialize_{}".format(key)
                value = getattr(self, key)

                if hasattr(self, processor):
                    value = getattr(self, processor)(value)

                if hasattr(value, "to_dict"):
                    value = value.to_dict()
                    
                # Add processor here for any child objects
                yield (key, value)

    def to_object(self, value, obj):
        if isinstance(value, dict):        # Check to see if the input is a Dict, and process if needed
            return obj(**value)
        
        return value

    def clean(self):
        for key in [k for k in self.fields if k in self.__dict__]:      # Find all the keys that are on the object that are allowed by the NestedModel Class
            clean_method = "clean_{}".format(key)

            if hasattr(self, clean_method):          # Calls the clean_method if it exists for the attribute
                getattr(self, clean_method)()

            if hasattr(self.__dict__[key], "clean"):    # If it has a clean() method call that on any children
                self.__dict__[key].clean()

    def to_dict(self):
        return dict(self)

    def validate(self):
        for key in self.fields:       # Check for all field validators.  Expected result is a true/false
            validator = "validate_{}".format(key)
            if hasattr(self, validator):
                getattr(self, validator)()      # Expected behavior is to raise a validation error if it fails
