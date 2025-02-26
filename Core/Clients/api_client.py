from http.client import responses
from requests.auth import HTTPBasicAuth
from Core.Clients.endpoints import Endpoints
from Core.Settings.config import Users, Timeouts, BookingId
import requests
import os
from dotenv import load_dotenv
from Core.Settings.environments import Environment
import allure

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.session()
        self.session.headers = {
            'Content-type': 'application/json'
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_URL')
        else:
            raise ValueError(f'Unsupported environment: {environment}')

    def get(self, endpoint, params=None, status_code=200):
        url = self.get_base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.get_base_url + endpoint
        response = requests.post(url, headers=self.session.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step('Ping Api client'):
            url = f'{self.base_url}{Endpoints.PING_ENDPOINT}'
            response = self.session.get()
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f'Expected status 201 but got {response.status_code}'
        return response.status_code

    def auth(self):
        with allure.step('Getting auth'):
            url = f'{self.base_url}{Endpoints.AUTH_ENDPOINT}'
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        token = response.json().get('token')
        with allure.step('Updating header with auth'):
            self.session.headers.update({"Authorization": f'Bearer {token}'})

    def get_booking_by_id(self):
        with allure.step('Search by ID'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{BookingId.BOOKING_ID}'
            response = self.session.get(url, headers=self.session.headers)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def delete_booking(self):
        with allure.step('Delete by ID'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{BookingId.BOOKING_ID}'
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD))
            response.raise_for_status()
            with allure.step('Assert status code'):
                assert response.status_code == 201, f'Expected status 201 but got {response.status_code}'
        return response.status_code

    def create_booking(self, create_body):
        with allure.step('Create booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.post(url, json=create_body)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def get_bookings(self, params=None):
        with allure.step('Search bookings'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.post(url, params)
        with allure.step('Assert status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def update_booking(self, update_body):
        with allure.step('Update booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{BookingId.BOOKING_ID}'
            response = self.session.put(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD), json=update_body)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def partial_update_booking(self, partial_update_body):
        with allure.step('Partial update booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{BookingId.BOOKING_ID}'
            response = self.session.patch(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD), json=partial_update_body)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()
