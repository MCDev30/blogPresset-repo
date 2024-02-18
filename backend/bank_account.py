from flask import request, jsonify


def bank_session(app, db):
    def verify_user_exist(email):
        cursor = db.cursor()
        cursor.execute("SELECT active FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user[0] == 1:
            return True
        else:
            return False

    @app.route('/add-account', methods=['POST'])
    def add_check():
        email = request.json.get('email')
        bank = request.json.get('bank')
        account_number = request.json.get('account_number')
        iban = request.json.get('iban')
        bic = request.json.get('bic')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Account WHERE email = %s AND bank = %s AND account_number = %s AND iban = %s AND bic = %s",
                       (email, bank, account_number, iban, bic))
        existing_account = cursor.fetchone()
        if not existing_account:
            if verify_user_exist(email=email):
                cursor = db.cursor()
                cursor.execute("INSERT INTO Account (email, bank, account_number, iban, bic) VALUES (%s, %s, %s, %s, %s)", (
                    email, bank, account_number, iban, bic))
                db.commit()
                return jsonify({"success": True, "message": "Bank account add successfully", "Acount_info": {"email": email, "bank": bank, "account_number": account_number, "iban": iban, "bic": bic}, "status": 200})
            else:
                return (jsonify({"success": False, "message": "Something wen't wrong", "status": 404, "error": "Permission denied"}))
        else:
            return (jsonify({"success": False, "message": "The account with this credentials already exist", "status": 200}))

    @app.route('/accounts/<email>', methods=['GET'])
    def get_user_account(email):
        if verify_user_exist(email):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Account WHERE email = %s", (email,))
            user_accounts = cursor.fetchall()
            account = {}
            if len(user_accounts) > 0:
                mail = user_accounts[0][1]
                i = 1
                for acc in user_accounts:
                    account["account"+str(i)] = {"id": acc[0], "bank": acc[2],
                                                 "account_number": acc[3], "iban": acc[4], "bic": acc[5], "created_at": acc[6]}
                    i += 1
                return jsonify({"success": True, "owner": mail, "user_accounts": account, "status": 200, "length": len(user_accounts)})
            else:
                return jsonify({"success": True, "user_accounts": account, "status": 200, "length": len(user_accounts)})

    @app.route('/delete_bank/<email>/<id>', methods=['DELETE'])
    def delete_bank(email, id):
        if verify_user_exist(email):
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM Account WHERE email = %s AND id = %s", (email, id))
            db.commit()
            return jsonify({"success": True, "message": "Account deleted successful", "status": 200})
        else:
            return jsonify({"success": False, "message": "Account deleting failed", "status": 404, "error": "Permission denied"})
