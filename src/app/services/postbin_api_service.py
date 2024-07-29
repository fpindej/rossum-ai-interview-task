import base64

import requests
from flask import current_app


class PostbinApiService:
    def __init__(self):
        self.base_url = current_app.config['POSTBIN_API_BASE_URL']

    def send_data(self, annotation_id: str, xml_base64: base64):
        payload = {
            'annotationId': annotation_id,
            'content': xml_base64
        }

        response = requests.post(self.base_url, json=payload)
        if response.status_code != 200:
            current_app.logger.error(f"Failed to send data: {response.status_code} {response.text}")
            raise Exception("Failed to send data to Postbin API")
