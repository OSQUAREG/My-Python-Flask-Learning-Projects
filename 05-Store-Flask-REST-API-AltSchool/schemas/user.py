from marshmallow import Schema, fields


class UserPlainSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


from .store import StorePlainSchema

class UserSchema(UserPlainSchema):
    # adding stores of the user to the user schema
    stores = fields.List(fields.Nested(StorePlainSchema), dump_only=True)


class UserUpdateSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str(required=True)
