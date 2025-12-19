from functools import wraps
from flask import Blueprint, request, jsonify
from user.create_jwt import validate_token

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
            print(token)
        
        try:
            payload = validate_token(token)
            if isinstance(payload, str):
                return jsonify({'message': payload}), 401
            
            # Add user data to request context for use in protected routes
            request.current_user = payload
            
        except Exception as e:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorator
