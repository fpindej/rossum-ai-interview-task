import requests
from flask import current_app
from requests import Response


class RossumApiService:
    def __init__(self):
        self.base_url = current_app.config['ROSSUM_API_BASE_URL']
        self.bearer_token = self.__login()

    def __login(self):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'username': current_app.config['ROSSUM_API_USERNAME'],
            'password': current_app.config['ROSSUM_API_PASSWORD']
        }

        url = f'{self.base_url}/auth/login'
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            current_app.logger.error(f"Failed to login: {response.status_code} {response.text}")
            raise Exception("Failed to login to Rossum API")

        current_app.logger.info('Logged in successfully to Rossum API')
        bearer_token = response.json()['key']
        return bearer_token

    def export_queue(self, queue_id: str, annotation_id: str, export_format='xml',
                     export_status='exported') -> Response:
        headers = {
            'Authorization': f'Bearer {self.bearer_token}'
        }
        query_params = {
            'id': annotation_id,
            'format': export_format,
            'status': export_status
        }
        url = f'{self.base_url}/queues/{queue_id}/export'

        current_app.logger.info('Fetching data from Rossum API, url: %s', url)
        response = requests.get(url, headers=headers, params=query_params)

        if response.status_code != 200:
            current_app.logger.error(f"Failed to fetch data: {response.status_code} {response.text}")
            raise Exception("Failed to fetch data from Rossum API")

        current_app.logger.info('Data fetched successfully from Rossum API')
        return response
