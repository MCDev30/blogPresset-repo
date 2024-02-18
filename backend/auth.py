from flask_jwt_extended import create_access_token
import bcrypt
from flask import request, jsonify


def register(name, surname, email, phone, password, access_token, msg):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    if not (name or surname or password or email):
        return {"success": False, "message": "All data is required", "status": 401}, None
    return {"success": True, "message": msg, "user": {"name": name, "surname": surname, "email": email, "phone": phone}, "token": str(access_token), "status": 200}, {"password": str(hashed_password), "salt": str(salt)}


def login(name, surname, email, password, phone, access_token, check):
    if not (password or email):
        return {"success": False, "message": "All data is required", "status": 401}
    if not check:
        return {"success": check, "message": "Login unsuccessful", "error": "incorrect password", "status": 401}
    return {"success": check, "message": "Login successful", "user": {"name": name, "surname": surname, "email": email, "phone": phone}, "token": access_token, "status": 200}


def authentication(app, db):
    @app.route('/')
    def index():
        return "Documentation"

    # inscription
    @app.route('/register', methods=['POST'])
    def user_register():
        name = request.json.get('name', None)
        surname = request.json.get('surname', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        phone = request.json.get('phone', None)
        cursor = db.cursor()
        insert_query = "INSERT INTO User (name, surname, email, password, phone, salt, token, active) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        all_mail = cursor.fetchone()
        if all_mail:
            return jsonify({"success": False, "message": "Email already exists", "status": 400})
        access_token = create_access_token(identity=name)
        data, query = register(name, surname, email, phone,
                               password, access_token, "Register successful")
        cursor.execute(insert_query, (name, surname, email,
                                      query["password"], phone, query["salt"], access_token, 0))
        db.commit()
        return jsonify(data)

    # rendre active la session de l'utilisateur
    def set_user_active(email, active_status):
        import random
        cursor = db.cursor()
        cursor.execute("UPDATE User SET active = %s WHERE email = %s",
                       (active_status, email))
        cursor.execute("UPDATE User SET code = %s WHERE email = %s", (str(random.randint(111111, 999999)), email))
        db.commit()

    # Connexion
    @app.route('/login', methods=['POST'])
    def user_login():
        mail = request.json.get('email', None)
        pwd = request.json.get('password', None)
        # token = request.json.get('token', None)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM User WHERE email = %s", (mail,))
        user = cursor.fetchone()
        if user:
            password = str(user[4])[2:-1]
            salt = str(user[6])[2:-1]
            salt = salt.split("'")[1]
            pwd = bcrypt.hashpw(pwd.encode(), bytes(salt, 'utf-8'))
            check = str(password) == str(pwd)
            data = login(user[1], user[2], mail, pwd, user[5], user[7], check)
            set_user_active(mail, 1)
            
        else:
            return jsonify({"success": False, "message": "User not found. Register firstly", "status": 404})
        return jsonify(data)

    # verifier l'accès
    def verify_token(token, email):
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM User WHERE token = %s AND email = %s", (token, email))
        user = cursor.fetchone()
        if user and user[6] == 1:
            return True
        else:
            return False

    @app.route('/users/<token>/<email>', methods=['GET'])
    def get_all_users(token, email):
        if verify_token(token, email):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM User")
            users = cursor.fetchall()
            users_list = []
            for user in users:
                id, name, surname, email, password, phone, salt, token, active, created_at, updated_at = user
                password = str(password)[2:-1]
                salt = str(salt)[2:-1]
                users_list.append({"id": id, "name": name, "surname": surname, "email": email, "phone": phone,
                                   "created_at": created_at, "updated_at": updated_at})
            return jsonify(users_list)
        else:
            return jsonify({"error": "Authorization failed. Try to put the valid token"})

    def delete_user(email):
        cursor = db.cursor()
        cursor.execute("DELETE FROM User WHERE email = %s", (email,))
        db.commit()

    @app.route('/reset-password', methods=['PUT'])
    def change_password():
        email = request.json.get('email', None)
        new_password = request.json.get('password', None)
        cursor = db.cursor()
        cursor.execute("SELECT name FROM User WHERE email = %s", (email,))
        name = cursor.fetchone()[0]
        cursor.execute("SELECT surname FROM User WHERE email = %s", (email,))
        surname = cursor.fetchone()[0]
        cursor.execute("SELECT phone FROM User WHERE email = %s", (email,))
        phone = cursor.fetchone()[0]
        if name:
            delete_user(email)
            insert_query = "INSERT INTO User (name, surname, email, password, phone, salt, token, active) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
            access_token = create_access_token(identity=name)
            data, query = register(name, surname, email, phone,
                                   new_password, access_token, "Password change successful")
            cursor.execute(insert_query, (name, surname, email,
                                          query["password"], phone, query["salt"], access_token, 0))
            db.commit()
            return jsonify(data)
        else:
            return jsonify({"success": False, "message": "User with this email not found. Please register", "status": 404})

    # supprimer un compte
    @app.route('/delete-account', methods=["DELETE"])
    def delete_user_account():
        email = request.json.get('email', None)
        token = request.json.get('token', None)
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM User WHERE email = %s AND token = %s", (email, token))
        db.commit()
        return jsonify({"message": "The user with email = " + email + ' has been deleted successfully', "status": 200})

    # logout
    @app.route('/logout', methods=['POST'])
    def logout():
        email = request.json.get('email', None)
        token = request.json.get('token', None)
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM User WHERE email = %s AND token = %s", (email, token))
        user = cursor.fetchone()
        if user:
            set_user_active(email, 0)
            return jsonify({"message": "Logout successfully", "status": 200})
        else:
            return jsonify({"message": "Logout failed. Try again to fix the error", "status": 404, "error": "User not found"})
