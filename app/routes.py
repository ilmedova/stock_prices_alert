from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.controllers.stock_controller import StockController


auth_bp = Blueprint('auth_bp', __name__)
stock_bp = Blueprint("stock_bp", __name__)


auth_bp.route('/api/example', methods=['GET'])(AuthController.example)
auth_bp.route('/api/register', methods=['POST'])(AuthController.register)
auth_bp.route('/api/login', methods=['POST'])(AuthController.login)

stock_bp.route("/api/user/stocks", methods=["GET"])(StockController.get_user_stocks)
stock_bp.route("/api/user/stocks", methods=["POST"])(StockController.add_user_stock)
stock_bp.route("/api/user/stocks/<string:stock_symbol>", methods=["DELETE"])(StockController.remove_user_stock)