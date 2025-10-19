from mongoengine import Document, StringField, ListField, ReferenceField, FloatField
from flask_login import UserMixin

class User(UserMixin, Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    roles = ListField(StringField(), default=["client"])

    meta = {
        "collection": "users",
        "indexes": [
            "email"
        ]
    }

class Product(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    price = FloatField(required=True)
    image_url = StringField(default="https://via.placeholder.com/300x200?text=No+Image")

    meta = {
        "collection": "products",
        "indexes": [
            "name"
        ]
    }