from flask.testing import FlaskClient
from app.app import app

def test_health():
    client = app.test_client()
    
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    print("Healthcheck passed")
    
if __name__ == "__main__":
    test_health()