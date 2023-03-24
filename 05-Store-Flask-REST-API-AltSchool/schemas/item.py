from marshmallow import Schema, fields


# Parent Item Schema
class ItemPlainSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


"""
To avoid getting:
ImportError: Cannot import name from partially initialized module (mostly due to a circular import)
import PlainStoreSchema just before or within the class where it will be nested, since the below class formation is dependent on it.
You can use .store because they are in the same directory.
"""

from .store import StorePlainSchema

# Child Item Schema
class ItemSchema(ItemPlainSchema):
    # from .store import PlainStoreSchema

    # Adding the store of the item to the item schema
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(StorePlainSchema(only=("name",)), dump_only=True)
    # fields.Nested: allows to nest a Schemas (PlainStoreSchema) inside a field


# Update Item Schema
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
