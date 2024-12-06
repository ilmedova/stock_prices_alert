from flask import Blueprint, request, jsonify
from app.models import db, UserStock
import jwt

stock_bp = Blueprint("stock_bp", __name__)


def get_user_id_from_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    decoded = jwt.decode(token, "qazwsx12", algorithms=["HS256"])
    return decoded["user_id"]


@stock_bp.route("/api/user/stocks", methods=["GET"])
def get_user_stocks():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user_stocks = UserStock.query.filter_by(user_id=user_id).all()
    selected_symbols = {stock.stock_symbol: stock.threshold for stock in user_stocks}
    return jsonify(selected_symbols)


@stock_bp.route("/api/user/stocks", methods=["POST"])
def add_user_stock():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    stock_symbol = data.get("stock_symbol")
    threshold = data.get("threshold")

    if not stock_symbol or threshold is None:
        return jsonify({"message": "Missing stock symbol or threshold"}), 400

    user_stock = UserStock(user_id=user_id, stock_symbol=stock_symbol, threshold=threshold)
    db.session.add(user_stock)
    db.session.commit()

    user_stocks = UserStock.query.filter_by(user_id=user_id).all()
    selected_symbols = {stock.stock_symbol: stock.threshold for stock in user_stocks}

    return jsonify(selected_symbols)


@stock_bp.route("/api/user/stocks/<string:stock_symbol>", methods=["DELETE"])
def remove_user_stock(stock_symbol):
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    UserStock.query.filter_by(user_id=user_id, stock_symbol=stock_symbol).delete()
    db.session.commit()

    user_stocks = UserStock.query.filter_by(user_id=user_id).all()
    selected_symbols = {stock.stock_symbol: stock.threshold for stock in user_stocks}

    return jsonify(selected_symbols)
