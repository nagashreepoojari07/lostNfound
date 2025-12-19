import jwt
from datetime import datetime, timedelta

from common.database_connection import get_db_connection
SECRET_KEY = 'lostAndFound'

def create_jwt_token(payload):
   token_payload = {
       **payload,
       'exp': datetime.utcnow() + timedelta(hours=1)
   }
   return jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')

# # Example usage
# user_data = {'user_id': 123, 'username': 'john_doe'}
# token = create_jwt_token(user_data)
# print(f"Generated Token: {token}")

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # print("printing payload")
        print(payload)
        # Check if user still exists
        user = get_user_by_id(payload["id"])
        # print("user is", user)
        if not user:
            return "User does not exist"
        # print("user exists")
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


def get_user_by_id(user_id):
    print("inside get user by id")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM public.\"app_user\" WHERE \"id\" = %s",(user_id,)
    )
    user = cur.fetchall()
    print(user)
    cur.close()
    conn.close()
    return user