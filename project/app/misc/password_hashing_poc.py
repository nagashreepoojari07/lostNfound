from sys import hash_info
import bcrypt
# Hashing a password
password = "MySecurePassword"
password_encoded = password.encode('utf-8')
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password_encoded, salt)
print("Hashed Password:", hashed_password)
# Verifying a password

# entered_password = b"MySecurePassword"
if bcrypt.checkpw(password_encoded, hashed_password):
   print("Password match!")
else:
   print("Incorrect password.")

print(type(hashed_password))
string_data = hashed_password.decode('utf-8')
byte_data = string_data.encode('utf-8')
print(byte_data==hashed_password)
