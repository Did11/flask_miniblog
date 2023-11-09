import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import config

load_dotenv()

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configuración adicional si es necesaria
app.config['PROFILE_IMAGES_DEST'] = os.path.join(app.root_path, 'static/images/profile_images')
if not os.path.exists(app.config['PROFILE_IMAGES_DEST']):
    os.makedirs(app.config['PROFILE_IMAGES_DEST'])

# Importaciones retrasadas para evitar importaciones circulares
from .routes import users
from .models import Usuario, Post, Comentario

app.register_blueprint(users)
