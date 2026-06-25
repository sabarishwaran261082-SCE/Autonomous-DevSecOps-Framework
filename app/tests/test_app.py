from app import app

client = app.test_client()


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200


def test_login_page():
    response = client.get("/login")
    assert response.status_code == 200


def test_dashboard_page():
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_health_api():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "UP"