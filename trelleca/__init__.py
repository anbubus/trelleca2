from flask import Flask
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_login import LoginManager
from .models import User
from bson import ObjectId

uri = "mongodb+srv://ig0rmota6678:TRuKlMtIKBdum3r5@cluster0.fxj1uaf.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
app.config["SECRET_KEY"] = "pato"
app.config["MONGO_URI"] = uri

client = MongoClient(uri, 27017)
db = client['database']
users = db['users']

def create_app():

    login_manager = LoginManager()
    login_manager.login_view = 'auths.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = users.find_one({"_id": ObjectId(id)})
        return User(user["_id"])

    from .view import views
    from .auth import auths

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')

    return app
    
