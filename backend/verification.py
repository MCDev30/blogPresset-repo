from flask import request, jsonify
import smtplib

def verification_session(app, db):
    @app.route("/send_email", methods=["POST"])
    def send_verification_email():
        from email.message import EmailMessage
        email = request.json.get('email') 
        cursor = db.cursor()
        cursor.execute("SELECT code FROM User WHERE email = %s", (email,))
        code = cursor.fetchone()[0]
        smtp_server = "smtp.gmail.com"
        port = 587
        username = 'charbelzmk@gmail.com'
        password = 'afjk hkpv onzl oxuj'
        msg = EmailMessage()
        msg['From'] = 'E-CHECK Admin@panel'
        msg['To'] = email
        msg['Subject'] = ' '
        msg.set_content(
            f"Code de verification\n\n\t{code}")
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            data = {"message": "Email envoye avec succes !","status": 200,"success": True}
            return jsonify(data)
        except Exception as e:
            data = {"message": "Email non envoyé !","status": 200,"success": False}
            return jsonify(data)
    
    @app.route("/verify_email/<email>/<code>", methods=["GET"])
    def verify_code(email, code):
        cursor = db.cursor()
        cursor.execute("SELECT code FROM User WHERE email = %s", (email,))
        code_from_db = cursor.fetchone()[0]
        if str(code) == str(code_from_db):
            return jsonify({"success":True, "message":"Correct code", "status":200})
        else:
            return jsonify({"success":False, "message":"Incorrect code", "status":200})