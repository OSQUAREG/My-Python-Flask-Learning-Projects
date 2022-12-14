from marshmallow import Schema, fields


# Parent Store Schema
class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

# Parent Item Schema
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

# Child Store Schema
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    # fields.List: returns a list of items in the store
    # fields.Nested: allows to nest a Schema (PlainItemSchema) inside a field

# Update Store Schema
class UpdateStoreSchema(Schema):
    name = fields.Str()

# Child Item Schema
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    # fields.Nested: allows to nest a Schemas (PlainStoreSchema) inside a field

# Update Item Schema
class UpdateItemSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()