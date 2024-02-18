# import bcrypt
# from flask_jwt_extended import JWTManager, create_access_token

# salt = bcrypt.gensalt()
# password = "motdepassesecret"
# hashed_password = bcrypt.hashpw(password.encode(), salt)
# # hh = bytes(str(hashed_password.split('')[1]), 'utf-8')
# # hp = bcrypt.checkpw(password.encode(), hh)
# print(hashed_password)
# hashed_password_bytes = bytes(hashed_password.split('')[1], 'utf-8')
# print(hashed_password_bytes)
# d = {"success": True, 
#       "user": {"name":"name", "email": "email", "password":"str(hashed_password )", "salt": "str(salt)"}, 
#       "token":"str(access_token)", 
#       "status":200}
# print(d["user"]["password"])

# salt_str = str("b\"b'$2b$12$rzByW9cbXwBr2W59aRKODO'\"")
# clean_salt = salt_str[2:-1]
# print(clean_salt)

# from datauri import DataURI
# png_uri = DataURI.from_file('/Users/macbookpro/Desktop/Flask/0.png')
# txt = str(png_uri.data)
# print(png_uri.data)
# import cloudinary
# from cloudinary.uploader import upload  
        
# cloudinary.config( 
#   cloud_name = "dci5irloe", 
#   api_key = "873459432213644", 
#   api_secret = "py1r3VdpiCa7BuofyZ78dUa5lZc",
#   secure=True
# )

# upload_result = upload("0.png")
# print(upload_result['secure_url'])
# from datetime import datetime

# import timedelta

# date = str(datetime.now()).split(" ")[0]

# print(date)
# def code_aleatoire():
#     import random
#     return random.randint(111111, 999999)

# print(code_aleatoire())
# import pywhatkit
# phone_number = "+22953870071"
# message = "Bonjour, comment vas-tu ?"
# pywhatkit.sendwhatmsg(phone_number, message, 18,59)
