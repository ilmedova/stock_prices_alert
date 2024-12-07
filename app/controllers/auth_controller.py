from flask import request, jsonify
from app.services.auth_service import AuthService

class AuthController:
    @staticmethod
    def example():
        return "Hello world"

    @staticmethod
    def register():
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({"message": "Missing required fields"}), 400

            AuthService.create_user(username, password)
            return jsonify({"message": "User registered successfully"}), 201
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
        except Exception as e:
            return jsonify({"message": "Internal server error"}), 500

    @staticmethod
    def login():
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({"message": "Missing username or password"}), 400

            user = AuthService.authenticate_user(username, password)
            token = AuthService.generate_jwt(user.id)
            return jsonify({"message": "Login successful", "token": token}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 401
        except Exception as e:
            return jsonify({"message": "Internal server error"}), 500
