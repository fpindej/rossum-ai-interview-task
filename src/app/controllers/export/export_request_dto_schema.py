from marshmallow import Schema, fields, EXCLUDE


class ExportRequestDtoSchema(Schema):
    annotation_id = fields.Str(required=True)
    queue_id = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE
