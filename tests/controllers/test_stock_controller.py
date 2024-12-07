import datetime
import jwt
import json

from datetime import timedelta

def generate_token(user_id):
    secret_key = "qazwsx12"
    exp = datetime.datetime.now(datetime.timezone.utc) + timedelta(hours=1)
    payload = {
        "user_id": user_id,
        "exp": exp
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def generate_auth_header(user_id, secret="test_secret"):
    token = generate_token(user_id)
    return {"Authorization": f"Bearer {token}"}

def test_get_user_stocks(client, add_user):
    add_user(1, "testuser", "testpassclearword")
    stock_data = {"stock_symbol": "AAPL", "threshold": 150}
    client.post("/api/user/stocks",
                headers=generate_auth_header(1),
                data=json.dumps(stock_data),
                content_type="application/json")
    headers = generate_auth_header(1)
    response = client.get("/api/user/stocks", headers=headers)
    assert response.status_code == 200
    assert response.json == {"AAPL": 150}

def test_get_user_stocks_unauthorized(client):
    response = client.get("/api/user/stocks")
    assert response.status_code == 401
    assert response.json == {"message": "Unauthorized"}

def test_add_user_stock(client, add_user):
    add_user(1, "testuser", "testpassclearword")
    stock_data = {"stock_symbol": "GOOGL", "threshold": 200}
    headers = generate_auth_header(1)
    response = client.post("/api/user/stocks",
                           headers=headers,
                           data=json.dumps(stock_data),
                           content_type="application/json")
    assert response.status_code == 200
    assert response.json == {"GOOGL": 200}

def test_remove_user_stock(client, add_user):
    add_user(1, "testuser", "testpassclearword")
    stock_data = {"stock_symbol": "AAPL", "threshold": 150}
    headers = generate_auth_header(1)
    client.post("/api/user/stocks", headers=headers,
                data=json.dumps(stock_data), content_type="application/json")
    response = client.delete("/api/user/stocks/AAPL", headers=headers)
    assert response.status_code == 200
    assert response.json == {}
