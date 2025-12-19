from operator import attrgetter
from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from common.database_connection import get_db_connection
# from project.notification_layer.rabbitQ_setup import get_mq_connection
import bcrypt
from user.create_jwt import create_jwt_token,validate_token
# from flask_jwt_extended import jwt_required
from common.utils import token_required

app = Blueprint('user', __name__, url_prefix='/api/')

#signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone_no")
    email = data.get("email_id")
    password = data.get("password")

    # Hashing a password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    print("Hashed Password:", hashed_password)
    hashed_password_str = hashed_password.decode('utf-8')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO public.\"app_user\" (\"name\", \"phone_no\", \"email_id\", \"password_hash\") VALUES (%s, %s, %s, %s)",
        (name, phone, email, hashed_password_str)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "User profile created successfully"}), 201

#signin
@app.route('/signin', methods=['POST'])
def signin():
    print("entered sign in")
    data = request.get_json()

    email = data.get("email_id")
    password = data.get("password")

    # Hashing a password
    password_bytes = password.encode('utf-8')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT \"password_hash\" FROM public.\"app_user\" WHERE \"email_id\" = %s",
        (email,)
    )
    password_hash = cur.fetchone()[0]
    print(password_hash)
    # conn.commit()


    # Verifying a password
    if bcrypt.checkpw(password_bytes, password_hash.encode('utf-8')):
        print("Password match!")
        # Example usage
        cur.execute(
            "SELECT \"id\", \"name\", \"phone_no\", \"email_id\" FROM public.\"app_user\" WHERE \"email_id\" = %s",
            (email,)
        )
        user_row = cur.fetchone()
        user_data = {
            "id": user_row[0],
            "name": user_row[1], 
            "phone_no": user_row[2],
            "email_id": user_row[3]
        }
        print(user_data)
        token = create_jwt_token(user_data)
        print(f"Generated Token: {token}")
        cur.close()
        conn.close()
        return jsonify({"message": "User logged in successfully", "token": token}), 200
    else:
        print("Incorrect password.")
        cur.close()
        conn.close()
        return jsonify({"message": "Incorrect password"}), 401


# Example route: get all users
@app.route('/users', methods=['GET'])
# @jwt_required()
@token_required
def get_users():
    current_user = request.current_user  # Access logged-in user data
    print(f"User {current_user['name']} is accessing users list")
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM public.\"app_user\";")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)
