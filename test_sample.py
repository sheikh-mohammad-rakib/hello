import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}

def test_no_content(client):
    response = client.get("/no_content")
    assert response.status_code == 204
    # 204 No Content responses must not include a body
    assert not response.data  # response.data should be empty for 204

def test_exp(client):
    response = client.get("/exp")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}

def test_get_data(client):
    response = client.get("/data")
    assert response.status_code == 200
    assert response.get_json()["message"].startswith("Data of length")

def test_name_search_success(client):
    response = client.get("/name_search?q=Tanya")
    assert response.status_code == 200
    assert response.get_json()["first_name"].lower() == "tanya"

def test_name_search_missing_query(client):
    response = client.get("/name_search")
    assert response.status_code == 400
    assert response.get_json() == {"message": "Query parameter 'q' is missing"}

def test_name_search_invalid_input(client):
    response = client.get("/name_search?q=1234")
    assert response.status_code == 422
    assert response.get_json() == {"message": "Invalid input parameter"}
    response = client.get("/name_search?q=   ")
    assert response.status_code == 422
    assert response.get_json() == {"message": "Invalid input parameter"}

def test_name_search_not_found(client):
    response = client.get("/name_search?q=Nonexistent")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Person not found"}
