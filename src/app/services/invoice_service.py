import base64

import xmltodict

from app.annotation_converter.annotation import Annotation
from app.annotation_converter.invoice import InvoiceRegisters, Invoices, Detail, Payable


class InvoiceService:
    def get_base64_invoice(self, annotation: Annotation) -> base64:
        invoice_registers = self.convert_annotation_to_invoice_registers(annotation)
        invoice_registers_xml = self.convert_invoice_registers_to_xml(invoice_registers)
        invoice_registers_xml_base64 = self.convert_invoice_registers_xml_to_base64(invoice_registers_xml)

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
