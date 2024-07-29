from functools import wraps

from flask import request, jsonify

from .content_type_enum import ContentType
from ...controllers.response import Response


def check_content_type(content_type: ContentType):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_type != content_type.value:
                return jsonify(Response(success=False, data=f'Invalid content type. Expected {content_type.value}')
                               .serialize()), 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator
