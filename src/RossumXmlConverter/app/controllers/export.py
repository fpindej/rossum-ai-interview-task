from flask import Blueprint, jsonify, current_app
from flask_httpauth import HTTPBasicAuth

from app.content_type_enum import ContentType
from app.controllers.export_request_dto_schema import ExportRequestDtoSchema
from app.controllers.result_dto import ResultDto
from app.controllers.validation_decorator import validate_request, check_content_type
from app.services.auth_service import verify_password as auth_verify_password

moduleName = 'export'
export_bp = Blueprint(moduleName, __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    current_app.logger.info('Verifying user credentials')
    return auth_verify_password(username, password)


@export_bp.route('/export', methods=['POST'])
@auth.login_required
@check_content_type(ContentType.APPLICATION_JSON)
@validate_request(ExportRequestDtoSchema)
def export_data():
    current_app.logger.info('Exporting data')
    return jsonify(ResultDto(success=True).serialize()), 200
