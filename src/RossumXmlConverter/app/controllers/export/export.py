from flask import Blueprint, jsonify, current_app, request
from flask_httpauth import HTTPBasicAuth

from app.controllers.export.export_request_dto import ExportRequestDto
from app.controllers.export.export_request_dto_schema import ExportRequestDtoSchema
from app.controllers.result_dto import ResultDto
from app.services.auth_service import verify_password as auth_verify_password
from app.utils.contenttype.content_type_decorator import check_content_type
from app.utils.contenttype.content_type_enum import ContentType
from app.utils.schema_validator import validate_request

moduleName = 'export'
export_bp = Blueprint(moduleName, __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    current_app.logger.info('Verifying user credentials')
    return auth_verify_password(username, password, current_app.config['USERNAME'], current_app.config['PASSWORD'])


@export_bp.route('/export', methods=['POST'])
@auth.login_required
@check_content_type(ContentType.APPLICATION_JSON)
def export_data():
    requestDto = validate_request(data=request.get_json(), schema_class=ExportRequestDtoSchema,
                                  dto_class=ExportRequestDto, logger=current_app.logger)
    current_app.logger.info('Exporting data')
    return jsonify(ResultDto(success=True).serialize()), 200
