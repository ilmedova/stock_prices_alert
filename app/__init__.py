from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:qazwsx12@localhost/stock_notifications"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import auth_bp
    from app.stock_routes import stock_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)

    return app