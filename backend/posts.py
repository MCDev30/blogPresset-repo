from flask import request, jsonify


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
        image_list = ('"' + str(request.json.get('image_list')).replace('"', "'") + '"')
        cursor = db.cursor()
        if email != "":
            if verify_user_exist(email=email):
                cursor = db.cursor()
                cursor.execute("INSERT INTO Posts (email, post, image_list) VALUES (%s, %s, %s)", (
                    email, post, image_list))
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
                        # image_list =  [image for image in post[3].split("'") if image != ", " and image != "[" and image != "]" and '\"[' not in image and '\"]' not in image and ']\"' not in image] if (post[3] != "" or post[3]) else []
                        img = str(post[3], 'utf-8').replace("b'", '').replace("\'", "")
                        image_liste = img.replace("[", "").replace("]", "").replace("'", "").split(",")
                        image_list = [image.replace('"',"").replace(' ',"") for image in image_liste if image != "None"]
                    except:
                        image_list = []
                    posts["post"+str(i)] = {"id": post[0], "post": post[2],"image_list": image_list,"created_at": post[4]}
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
