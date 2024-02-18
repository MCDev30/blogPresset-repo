from flask import request, jsonify

def check_session(app,db):
    def check_availability(email):
        cursor = db.cursor()
        cursor.execute("SELECT active FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user[0] == 1:
            cursor.execute("SELECT COUNT(*) FROM Account WHERE email = %s", (email,))
            count = cursor.fetchone()[0]
            if count != 0:
                return True
        else:
            return False
    
    def ajouter_jours(date):
        import datetime
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        difference = datetime.timedelta(days=365 + 8)
        date_obj += difference
        date_str = date_obj.strftime("%Y-%m-%d")
        return date_str
    
    @app.route("/check", methods=["POST"])
    def add_check_():
        from datetime import datetime
        email = request.json.get('email')
        bank_name = request.json.get('bank_name')
        nom = request.json.get('nom')
        surname = request.json.get('surname')
        montant = request.json.get('montant')
        objet = request.json.get('objet',None)
        expire = ajouter_jours(str(datetime.now()).split(" ")[0])
        if check_availability(email):
            cursor = db.cursor()
            cursor.execute("INSERT INTO Cheque (email, bank_name, nom, surname, montant, objet, expire) VALUES (%s, %s, %s, %s, %s, %s,%s)", (email, bank_name, nom, surname, montant, objet, expire))
            db.commit()
            return jsonify({"message":"Cheque add successfully", "success":True, "status":200})
        else:
            return jsonify({"message": "No user with this email -- Unauthenticated", "status":200,"success":False})
        
    @app.route("/all_check/<email>", methods=["GET"])
    def get_historic(email):
        if check_availability(email):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Cheque WHERE email = %s", (email,))
            results = cursor.fetchall()
            data = {}
            i = 1
            for result in results:
                data["cheque"+str(i)] = {
                    "bank_name":result[2],
                    "nom_prenom":result[3] +' '+result[4],
                    "montant":result[5],
                    "objet":result[6],
                    "expire":result[7],
                    "created_at":result[8]
                }
                i += 1
            return jsonify({"success":True, "message":"All cheque created by user with email: " + email,"all_check":data, "status":200})
        else:
            return jsonify({"message": "No user with this email -- Unauthenticated", "status":200,"success":False})
    
    @app.route("/delete_check/<id>", methods=["DELETE"])
    def delete_cheque(id):
        cursor = db.cursor()
        cursor.execute("SELECT id FROM Cheque")
        cheque_ids = [cheque[0] for cheque in cursor.fetchall()]
        if id in cheque_ids:
            cursor.execute("DELETE FROM Cheque WHERE id = %s", (id,))
            db.commit()
            return jsonify({"success":"True", "message":"Cheque deleted successfully", "status":200})
        else:
            return jsonify({"success":"False", "message":"Cheque with this id is haven't exist", "status":200})
        

