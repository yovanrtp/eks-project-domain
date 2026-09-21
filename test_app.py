import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_login_success(client):
    rv = client.post('/login', data={'username': 'admin', 'password': 'password123'}, follow_redirects=True)
    assert b"Hello, admin!" in rv.data

def test_login_failure(client):
    rv = client.post('/login', data={'username': 'admin', 'password': 'wrong'}, follow_redirects=True)
    assert b"Invalid credentials" in rv.data