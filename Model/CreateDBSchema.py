from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///dmb.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menuName = db.Column(db.Text)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menuId = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menuItemName = db.Column(db.Text)
    price = db.Column(db.Float)


class MenuImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.Text)
    imageBinary = db.Column(db.PickleType)


db.create_all()
manager = APIManager(app, flask_sqlalchemy_db=db)
methods = ['GET', 'POST', 'DELETE', 'PATCH']
url_prefix = '/dmb'
manager.create_api(Menu, methods=methods, url_prefix=url_prefix)
manager.create_api(MenuItem, methods=methods, url_prefix=url_prefix)
manager.create_api(MenuImage, methods=methods, url_prefix=url_prefix)
app.run()
