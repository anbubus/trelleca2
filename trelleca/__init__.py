from flask import Flask
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ig0rmota6678:TRuKlMtIKBdum3r5@cluster0.fxj1uaf.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
app.config["SECRET_KEY"] = "pato"
app.config["MONGO_URI"] = uri

client = MongoClient(uri, 27017)
db = client.database


def create_app():
    from .view import views
    from .auth import auths

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')

    return app
    
