import bcrypt
import jwt
import datetime
from app.models import User
from app import db

SECRET_KEY = "qazwsx12"

class AuthService:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def create_user(username, password):
        if User.query.filter_by(username=username).first():
            raise ValueError("User already exists")

        hashed_password = AuthService.hash_password(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not AuthService.check_password(password, user.password):
            raise ValueError("Invalid username or password")

        return user

    @staticmethod
    def generate_jwt(user_id):
        exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        return jwt.encode(
            {"user_id": user_id, "exp": exp},
            SECRET_KEY,
            algorithm="HS256"
        )

    @staticmethod
    def decode_jwt(token):
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
        except Exception as e:
            raise ValueError(f"Error decoding token: {str(e)}")
