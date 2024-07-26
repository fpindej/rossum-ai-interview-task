﻿from flask import jsonify
from marshmallow import ValidationError

from app.controllers.result_dto import ResultDto


def validate_request(data, schema_class, dto_class, logger):
    schema = schema_class(partial=True)
    try:
        logger.info('Validating request data')
        validated_data = schema.load(data)
    except ValidationError as err:
        logger.error(f'Validation error: {err.messages}')
        return jsonify((ResultDto(success=False, data=err.messages).serialize())), 400
    return dto_class.deserialize(validated_data)
