from .annotation.export_annotation import ExportAnnotation
from .invoice.invoice_registers import InvoiceRegisters, Detail, Payable, Invoices


class AnnotationConverter:
    @staticmethod
    def convert(export_annotation: ExportAnnotation) -> InvoiceRegisters:
        export_payable = export_annotation.Invoices.Payable

        invoice_details = [
            Detail(
                Amount=detail.Amount,
                Quantity=detail.Quantity,
                Notes=detail.Notes,
                AccountId=detail.AccountId
            ) for detail in export_payable.Details
        ]

        invoice_payable = Payable(
            InvoiceNumber=export_payable.InvoiceNumber,
            InvoiceDate=export_payable.InvoiceDate,
            DueDate=export_payable.DueDate,
            TotalAmount=export_payable.TotalAmount,
            Iban=export_payable.Iban,
            Amount=export_payable.Amount,
            Currency=export_payable.Currency,
            Vendor=export_payable.Vendor,
            VendorAddress=export_payable.VendorAddress,
            Details=invoice_details,
            Notes=export_payable.Notes
        )

        invoices = Invoices(Payable=invoice_payable)
        invoice_registers = InvoiceRegisters(Invoices=invoices)

        return invoice_registers
