from functools import wraps

from flask import request, jsonify, current_app
from marshmallow import ValidationError

from app.content_type_enum import ContentType
from app.controllers.result_dto import ResultDto


def check_content_type(content_type: ContentType):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_type != content_type.value:
                return jsonify({'success': False, 'error': f'Content-Type must be {content_type.value}'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_request(schema_class):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            schema = schema_class()
            try:
                current_app.logger.info('Validating request data')
                _ = schema.load(data)
            except ValidationError as err:
                current_app.logger.error(f'Validation error: {err.messages}')
                return jsonify((ResultDto(success=False, data=err.messages).serialize())), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
