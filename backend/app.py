from models import create_user_table, bank_account_table,create_cheque_table
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_cors import CORS
from bank_account import bank_session
from cheque_emission import check_session
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
        user=os.getenv('name'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    create_user_table(db=db)
    bank_account_table(db=db)
    create_cheque_table(db=db)
    authentication(app=app, db=db)
    bank_session(app=app, db=db)
    check_session(app=app, db=db)
    verification_session(app=app, db=db)
    app.run(debug=True, load_dotenv=True, port=8000)
