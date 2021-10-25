import os
import pymysql
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from result import students, admin, main
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:test@localhost/empfynd'
db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASS')
mail = Mail(app)

from result.students.routes import student
from result.admin.routes import admin
from result.main.routes import main

app.register_blueprint(student)
app.register_blueprint(admin)
app.register_blueprint(main)