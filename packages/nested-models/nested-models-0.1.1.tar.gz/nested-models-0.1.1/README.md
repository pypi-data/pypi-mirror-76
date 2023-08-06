# nested-models

Nested models are serializeable objects that can be converted to various formats like JSON and YAML while providing functionality such as serialization/deserialization, cleaning, validation and  defaults values.

It also utilizes a Schema format that can restrict the fields that are serialized by the object.

Classes can be extended to add extra functionality and an encoder is provided that can be used with Django's JSON fields.

It also supports nesting Models inside of Models.

## Goal

The goal is to provide a basic object that can be sereialized/deserialized into various formats supported by Python.
