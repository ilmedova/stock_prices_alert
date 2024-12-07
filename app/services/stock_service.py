from app.models import db, UserStock
import jwt

SECRET_KEY = "qazwsx12"  # Replace with a secure key


class StockService:
    @staticmethod
    def get_user_id_from_token(auth_header):
        if not auth_header or not auth_header.startswith("Bearer "):
            raise ValueError("Authorization token missing or invalid")

        token = auth_header.split(" ")[1]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    @staticmethod
    def get_user_stocks(user_id):
        user_stocks = UserStock.query.filter_by(user_id=user_id).all()
        return {stock.stock_symbol: stock.threshold for stock in user_stocks}

    @staticmethod
    def add_user_stock(user_id, stock_symbol, threshold):
        if not stock_symbol or threshold is None:
            raise ValueError("Missing stock symbol or threshold")

        user_stock = UserStock(user_id=user_id, stock_symbol=stock_symbol, threshold=threshold)
        db.session.add(user_stock)
        db.session.commit()

        return StockService.get_user_stocks(user_id)

    @staticmethod
    def remove_user_stock(user_id, stock_symbol):
        UserStock.query.filter_by(user_id=user_id, stock_symbol=stock_symbol).delete()
        db.session.commit()

        return StockService.get_user_stocks(user_id)
