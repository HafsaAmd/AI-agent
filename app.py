from flask import Flask
from config import Config
import mongoengine
import os

# Try to load dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv not available - using environment variables directly")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongoengine.connect(host=app.config['MONGO_URI'])

    from models import User, Product 

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    # Registering blueprints here
    from views import main_bp, auth_bp, user_bp, product_bp, ai_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/admin") 
    app.register_blueprint(product_bp, url_prefix="/products") 
    app.register_blueprint(ai_bp, url_prefix="/ai")

    return app