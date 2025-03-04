import pytest
import allure
import requests


@allure.feature('Test Create')
@allure.story('Test connection')
def test_create(api_client):
    status_code = api_client.create_booking()
    with allure.step('Check status code'):
        assert status_code == 200, f'Expected status 200 but got {status_code}'

