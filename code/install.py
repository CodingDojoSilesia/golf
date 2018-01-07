from app import app, db

with app.app_context():
    print('create database schema...')
    db.create_all()
