from marshmallow import Schema, fields, EXCLUDE, validates_schema, ValidationError


class ExportRequestDtoSchema(Schema):
    annotation_id = fields.Str(required=False)
    queue_id = fields.Str(required=False)

    class Meta:
        unknown = EXCLUDE

    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data.get('annotation_id') and not data.get('queue_id'):
            raise ValidationError('At least one of annotation_id or queue_id must be provided.')
