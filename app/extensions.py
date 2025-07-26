from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
