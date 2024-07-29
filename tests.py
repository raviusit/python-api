import pytest
import requests


base_url = "http://localhost:5000/todos"
query_parameters = '2'

def test_get_all_todos():
    # Arrange

    #Act:
    response = requests.get(base_url)

    #Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()

    # Assertion of body response content:
    print(data.keys())
    assert 'Todos' in data.keys()

def test_get_a_todo():
    # Arrange

    #Act:
    response = requests.get(f'{base_url}?{query_parameters}')

    #Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    # Assertion of body response content:
    assert data['Todos'][1][1] == "Fire"

