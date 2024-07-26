from functools import wraps

from flask import request, jsonify

from ...controllers.result_dto import ResultDto
from .content_type_enum import ContentType


def check_content_type(content_type: ContentType):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_type != content_type.value:
                return jsonify(ResultDto(success=False, data=f'Invalid content type. Expected {content_type.value}')
                               .serialize()), 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator
