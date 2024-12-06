from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database schema is created
    app.run(debug=True)
