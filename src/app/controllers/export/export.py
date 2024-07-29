from flask import Blueprint, jsonify, current_app, request
from flask_httpauth import HTTPBasicAuth

from .export_request_dto import ExportRequestDto
from .export_request_dto_schema import ExportRequestDtoSchema
from ..response import Response
from ...services.annotation_service import AnnotationService
from ...services.auth_service import verify_password as auth_verify_password
from ...services.invoice_service import InvoiceService
from ...services.postbin_api_service import PostbinApiService
from ...services.rossum_api_service import RossumApiService
from ...utils.contenttype.content_type_decorator import check_content_type
from ...utils.contenttype.content_type_enum import ContentType
from ...utils.schema_validator import validate_request

moduleName = 'export'
export_bp = Blueprint(moduleName, __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    current_app.logger.info('Verifying user credentials')
    return auth_verify_password(username, password, current_app.config['EXPORT_USERNAME'],
                                current_app.config['EXPORT_PASSWORD'])


@export_bp.route('/export', methods=['POST'])
@auth.login_required
@check_content_type(ContentType.APPLICATION_JSON)
def export_data():
    request_dto, error_response = validate_request(data=request.get_json(), schema_class=ExportRequestDtoSchema,
                                                   dto_class=ExportRequestDto, logger=current_app.logger)

    if error_response:
        return jsonify(error_response.serialize()), 400

    try:
        rossum_api_service = RossumApiService()
        export_queue_response = rossum_api_service.export_queue(queue_id=request_dto.queue_id,
                                                                annotation_id=request_dto.annotation_id)
    except Exception as e:
        current_app.logger.error(f'Failed to export data: {e}')
        return jsonify(Response(success=False).serialize()), 500

    # For the sake of simplicity I'm relying on a happy path here
    annotation = AnnotationService.extract_annotation_data(export_queue_response.text)
    invoice_registers_xml_base64 = InvoiceService.get_base64_invoice(annotation)

    try:
        postbin_api_service = PostbinApiService()
        postbin_api_service.send_data(annotation_id=request_dto.annotation_id, xml_base64=invoice_registers_xml_base64)
    except Exception as e:
        current_app.logger.error(f'Failed to send data: {e}')
        return jsonify(Response(success=False).serialize()), 500

    return jsonify(Response(success=True).serialize()), 200
