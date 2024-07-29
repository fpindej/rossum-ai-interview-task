import xmltodict
from flask import current_app

from ..annotation_converter.annotation import Annotation, Detail as AnnotationDetail
from ..annotation_converter.invoice import InvoiceRegisters, Invoices, Payable, Detail as InvoiceDetail


class AnnotationService:
    @staticmethod
    def extract_annotation_data(export_queue_response_text: str, annotation_id: str) -> Annotation:
        data = xmltodict.parse(export_queue_response_text)
        annotations = data['export']['results']['annotation']
        # This works only if there are multiple annotations in the response, otherwise it returns the annotation itself
        # Might be better to return the annotation itself if there is only one annotation
        # Let's keep it as is for now just to keep it simple for the sake of this example
        target_annotation = next((a for a in annotations if a['@url'].endswith(annotation_id)), None)

        if not target_annotation:
            current_app.logger.error(f"Annotation with id {annotation_id} not found")
            raise ValueError(f"Annotation with id {annotation_id} not found")

        annotations = AnnotationService.__deserialize_annotation(target_annotation)
        invoice_registers = AnnotationService.convert_annotation_to_invoice_registers(annotations)
        return annotations

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
                        detail = AnnotationDetail(
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

    @staticmethod
    def convert_annotation_to_invoice_registers(annotation: Annotation) -> InvoiceRegisters:
        # extract details from annotation
        details = [
            InvoiceDetail(Amount=detail.item_total_base, Quantity=detail.item_quantity, Notes=detail.item_description)
            for detail in annotation.details]
        payable = Payable(
            InvoiceNumber=annotation.document_id,
            InvoiceDate=annotation.date_issue,
            DueDate=annotation.date_due,
            TotalAmount=annotation.amount_total,
            Iban=annotation.iban,
            Amount=annotation.amount_total_base,
            Currency=annotation.currency,
            Vendor=annotation.recipient_name,
            VendorAddress=annotation.recipient_address,
            Details=details,
            Notes=annotation.notes
        )
        invoice = Invoices(Payable=payable)
        invoice_registers = InvoiceRegisters(Invoices=invoice)

        return invoice_registers
