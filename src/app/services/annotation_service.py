﻿import xmltodict
from flask import current_app

from ..models.annotation import Annotation, Detail


class AnnotationService:
    @staticmethod
    def extract_annotation_data(export_queue_response_text: str, ) -> Annotation:
        # Consider validating the schema by the XDS file: https://elis.rossum.ai/api/static/api/queues_export.xsd
        data = xmltodict.parse(export_queue_response_text)
        annotation_dict = data['export']['results']['annotation']

        annotation = AnnotationService.__deserialize_annotation(annotation_dict)
        return annotation

    @staticmethod
    def __deserialize_annotation(data: dict) -> Annotation:
        content = data.get('content', {}).get('section', [])
        annotation_data = {}
        details = []

        for section in content:
            schema_id = section.get('@schema_id')
            datapoints = section.get('datapoint', [])

            match schema_id:
                case 'basic_info_section':
                    annotation_data['document_id'] = AnnotationService.__extract_datapoint(datapoints, 'document_id')
                    annotation_data['date_issue'] = AnnotationService.__extract_datapoint(datapoints, 'date_issue')
                    annotation_data['date_due'] = AnnotationService.__extract_datapoint(datapoints, 'date_due')

                case 'amounts_section':
                    annotation_data['amount_total'] = float(
                        AnnotationService.__extract_datapoint(datapoints, 'amount_total') or 0)
                    annotation_data['amount_total_base'] = float(
                        AnnotationService.__extract_datapoint(datapoints, 'amount_total_base') or 0)
                    annotation_data['currency'] = AnnotationService.__extract_datapoint(datapoints, 'currency')

                case 'vendor_section':
                    annotation_data['recipient_name'] = AnnotationService.__extract_datapoint(datapoints,
                                                                                              'recipient_name')
                    annotation_data['recipient_address'] = AnnotationService.__extract_datapoint(datapoints,
                                                                                                 'recipient_address')

                case 'line_items_section':
                    multivalue = section.get('multivalue', {})
                    tuples = multivalue.get('tuple', [])
                    if isinstance(tuples, dict):
                        tuples = [tuples]
                    for item in tuples:
                        datapoints = item.get('datapoint', [])
                        detail = Detail(
                            item_total_base=float(
                                AnnotationService.__extract_datapoint(datapoints, 'item_total_base') or 0),
                            item_quantity=int(AnnotationService.__extract_datapoint(datapoints, 'item_quantity') or 0),
                            item_description=AnnotationService.__extract_datapoint(datapoints, 'item_description')
                        )
                        details.append(detail)

                case 'other_section':
                    annotation_data['notes'] = AnnotationService.__extract_datapoint(datapoints, 'notes')

        annotation = Annotation(
            details=details,
            document_id=annotation_data.get('document_id'),
            date_issue=annotation_data.get('date_issue'),
            date_due=annotation_data.get('date_due'),
            amount_total=annotation_data.get('amount_total'),
            amount_total_base=annotation_data.get('amount_total_base'),
            currency=annotation_data.get('currency'),
            recipient_name=annotation_data.get('recipient_name'),
            recipient_address=annotation_data.get('recipient_address'),
            notes=annotation_data.get('notes')
        )

        return annotation

    @staticmethod
    def __extract_datapoint(datapoints, schema_id):
        if isinstance(datapoints, dict):
            datapoints = [datapoints]

        for dp in datapoints:
            if dp.get('@schema_id') == schema_id:
                return dp.get('#text')
        return None
