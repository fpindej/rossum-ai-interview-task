from unittest.mock import patch

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_rossum_api():
    with patch('app.services.rossum_api_service.RossumApiService.export_queue') as mock_export_queue:
        mock_export_queue.return_value = type('obj', (object,), {'text': __get_rossum_api_xml_response()})
        yield mock_export_queue


@pytest.fixture
def mock_postbin_api():
    with patch('app.services.postbin_api_service.PostbinApiService.send_data') as mock_send_data:
        mock_send_data.return_value = None
        yield mock_send_data


def test_export_pipeline(client, mock_rossum_api, mock_postbin_api):
    # Send request to /export endpoint
    response = client.post('/export', json={
        'queue_id': '123',
        'annotation_id': '456'
    }, headers={
        'Authorization': 'Basic bXlVc2VyMTIzOnNlY3JldFNlY3JldA==',  # Base64 for user:password
        'Content-Type': 'application/json'
    })

    # Assert the response
    assert response.status_code == 200
    assert response.json['success'] == True


def __get_rossum_api_xml_response():
    return '''<?xml version="1.0" encoding="utf-8"?>
<export><results><annotation url="https://test.rossum.app/api/v1/annotations/456"><status>exported</status><arrived_at>2024-07-26T20:59:45.128212Z</arrived_at><exported_at>2024-07-29T00:36:40.177097Z</exported_at><document url="https://pindej.rossum.app/api/v1/documents/3898558"><file_name>[SAMPLE]_tax-invoice-uk_2.pdf</file_name><file>https://pindej.rossum.app/api/v1/documents/3898558/content</file></document><modifier url="https://pindej.rossum.app/api/v1/users/289033"><username>rossum.ai@mail.pindej.cz</username></modifier><schema url="https://pindej.rossum.app/api/v1/schemas/1260807"></schema><metadata></metadata><content><section schema_id="basic_info_section"><datapoint rir_confidence="0.9948073504881643" schema_id="document_id" type="string">123456789</datapoint><datapoint rir_confidence="0.9910721362327274" schema_id="date_issue" type="date">2018-07-27</datapoint><datapoint rir_confidence="0.9012867778661668" schema_id="document_type" type="enum">tax_invoice</datapoint><datapoint rir_confidence="0.9761604367324285" schema_id="language" type="enum">eng</datapoint></section><section schema_id="amounts_section"><datapoint rir_confidence="0.9998104575276374" schema_id="amount_total_base" type="number">9.325</datapoint><datapoint rir_confidence="0.9998496732115746" schema_id="amount_total_tax" type="number">1.865</datapoint><datapoint rir_confidence="0.995746775351016" schema_id="amount_total" type="number">11.190</datapoint><datapoint rir_confidence="0.9937709052630528" schema_id="amount_due" type="number">11.190</datapoint><datapoint rir_confidence="0.9565113684094471" schema_id="currency" type="enum">gbp</datapoint><multivalue schema_id="tax_details"></multivalue></section><section schema_id="vendor_section"><datapoint rir_confidence="0.9252046239536199" schema_id="sender_name" type="string">ROSSUM</datapoint><datapoint rir_confidence="0.9521198230968534" schema_id="sender_address" type="string">1234 North Street
London SW7 2AP UK</datapoint><datapoint schema_id="sender_vat_id" type="string"></datapoint><datapoint schema_id="sender_ic" type="string"></datapoint><datapoint rir_confidence="0.9209103366303653" schema_id="recipient_name" type="string">ABC Company</datapoint><datapoint rir_confidence="0.316026750034617" schema_id="recipient_address" type="string">7890 South Street
Manchester M1 1BE UK
+44 616
5678</datapoint><datapoint schema_id="recipient_ic" type="string"></datapoint></section><section schema_id="payment_info_section"><datapoint schema_id="account_num" type="string"></datapoint><datapoint schema_id="bank_num" type="string"></datapoint></section><section schema_id="line_items_section"><multivalue schema_id="line_items"><tuple schema_id="line_item"><datapoint rir_confidence="0.8392156958580017" schema_id="item_quantity" type="number">150</datapoint><datapoint schema_id="item_code" type="string"></datapoint><datapoint rir_confidence="0.8058823645114899" schema_id="item_description" type="string">Item 1</datapoint><datapoint rir_confidence="0.6764706075191498" schema_id="item_amount_base" type="number">15</datapoint><datapoint rir_confidence="0.7627451121807098" schema_id="item_total_base" type="number">2250</datapoint></tuple><tuple schema_id="line_item"><datapoint rir_confidence="0.8509804010391235" schema_id="item_quantity" type="number">100</datapoint><datapoint schema_id="item_code" type="string"></datapoint><datapoint rir_confidence="0.8313725590705872" schema_id="item_description" type="string">Item 2</datapoint><datapoint rir_confidence="0.7137255072593689" schema_id="item_amount_base" type="number">30</datapoint><datapoint rir_confidence="0.800000011920929" schema_id="item_total_base" type="number">3000</datapoint></tuple><tuple schema_id="line_item"><datapoint rir_confidence="0.843137264251709" schema_id="item_quantity" type="number">35</datapoint><datapoint schema_id="item_code" type="string"></datapoint><datapoint rir_confidence="0.8450980484485626" schema_id="item_description" type="string">Item 3</datapoint><datapoint rir_confidence="0.7568627595901489" schema_id="item_amount_base" type="number">45</datapoint><datapoint rir_confidence="0.8137255012989044" schema_id="item_total_base" type="number">1575</datapoint></tuple><tuple schema_id="line_item"><datapoint rir_confidence="0.843137264251709" schema_id="item_quantity" type="number">25</datapoint><datapoint schema_id="item_code" type="string"></datapoint><datapoint rir_confidence="0.8372549116611481" schema_id="item_description" type="string">Item 4</datapoint><datapoint rir_confidence="0.6666666865348816" schema_id="item_amount_base" type="number">100</datapoint><datapoint rir_confidence="0.8019607961177826" schema_id="item_total_base" type="number">2500</datapoint></tuple></multivalue></section><section schema_id="other_section"><datapoint schema_id="notes" type="string"></datapoint></section></content><automated>false</automated><modified_at>2024-07-29T00:36:36.077217Z</modified_at><assigned_at>2024-07-29T00:36:34.825627Z</assigned_at></annotation><annotation url="https://pindej.rossum.app/api/v1/annotations/3425119"><status>exported</status><arrived_at>2024-07-26T20:59:45.128212Z</arrived_at><exported_at>2024-07-28T21:58:21.773013Z</exported_at><document url="https://pindej.rossum.app/api/v1/documents/3898553"><file_name>[SAMPLE]_tax-invoice-uk.pdf</file_name><file>https://pindej.rossum.app/api/v1/documents/3898553/content</file></document><modifier url="https://pindej.rossum.app/api/v1/users/289033"><username>rossum.ai@mail.pindej.cz</username></modifier><schema url="https://pindej.rossum.app/api/v1/schemas/1260807"></schema><metadata></metadata><content><section schema_id="basic_info_section"><datapoint rir_confidence="0.9999294281005859" schema_id="document_id" type="string">000957537</datapoint><datapoint rir_confidence="0.9998705983161926" schema_id="date_issue" type="date">2019-03-01</datapoint><datapoint rir_confidence="0.999998927116394" schema_id="document_type" type="enum">tax_invoice</datapoint><datapoint rir_confidence="0.9999998807907104" schema_id="language" type="enum">eng</datapoint></section><section schema_id="amounts_section"><datapoint rir_confidence="0.9088642001152039" schema_id="amount_total_base" type="number">1682.00</datapoint><datapoint rir_confidence="0.9998549222946167" schema_id="amount_total_tax" type="number">336.40</datapoint><datapoint rir_confidence="0.9982389211654663" schema_id="amount_total" type="number">2018.40</datapoint><datapoint rir_confidence="0.9971195459365845" schema_id="amount_due" type="number">2018.40</datapoint><datapoint rir_confidence="1.0" schema_id="currency" type="enum">gbp</datapoint><multivalue schema_id="tax_details"></multivalue></section><section schema_id="vendor_section"><datapoint rir_confidence="0.8403704762458801" schema_id="sender_name" type="string">Good Lock &amp; Safe Services</datapoint><datapoint rir_confidence="0.5714425444602966" schema_id="sender_address" type="string">762 Lovewell Street
Newcastle Upon Tyne
NE1 0SG</datapoint><datapoint rir_confidence="0.5000503063201904" schema_id="sender_vat_id" type="string">71 952 744286</datapoint><datapoint schema_id="sender_ic" type="string"></datapoint><datapoint rir_confidence="0.973338782787323" schema_id="recipient_name" type="string">Hiltop Hamlet</datapoint><datapoint rir_confidence="0.9217020869255066" schema_id="recipient_address" type="string">PO Box 17320
HARDEN
BD16 1BU</datapoint><datapoint schema_id="recipient_ic" type="string"></datapoint></section><section schema_id="payment_info_section"><datapoint rir_confidence="0.9795304536819458" schema_id="account_num" type="string">505736372</datapoint><datapoint rir_confidence="0.9195305109024048" schema_id="bank_num" type="string">80-37-95</datapoint></section><section schema_id="line_items_section"><multivalue schema_id="line_items"><tuple schema_id="line_item"><datapoint rir_confidence="0.9215686321258545" schema_id="item_quantity" type="number">100</datapoint><datapoint rir_confidence="0.6843137443065643" schema_id="item_code" type="string">Skeleton key</datapoint><datapoint rir_confidence="0.8699346482753754" schema_id="item_description" type="string">GMK keys stamping 132 issue 42-40</datapoint><datapoint rir_confidence="0.7843137383460999" schema_id="item_amount_base" type="number">16.82</datapoint><datapoint rir_confidence="0.7176470756530762" schema_id="item_total_base" type="number">1682.00</datapoint></tuple></multivalue></section><section schema_id="other_section"><datapoint schema_id="notes" type="string"></datapoint></section></content><automated>false</automated><modified_at>2024-07-26T21:52:04.577442Z</modified_at><assigned_at>2024-07-26T21:51:46.429448Z</assigned_at></annotation></results><pagination><next></next><previous></previous><total>2</total><total_pages>1</total_pages></pagination></export>'''
