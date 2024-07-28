import xml.etree.ElementTree as ElementTree

from .export_annotation import ExportAnnotation, Detail, Payable, Document, Modifier, Annotation, Invoices


def from_xml(xml_str: str) -> ExportAnnotation:
    root = ElementTree.fromstring(xml_str)

    def get_text(element, tag):
        child = element.find(tag)
        return child.text if child is not None else None

    def parse_detail(detail_element):
        return Detail(
            Amount=float(get_text(detail_element, 'item_amount')),
            Quantity=int(get_text(detail_element, 'item_quantity')),
            Notes=get_text(detail_element, 'item_description')
        )

    def parse_payable(payable_element):
        details = []
        for tuple_element in payable_element.findall(".//tuple"):
            details.append(parse_detail(tuple_element))

        return Payable(
            InvoiceNumber=get_text(payable_element, ".//datapoint[@schema_id='invoice_id']"),
            InvoiceDate=get_text(payable_element, ".//datapoint[@schema_id='date_issue']"),
            DueDate=get_text(payable_element, ".//datapoint[@schema_id='date_due']"),
            TotalAmount=float(get_text(payable_element, ".//datapoint[@schema_id='amount_total']")),
            Iban=get_text(payable_element, ".//datapoint[@schema_id='iban']"),
            Amount=float(get_text(payable_element, ".//datapoint[@schema_id='amount_total_tax']")),
            Currency=get_text(payable_element, ".//datapoint[@schema_id='currency']"),
            Vendor=get_text(payable_element, ".//datapoint[@schema_id='sender_name']"),
            VendorAddress=get_text(payable_element, ".//datapoint[@schema_id='sender_address']"),
            Details=details
        )

    def parse_document(document_element):
        return Document(
            file_name=get_text(document_element, "file_name"),
            file_url=get_text(document_element, "file")
        )

    def parse_modifier(modifier_element):
        return Modifier(
            username=get_text(modifier_element, "username")
        )

    def parse_annotation(annotation_element):
        document_element = annotation_element.find("document")
        modifier_element = annotation_element.find("modifier")

        return Annotation(
            status=get_text(annotation_element, "status"),
            arrived_at=get_text(annotation_element, "arrived_at"),
            exported_at=get_text(annotation_element, "exported_at"),
            document=parse_document(document_element),
            modifier=parse_modifier(modifier_element),
            automated=annotation_element.find("automated").text.lower() == 'true',
            modified_at=get_text(annotation_element, "modified_at"),
            assigned_at=get_text(annotation_element, "assigned_at")
        )

    annotation = root.find(".//annotation")
    payable = parse_payable(annotation)
    annotations = [parse_annotation(annotation)]

    invoices = Invoices(Payable=payable)
    invoice_registers = ExportAnnotation(Invoices=invoices, Annotations=annotations)

    return invoice_registers
