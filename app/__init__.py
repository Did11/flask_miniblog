import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['PROFILE_IMAGES_DEST'] = os.path.join(app.root_path, 'static/images/profile_images')
print(app.config['PROFILE_IMAGES_DEST'])

if not os.path.exists(app.config['PROFILE_IMAGES_DEST']):
    os.makedirs(app.config['PROFILE_IMAGES_DEST'])

# Importaciones retrasadas para evitar importaciones circulares
from .routes import users
app.register_blueprint(users)


from . import routes, models

if __name__ == "__main__":
    app.run(debug=True)
