from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = "oxRJONF-qPdcIHDM-ZMBxrGIg-qOJfyNB"


#################------------- Model start -------------#################
def create_user_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password BLOB NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            profile BLOB,
            salt BLOB NOT NULL,
            token VARCHAR(2000) NOT NULL,
            active INT NOT NULL,
            code VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            Citation VARCHAR(255)
        )
    """)

def create_posts_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            post VARCHAR(255) NOT NULL,
            image_1 TEXT,
            image_2 TEXT,
            image_3 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  
        )
    """)

def create_comments_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            comment_email VARCHAR(255) NOT NULL,
            post_id INT NOT NULL,
            comments VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  
        )
    """)
#################------------- Model end -------------#################


#################------------- authentication start -------------#################
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
    def api_documentation():
        documentation = """
        <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Blog Presset api documentation</title>
            </head>
            <style>
                body{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                section{
                    text-align: justify;
                    display: flex;
                    flex-wrap: wrap;
                    align-items: center;
                    justify-content: center;
                    padding: 30px;
                    width: 100%;
                    border-radius: 10px;
                    margin-left:10%;
                }
                div{
                    width: 100%;
                    font-size: 1.4vw;
                }
                code{
                    border: 1px solid ;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 1vw;
                    margin-bottom: 10px;
                    cursor:pointer;
                }
            </style>
            <body>
                <section>
                    <div>
                        <p>Enregistrer un nouvel utilisateur.</p>
                        <code>/register - POST</code>
                        <code>/login - POST</code>
                        <p>Route pour se connecter avec une authentification JWT.</p>
                        
                        <code>/update_profile - PUT</code>
                        <p>Route pour mettre à jour le profil de l'utilisateur.</p>
                        
                        <code>/delete_user_account - DELETE</code>
                        <p>Route pour désactiver ou supprimer le compte utilisateur.</p>
                        
                        <code>/create_post - POST</code>
                        <p>Route pour créer un nouveau post.</p>
                        
                        <code>/update_post/{post_id} - PUT</code>
                        <p>Route pour mettre à jour un post spécifique.</p>
                        <code>/delete_post/{post_id} - DELETE</code>
                        <p>Route pour supprimer un post spécifique.</p>
                        
                        
                    </div>
                    
                    <div>
                        
                        <code>/add_comments{email}/{post_id} - POST</code>
                        <p>Route pour ajouter des commentaires à un post.</p>
                        <code>/update_comments/{email}/{comments_id} - PUT</code>
                        <p>Route pour mettre à jour des commentaires spécifiques.</p>
                        
                        <code>/delete_comments/{comments_id} - DELETE</code>
                        <p>Route pour supprimer des commentaires spécifiques.</p>
                        
                        <code>/get_comments/{post_id} - GET</code>
                        <p>Route pour obtenir les commentaires d'un post spécifique.</p>
                        
                        <code>/send_email - POST</code>
                        <p>Route pour envoyer un email de vérification.</p>
                        
                        <code>/verify_email/{email}- GET</code>

                        <p>Route pour vérifier l'email avec le code de vérification.</p>
                    </div>
                </section>
                
            </body>
        </html>
        """
        return documentation

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
        insert_query = "INSERT INTO User (username, password, email, profile, salt, token, active) VALUES (%s,%s, %s, %s, %s, %s,%s)"
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            user_info = [user[1],email,user[4]]
            delete_user(email)
            access_token = create_access_token(identity=email)
            data, query = register(user_info[0], new_password, email,access_token, "Mot de passe changé avec succès")
            cursor.execute(insert_query, (user_info[0], query["password"], email,  user_info[2],query["salt"], access_token, 0))
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
    
    
    # update account
    @app.route('/update_profile', methods=["POST"])
    def update_user():
        username = request.json.get('username', None)
        email= request.json.get('email', None)
        profile = request.json.get('profile', None)
        cursor = db.cursor()
        if username is not None and profile is not None:
            cursor.execute("UPDATE User SET username = %s, profile = %s WHERE email = %s", (username, profile, email))
            db.commit()
            return jsonify({"message": "Profile mis à jour avec succès", "status": 200, "success":True})
        elif username is not None:
            cursor.execute("UPDATE User SET username = %s WHERE email = %s", (username, email))
            db.commit()
            return jsonify({"message": "Nom d'utilisateur mis à jour avec succès", "status": 200, "success":True})
        elif profile is not None:
            cursor.execute("UPDATE User SET profile = %s WHERE email = %s", (profile, email))
            db.commit()
            return jsonify({"message": "Profil mis à jour avec succès", "status": 200, "success":True})
        else:
            return jsonify({"message": "Aucune donnée à mettre à jour", "status": 400, "success":True})
    
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
#################------------- authentication end -------------#################


#################------------- Posts start -------------#################
def posts_session(app, db):
    def verify_user_exist(email):
        cursor = db.cursor()
        cursor.execute("SELECT active FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user[0] == 1:
            return True
        else:
            return False

    @app.route('/add-posts', methods=['POST'])
    def add_posts():
        email = request.json.get('email')
        post = request.json.get('post')
        image_1 = request.json.get('image_1')
        image_2 = request.json.get('image_1')
        image_3 = request.json.get('image_1')
        cursor = db.cursor()
        if email != "":
            if verify_user_exist(email=email):
                cursor = db.cursor()
                cursor.execute("INSERT INTO Posts (email, post, image_1, image_2, image_3) VALUES (%s, %s, %s, %s, %s)",(
                    email, post, image_1, image_2, image_3))
                db.commit()
                return jsonify({"success": True, "message": "Publication ajoutée", "status": 200})
            else:
                return (jsonify({"success": False, "message": "Une erreur s'est produite", "status": 404, "error": "Permission denied"}))
        else:
            return (jsonify({"success": False, "message": "The account with this credentials already exist", "status": 200}))


    @app.route('/posts/<email>', methods=['GET'])
    def get_user_posts(email):
        if verify_user_exist(email):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Posts WHERE email = %s", (email,))
            user_post = cursor.fetchall()
            posts = {}
            if user_post and len(user_post) > 0:
                mail = user_post[0][1]
                i = 1
                for post in user_post:
                    try:
                        image_list = [post[3],post[4],post[5]]
                    except:
                        image_list = []
                    posts["post"+str(i)] = {"id": post[0], "post": post[2],"image_list": image_list,"created_at": post[6]}
                    i += 1
                return jsonify({"success": True, "email": mail, "all_user_posts": posts, "status": 200, "length": len(user_post)})
            else:
                return jsonify({"success": True, "user_accounts": posts, "status": 200, "length": 0})
            

    @app.route('/delete_post/<email>/<id>', methods=['DELETE'])
    def delete_post(email, id):
        if verify_user_exist(email):
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM Posts WHERE email = %s AND id = %s", (email, id))
            db.commit()
            return jsonify({"success": True, "message": "Publication suprimée avec succès", "status": 200})
        else:
            return jsonify({"success": False, "message": "Une erreur s'est produite", "status": 404, "error": "Permission denied"})


    @app.route('/all_posts_with_comments', methods=['GET'])
    def get_all_posts_with_comments():
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Posts")
        all_posts = cursor.fetchall()
        posts_with_comments = {}
        for post in all_posts:
            post_id = post[0]
            cursor.execute("SELECT * FROM Comments WHERE post_id = %s", (post_id,))
            comments = cursor.fetchall()
            post_comments = []
            for comment in comments:
                post_comments.append({"comment_id": comment[0], "comment_email": comment[1], "comments": comment[3], "created_at": comment[4]})
            posts_with_comments["post"+str(post_id)] = {"post_id": post[0], "email": post[1], "post": post[2], "image_1": post[3], "image_2": post[4], "image_3": post[5], "created_at": post[6], "comments": post_comments}
        return jsonify({"success": True, "all_posts_with_comments": posts_with_comments, "status": 200, "total_posts": len(all_posts)})
#################------------- Posts end -------------#################


#################------------- Comments start -------------#################
def comments_session(app, db):
    @app.route('/add_comments/<email>/<post_id>', methods=['POST'])
    def add_comments(email, post_id):
        comments = request.json.get('comments')
        cursor = db.cursor()
        cursor.execute("INSERT INTO Comments (comment_email, post_id, comments) VALUES (%s, %s, %s)", (
            email, post_id, comments))
        db.commit()
        return jsonify({"success": True, "message": "Commentaire ajouté avec succès", "status": 200})
    
    @app.route('/update_comments/<email>/<comments_id>', methods=['PUT'])
    def update_comments(email, comments_id):
        new_comments = request.json.get('comments')
        cursor = db.cursor()
        cursor.execute("UPDATE Comments SET comments = %s WHERE comment_email = %s AND id = %s", (
            new_comments, email, comments_id))
        db.commit()
        return jsonify({"success": True, "message": "Commentaire mis à jour avec succès", "status": 200})
    
    @app.route('/delete_comments/<comments_id>', methods=['DELETE'])
    def delete_comments(comments_id):
        cursor = db.cursor()
        cursor.execute("DELETE FROM Comments WHERE id = %s", (comments_id,))
        db.commit()
        return jsonify({"success": True, "message": "Commentaire supprimé avec succès", "status": 200})
    
    @app.route('/get_comments/<post_id>', methods=['GET'])
    def get_comments(post_id):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Comments WHERE post_id = %s", (post_id,))
        comments = cursor.fetchall()
        all_comments = {}
        if comments and len(comments) > 0:
            i = 1
            for comment in comments:
                all_comments["comment"+str(i)] = {"id": comment[0], "comment_email": comment[1], "comments": comment[3], "created_at": comment[4]}
                i += 1
            return jsonify({"success": True, "all_comments": all_comments, "status": 200, "length": len(comments)})
        else:
            return jsonify({"success": True, "all_comments": all_comments, "status": 200, "length": 0})
#################------------- Comments end -------------#################



if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        port=8889,
        user="root",
        password="root",
        database="BlogPresset"
    )
    create_user_table(db=db)
    create_posts_table(db=db)
    create_comments_table(db=db)
    authentication(app=app, db=db)
    posts_session(app=app, db=db)
    comments_session(app=app, db=db)
    
    
    
    app.run(debug=True, port=8000)
