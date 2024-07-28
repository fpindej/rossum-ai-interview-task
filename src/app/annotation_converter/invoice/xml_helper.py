import xml.etree.ElementTree as ElementTree

from .invoice_registers import InvoiceRegisters


def to_xml(data: InvoiceRegisters) -> str:
    def create_element(tag, text=None):
        element = ElementTree.Element(tag)
        if text:
            element.text = str(text)
        return element

    def serialize_detail(detail):
        detail_element = create_element('Detail')
        detail_element.append(create_element('Amount', detail.Amount))
        detail_element.append(create_element('AccountId', detail.AccountId))
        detail_element.append(create_element('Quantity', detail.Quantity))
        detail_element.append(create_element('Notes', detail.Notes))
        return detail_element

    def serialize_payable(payable):
        payable_element = create_element('Payable')
        payable_element.append(create_element('InvoiceNumber', payable.InvoiceNumber))
        payable_element.append(create_element('InvoiceDate', payable.InvoiceDate))
        payable_element.append(create_element('DueDate', payable.DueDate))
        payable_element.append(create_element('TotalAmount', payable.TotalAmount))
        payable_element.append(create_element('Notes', payable.Notes))
        payable_element.append(create_element('Iban', payable.Iban))
        payable_element.append(create_element('Amount', payable.Amount))
        payable_element.append(create_element('Currency', payable.Currency))
        payable_element.append(create_element('Vendor', payable.Vendor))
        payable_element.append(create_element('VendorAddress', payable.VendorAddress))

        details_element = create_element('Details')
        for detail in payable.Details:
            details_element.append(serialize_detail(detail))
        payable_element.append(details_element)

        return payable_element

    def serialize_invoices(invoices):
        invoices_element = create_element('Invoices')
        invoices_element.append(serialize_payable(invoices.Payable))
        return invoices_element

    def serialize_invoice_registers(invoice_registers):
        root = create_element('InvoiceRegisters')
        root.append(serialize_invoices(invoice_registers.Invoices))
        return root

    root_element = serialize_invoice_registers(data)
    return ElementTree.tostring(root_element, encoding='utf-8', xml_declaration=True).decode('utf-8')
