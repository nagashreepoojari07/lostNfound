from flask import Flask
from user.routes import app as user_bp
from lost_items.routes import app as lost_items_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(lost_items_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
