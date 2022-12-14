from marshmallow import Schema, fields


# Parent Store Schema
class StorePlainSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


"""
To avoid getting:
ImportError: Cannot import name from partially initialized module (mostly due to a circular import)
import PlainItemSchema just before or within the class where it will be nested, since the below class formation is dependent on it.
You can use .item because they are in the same directory.
"""

from .item import ItemPlainSchema
from .user import UserPlainSchema

# Child Store Schema
class StoreSchema(StorePlainSchema):
    # from .item import ItemPlainSchema

    # Adding the user (owner) of the store to the store schema
    user_id = fields.Int(required=True, load_only=True)
    owner = fields.Nested(UserPlainSchema(exclude=("password","id")))

    # Adding the items of the store to the store schema
    items = fields.List(fields.Nested(ItemPlainSchema(only=("name","price"))), dump_only=True)
    # fields.List: returns a list of items in the store
    # fields.Nested: allows to nest a Schema (PlainItemSchema) inside a field


# Update Store Schema
class StoreUpdateSchema(Schema):
    name = fields.Str()
    user_id = fields.Int()


from .store import StoreSchema

class UserStoreItemSchema(UserPlainSchema):
    # adding stores of the user to the user schema
    stores = fields.List(fields.Nested(StoreSchema), dump_only=True)
