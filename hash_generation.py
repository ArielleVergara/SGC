from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

password = "1234"
hashed = bcrypt.generate_password_hash(password).decode('utf-8')
print(hashed)