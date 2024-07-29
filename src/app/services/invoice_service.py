import base64

import xmltodict

from app.models.annotation import Annotation
from app.models.invoice import InvoiceRegisters, Invoices, Detail, Payable


class InvoiceService:
    @staticmethod
    def get_base64_invoice(annotation: Annotation) -> str:
        invoice_registers = InvoiceService.convert_annotation_to_invoice_registers(annotation)
        invoice_registers_xml = InvoiceService.convert_invoice_registers_to_xml(invoice_registers)
        invoice_registers_xml_base64 = InvoiceService.convert_invoice_registers_xml_to_base64(invoice_registers_xml)

        return invoice_registers_xml_base64

    @staticmethod
    def convert_annotation_to_invoice_registers(annotation: Annotation) -> InvoiceRegisters:
        # extract details from annotation
        details = [
            Detail(Amount=detail.item_total_base, Quantity=detail.item_quantity, Notes=detail.item_description)
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

    @staticmethod
    def convert_invoice_registers_to_xml(invoice_registers: InvoiceRegisters) -> str:
        return xmltodict.unparse(invoice_registers.to_dict(), pretty=True)

    @staticmethod
    def convert_invoice_registers_xml_to_base64(invoice_registers_xml: str) -> base64:
        return base64.b64encode(invoice_registers_xml.encode('utf-8')).decode('utf-8')
