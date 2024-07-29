from marshmallow import ValidationError

from ..controllers.response import Response


def validate_request(data, schema_class, dto_class, logger):
    try:
        logger.info('Validating request data')
        validated_data = schema_class().load(data)
    except ValidationError as err:
        logger.error(f'Validation error: {err.messages}')
        return None, Response(success=False, data=err.messages)
    return dto_class.deserialize(validated_data), None
