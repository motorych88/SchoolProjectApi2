import pytest
import allure
import requests

@allure.feature('Test Ping')
@allure.story('Test connection')
def test_ping(api_client):
    status_code = api_client.ping()
    with allure.step('Check status code'):
        assert status_code == 201, f'Expected status 200 but got {status_code}'


@allure.feature('Test Ping')
@allure.story('Test server unavabality')
def test_ping_server_unavabality(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception('Server unavaible'))
    with pytest.raises(Exception, match='Server unavaible'):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 500'):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test wrong HTTP method')
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 405'):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test not found')
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 404'):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()