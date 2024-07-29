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
    return '''<?xml version="1.0" encoding="utf-8"?><export><results><annotation url="https://test.rossum.app/api/v1/annotations/456"><status>exported</status><arrived_at>2024-07-26T20:59:45.128212Z</arrived_at><exported_at>2024-07-28T21:58:21.773013Z</exported_at><document url="https://test.rossum.app/api/v1/documents/3898553"><file_name>[SAMPLE]_tax-invoice-uk.pdf</file_name><file>https://test.rossum.app/api/v1/documents/3898553/content</file></document><modifier url="https://test.rossum.app/api/v1/users/289033"><username>rossum.ai@mail.test.cz</username></modifier><schema url="https://test.rossum.app/api/v1/schemas/1260807"></schema><metadata></metadata><content><section schema_id="basic_info_section"><datapoint rir_confidence="0.9999294281005859" schema_id="document_id" type="string">000957537</datapoint><datapoint rir_confidence="0.9998705983161926" schema_id="date_issue" type="date">2019-03-01</datapoint><datapoint rir_confidence="0.999998927116394" schema_id="document_type" type="enum">tax_invoice</datapoint><datapoint rir_confidence="0.9999998807907104" schema_id="language" type="enum">eng</datapoint></section><section schema_id="amounts_section"><datapoint rir_confidence="0.9088642001152039" schema_id="amount_total_base" type="number">1682.00</datapoint><datapoint rir_confidence="0.9998549222946167" schema_id="amount_total_tax" type="number">336.40</datapoint><datapoint rir_confidence="0.9982389211654663" schema_id="amount_total" type="number">2018.40</datapoint><datapoint rir_confidence="0.9971195459365845" schema_id="amount_due" type="number">2018.40</datapoint><datapoint rir_confidence="1.0" schema_id="currency" type="enum">gbp</datapoint><multivalue schema_id="tax_details"></multivalue></section><section schema_id="vendor_section"><datapoint rir_confidence="0.8403704762458801" schema_id="sender_name" type="string">Good Lock &amp; Safe Services</datapoint><datapoint rir_confidence="0.5714425444602966" schema_id="sender_address" type="string">762 Lovewell Street
Newcastle Upon Tyne
NE1 0SG</datapoint><datapoint rir_confidence="0.5000503063201904" schema_id="sender_vat_id" type="string">71 952 744286</datapoint><datapoint schema_id="sender_ic" type="string"></datapoint><datapoint rir_confidence="0.973338782787323" schema_id="recipient_name" type="string">Hiltop Hamlet</datapoint><datapoint rir_confidence="0.9217020869255066" schema_id="recipient_address" type="string">PO Box 17320
HARDEN
BD16 1BU</datapoint><datapoint schema_id="recipient_ic" type="string"></datapoint></section><section schema_id="payment_info_section"><datapoint rir_confidence="0.9795304536819458" schema_id="account_num" type="string">505736372</datapoint><datapoint rir_confidence="0.9195305109024048" schema_id="bank_num" type="string">80-37-95</datapoint></section><section schema_id="line_items_section"><multivalue schema_id="line_items"><tuple schema_id="line_item"><datapoint rir_confidence="0.9215686321258545" schema_id="item_quantity" type="number">100</datapoint><datapoint rir_confidence="0.6843137443065643" schema_id="item_code" type="string">Skeleton key</datapoint><datapoint rir_confidence="0.8699346482753754" schema_id="item_description" type="string">GMK keys stamping 132 issue 42-40</datapoint><datapoint rir_confidence="0.7843137383460999" schema_id="item_amount_base" type="number">16.82</datapoint><datapoint rir_confidence="0.7176470756530762" schema_id="item_total_base" type="number">1682.00</datapoint></tuple></multivalue></section><section schema_id="other_section"><datapoint schema_id="notes" type="string"></datapoint></section></content><automated>false</automated><modified_at>2024-07-26T21:52:04.577442Z</modified_at><assigned_at>2024-07-26T21:51:46.429448Z</assigned_at></annotation></results><pagination><next></next><previous></previous><total>1</total><total_pages>1</total_pages></pagination></export>'''
