import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_very_secret_key"
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb+srv://houssamcan23:12345@cluster0.f9dke.mongodb.net/ai_product_db?retryWrites=true&w=majority"
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 