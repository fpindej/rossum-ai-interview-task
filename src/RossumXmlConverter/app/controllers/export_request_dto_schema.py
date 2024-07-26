from marshmallow import Schema, fields


class ExportRequestDtoSchema(Schema):
    annotation_id = fields.Str(required=True)
    queue_id = fields.Str(required=True)
