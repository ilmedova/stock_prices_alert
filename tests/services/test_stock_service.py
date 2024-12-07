import datetime
import json
from app.services.stock_service import StockService
import jwt


def generate_auth_header(user_id):
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    payload = {
        "user_id": user_id,
        "exp": exp
    }
    token = jwt.encode(payload, "qazwsx12", algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


def test_get_user_stocks(client, add_user):
    add_user(1, "testuser", "testpassclearword")
    stock_data = {"stock_symbol": "AAPL", "threshold": 150}
    headers = generate_auth_header(1)
    response = client.post("/api/user/stocks",
                           headers=headers,
                           data=json.dumps(stock_data),
                           content_type="application/json")
    assert response.status_code == 200


def test_add_user_stock(client, add_user):
    user = add_user(1, "testuser", "testpassclearword")
    user_id = user.id
    response = StockService.add_user_stock(user_id, "AAPL", 150)
    assert "AAPL" in response
    assert response["AAPL"] == 150


def test_remove_user_stock(client, add_user):
    user = add_user(1, "testuser", "testpassclearword")
    user_id = user.id
    StockService.add_user_stock(user_id, "AAPL", 150)
    response = StockService.remove_user_stock(user_id, "AAPL")
    assert "AAPL" not in response
