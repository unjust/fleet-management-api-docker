import json
# import pytest
# import pdb
from datetime import datetime
from unittest.mock import patch
from fleet_api.app import ROWS_PER_PAGE, DEFAULT_PAGE
from .mock_data import TAXIS_RESPONSE, LOCATIONS_FOR_ID_RESPONSE, LAST_LOCATIONS_RESPONSE

# pylint: disable=fixme

endpoints = {
  'taxis': '/taxis',
  'trajectories_by_taxi_id': '/trajectories',
  'latest_trajectories': '/trajectories/latest'
}

@patch('fleet_api.app.taxis.get',
    name='mock_get_taxis',
   return_value=TAXIS_RESPONSE)
def test_get_taxis(mock_get_taxis, client): # patch args are always applied in reverse order
    '''Test get taxis endpoint without explicit paging'''
    response = client.get(endpoints['taxis'])
    json.loads(response.get_data(as_text=True))
    assert mock_get_taxis.call_args.args == (DEFAULT_PAGE, ROWS_PER_PAGE)

@patch('fleet_api.app.taxis.get',
    name='mock_get_taxis',
   return_value=TAXIS_RESPONSE)
def test_get_taxis_paged(mock_get_taxis, client):
    '''Test get taxis endpoint with paging parameters'''
    client.get(endpoints['taxis'] + '?page=2&limit=20')
    assert mock_get_taxis.call_args.args == (2, 20)

@patch('fleet_api.app.trajectories.get_trajectories_by_taxi_id',
    return_value=LOCATIONS_FOR_ID_RESPONSE,
    name='mock_trajectories')
def test_get_trajectories_by_taxi_id(mock_trajectories, client):
    '''Test get locations by taxi id endpoint with date parameter'''
    client.get(endpoints['trajectories_by_taxi_id'] + '?taxiId=6419&date=01-01-2021')
    assert mock_trajectories.call_args.args == (6419,
        DEFAULT_PAGE,
        ROWS_PER_PAGE,
        datetime.strptime('01-01-2021', '%d-%m-%Y').date())

# Note: can focus tests with 'pytest -v -m focus'
# @pytest.mark.focus
def test_get_trajectories_by_taxi_id_no_date(client):
    '''Test get locations by taxi id endpoint without date parameter
    delivers correct response'''
    response = client.get(endpoints['trajectories_by_taxi_id'] + '?taxiId=6419')
    assert response.status == '400 BAD REQUEST'
    # Note had a lot of difficulty trying to mock the exceptionhandler and assert that it was called
    # tried accessing like
    # app.error_handler_spec[None][None][Exception] = MagicMock();
    # create_autospec(app.error_handler_spec[None][None][Exception])

# @pytest.mark.focus
def test_get_trajectories_by_taxi_id_invalid_date(client):
    '''Test get locations by taxi id endpoint with invalid date parameter
    delivers correct response'''
    # https://pytest-with-eric.com/introduction/pytest-assert-exception/
    response = client.get(endpoints['trajectories_by_taxi_id'] + '?taxiId=6419&date=01-01-abc')
    assert response.status == '400 BAD REQUEST'
    assert 'Invalid date format' in response.json['message']

@patch('fleet_api.app.trajectories.get_trajectories_by_taxi_id',
    return_value=LOCATIONS_FOR_ID_RESPONSE,
    name='_mock_locations')
def test_get_trajectories_by_taxi_id_with_pages(_mock_locations, client):
    '''Test get locations by taxi id endpoint with paging'''
    client.get(endpoints['trajectories_by_taxi_id'] +
      '?taxiId=6419&date=22-01-2021&page=4&limit=10')
    assert _mock_locations.call_args.args == (6419,
        4,
        10,
        datetime.strptime('22-01-2021', '%d-%m-%Y').date())

# https://stackoverflow.com/questions/29834693/unit-test-behavior-with-patch-flask
@patch('fleet_api.app.trajectories.get_latest_trajectories',
    return_value=LAST_LOCATIONS_RESPONSE,
    name='_mock_latest_trajectories')
def test_get_latest_trajectories(mock_latest_trajectories, client):
    '''Test get last locations endpoint'''
    response = client.get(endpoints['latest_trajectories'])
    assert mock_latest_trajectories.call_args.args == (DEFAULT_PAGE, ROWS_PER_PAGE)
    assert json.loads(response.get_data()) == LAST_LOCATIONS_RESPONSE

@patch('fleet_api.app.trajectories.get_latest_trajectories')
def test_get_latest_trajectories_with_page_param(mock_latest_trajectories, client):
    '''Test get last locations endpoint with page parameter'''
    client.get(endpoints['latest_trajectories'] + '?page=2')
    assert mock_latest_trajectories.call_args.args == (2, ROWS_PER_PAGE)

@patch('fleet_api.app.trajectories.get_latest_trajectories')
def test_get_latest_trajectories_params(mock_latest_trajectories, client):
    '''Test get last locations endpoint with page and limit parameter'''
    client.get(endpoints['latest_trajectories'] + '?page=5&limit=20')
    assert mock_latest_trajectories.call_args.args == (5, 20)
