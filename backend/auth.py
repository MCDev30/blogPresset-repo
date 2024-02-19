from flask_jwt_extended import create_access_token
import bcrypt
from flask import request, jsonify


def register(username, password, email, access_token, msg):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    if not (username or password or email):
        return {"success": False, "message": "Assurez vous d'avoir remplir tous les champs", "status": 401}, None
    return {"success": True, "message": msg, "user": {"username": username,"email": email}, "token": str(access_token), "status": 200}, {"password": str(hashed_password), "salt": str(salt)}


def login(username,email, password, access_token, check, profile, citation):
    if not (password or email):
        return {"success": False, "message": "Assurez vous d'avoir remplir tous les champs", "status": 401}
    if not check:
        return {"success": check, "message": "Mot de passe incorrecte", "status": 401}
    return {"success": check, "message": "Connexion réussie", "user": {"username": username,"email": email, "profile":profile , "citation":citation}, "token": access_token, "status": 200}


def authentication(app, db):
    @app.route('/')
    def index():
        return "Documentation"

    # inscription
    @app.route('/register', methods=['POST'])
    def user_register():
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        cursor = db.cursor()
        insert_query = "INSERT INTO User (username, password, email, salt, token, active) VALUES (%s,%s, %s, %s, %s, %s)"
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        all_mail = cursor.fetchone()
        if all_mail:
            return jsonify({"success": False, "message": "Un utilisateur avec ce mail existe déjà", "status": 400})
        access_token = create_access_token(identity=email)
        data, query = register(username, password, email, access_token, "Inscription effectuée avec succès")
        cursor.execute(insert_query, (username, query["password"], email,
                                      query["salt"], access_token, 0))
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
            password = str(user[2])[2:-1]
            salt = str(user[5])[2:-1]
            salt = salt.split("'")[1]
            pwd = bcrypt.hashpw(pwd.encode(), bytes(salt, 'utf-8'))
            check = str(password) == str(pwd)
            data = login(user[1], mail, pwd, user[6],check, user[4], user[11])
            set_user_active(mail, 1)
        else:
            return jsonify({"success": False, "message": "Cet utilisateur n'existe pas. Inscrivez-vous!", "status": 404})
        return jsonify(data)

    # verifier l'accès
    def verify_token(token, email):
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM User WHERE token = %s AND email = %s", (token, email))
        user = cursor.fetchone()
        if user and user[7] == 1:
            return True
        else:
            return False
        
        
    @app.route('/user/<token>/<email>', methods=['GET'])
    def get_user_information(token, email):
        if verify_token(token, email):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
            user_info = cursor.fetchall()
            user_info_list = []
            for user_data in user_info:
                id, username, password, email, profile, salt, token, active, code, created_at, updated_at = user_data
                user_info_list.append({"id": id, "username": username, "email": email, "profile": profile, "active": active,
                                       "created_at": created_at, "updated_at": updated_at})
            return jsonify(user_info_list)
        else:
            return jsonify({"success":False, "message": "Accès refusé. Token invalide"})
        
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
            return jsonify({"error": "Accès refusé. Token invalide"})

    def delete_user(email):
        cursor = db.cursor()
        cursor.execute("DELETE FROM User WHERE email = %s", (email,))
        db.commit()

    @app.route('/reset-password', methods=['PUT'])
    def change_password():
        email = request.json.get('email', None)
        new_password = request.json.get('password', None)
        cursor = db.cursor()
        cursor.execute("SELECT username FROM User WHERE email = %s", (email,))
        username = cursor.fetchone()[0]
        if username:
            delete_user(email)
            insert_query = "INSERT INTO User (username, password, email, salt, token, active) VALUES (%s,%s, %s, %s, %s, %s)"
            access_token = create_access_token(identity=email)
            data, query = register(username, new_password, email, access_token, "Changement du mot de passe avec succès")
            cursor.execute(insert_query, (username, query["password"], email, query["salt"], access_token, 0))
            db.commit()
            return jsonify(data)
        else:
            return jsonify({"success": False, "message": "Cet utilisateur n'existe pas. Inscrivez-vous!", "status": 404})

    # supprimer un compte
    @app.route('/delete-account', methods=["DELETE"])
    def delete_user_account():
        email = request.json.get('email', None)
        token = request.json.get('token', None)
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM User WHERE email = %s AND token = %s", (email, token))
        db.commit()
        return jsonify({"message": "L'utilisateur avec l'email = " + email + ' est supprimé avec succès', "status": 200})

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
            return jsonify({"message": "Déconnexion effectuée", "status": 200})
        else:
            return jsonify({"message": "Echec de déconnexion. Réessayez", "status": 404, "error": "User not found"})
