from models import create_user_table,create_posts_table
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_cors import CORS
from posts import posts_session
from verification import verification_session
from auth import authentication
from dotenv import load_dotenv
import mysql.connector
import os

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

load_dotenv()

if __name__ == "__main__":
    db = mysql.connector.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    create_user_table(db=db)
    create_posts_table(db=db)
    authentication(app=app, db=db)
    posts_session(app=app, db=db)
    verification_session(app=app, db=db)
    app.run(debug=True, load_dotenv=True, port=8000)
