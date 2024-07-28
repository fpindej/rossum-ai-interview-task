import xmltodict

from app.annotation_converter.invoice.invoice import InvoiceRegisters, Invoices, Payable


def extract_datapoint(datapoints, schema_id):
    for dp in datapoints:
        if dp.get('@schema_id') == schema_id:
            return dp.get('#text')
    return None


def is_list(datapoints):
    return isinstance(datapoints, list)


def create_invoice_registers(data: dict) -> InvoiceRegisters:
    content = data.get('content', {}).get('section', [])
    invoice_data = {}

    for section in content:
        schema_id = section.get('@schema_id')
        datapoints = section.get('datapoint', [])

        match schema_id:
            case 'basic_info_section':
                invoice_data['InvoiceNumber'] = extract_datapoint(datapoints, 'document_id')
                invoice_data['InvoiceDate'] = extract_datapoint(datapoints, 'date_issue')
                invoice_data['DueDate'] = extract_datapoint(datapoints, 'date_due')

            case 'amounts_section':
                invoice_data['TotalAmount'] = float(extract_datapoint(datapoints, 'amount_total') or 0)
                invoice_data['Amount'] = float(extract_datapoint(datapoints, 'amount_total_base') or 0)
                invoice_data['Currency'] = extract_datapoint(datapoints, 'currency')

            case 'vendor_section':
                invoice_data['Vendor'] = extract_datapoint(datapoints, 'recipient_name')
                invoice_data['VendorAddress'] = extract_datapoint(datapoints, 'recipient_address')

            case 'other_section':
                if isinstance(datapoints, list):
                    invoice_data['Notes'] = extract_datapoint(datapoints, 'notes')

    payable = Payable(
        InvoiceNumber=invoice_data.get('InvoiceNumber'),
        InvoiceDate=invoice_data.get('InvoiceDate'),
        DueDate=invoice_data.get('DueDate'),
        TotalAmount=invoice_data.get('TotalAmount'),
        Notes=invoice_data.get('Notes'),
        Iban=invoice_data.get('Iban'),
        Amount=invoice_data.get('Amount'),
        Currency=invoice_data.get('Currency'),
        Vendor=invoice_data.get('Vendor'),
        VendorAddress=invoice_data.get('VendorAddress'),
        Details=None  # Details will be handled later
    )

    invoices = Invoices(Payable=payable)
    invoice_registers = InvoiceRegisters(Invoices=invoices)

    return invoice_registers


def from_xml(xml_str: str, annotation_id: str):
    data = xmltodict.parse(xml_str)
    annotations = data['export']['results']['annotation']
    target_annotation = next((a for a in annotations if a['@url'].endswith(annotation_id)), None)

    if not target_annotation:
        raise ValueError(f"Annotation with id {annotation_id} not found")

    invoice_registers = create_invoice_registers(target_annotation)

    invoice_registers_xml = xmltodict.unparse(invoice_registers.to_dict(), pretty=True)
    return invoice_registers_xml
