from apiflask.schemas import Schema
from apiflask import fields

"""
    class Tasks:
        id int
        content str
        date_added datetime
        is_completed boolean
"""

# schema is either outputting and inputting data used for serializing fields in the database

class TaskOutputSchema(Schema):
    id = fields.Integer()
    content =  fields.String()
    date_added = fields.DateTime()
    is_completed = fields.Boolean()


class TaskCreateSchema(Schema):
    content =  fields.String(required=True)


class TaskUpdateSchema(Schema):
    content =  fields.String(required=True)
    is_completed = fields.Boolean(required=True)

    