from models import User
from werkzeug.security import generate_password_hash

class UserController:
    @staticmethod
    def get_all_users():
        return User.objects()

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects(id=user_id).first()

    @staticmethod
    def create_user(email, password, roles=["client"]):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(email=email, password=hashed_password, roles=roles)
        user.save()
        return user

    @staticmethod
    def update_user(user_id, email=None, password=None, roles=None):
        user = User.objects(id=user_id).first()
        if user:
            if email: user.email = email
            if password: user.password = generate_password_hash(password, method='pbkdf2:sha256')
            if roles: user.roles = roles
            user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.objects(id=user_id).first()
        if user:
            user.delete()
            return True
        return False