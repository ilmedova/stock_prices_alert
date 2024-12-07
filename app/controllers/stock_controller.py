from flask import request, jsonify
from app.services.stock_service import StockService

class StockController:
    @staticmethod
    def get_user_stocks():
        try:
            auth_header = request.headers.get("Authorization")
            user_id = StockService.get_user_id_from_token(auth_header)
            user_stocks = StockService.get_user_stocks(user_id)
            return jsonify(user_stocks), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 401
        except Exception as e:
            return jsonify({"message": "Internal server error"}), 500

    @staticmethod
    def add_user_stock():
        try:
            auth_header = request.headers.get("Authorization")
            user_id = StockService.get_user_id_from_token(auth_header)

            data = request.json
            stock_symbol = data.get("stock_symbol")
            threshold = data.get("threshold")

            user_stocks = StockService.add_user_stock(user_id, stock_symbol, threshold)
            return jsonify(user_stocks), 201
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
        except Exception as e:
            return jsonify({"message": "Internal server error"}), 500

    @staticmethod
    def remove_user_stock(stock_symbol):
        try:
            auth_header = request.headers.get("Authorization")
            user_id = StockService.get_user_id_from_token(auth_header)

            user_stocks = StockService.remove_user_stock(user_id, stock_symbol)
            return jsonify(user_stocks), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
        except Exception as e:
            return jsonify({"message": "Internal server error"}), 500
