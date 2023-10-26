import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename  # Importamos esta utilidad para asegurar nombres de archivos
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager  # Importa JWTManager
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
app.debug = True

# Importa configuraciones de config.py
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)

# Inicialización de Bcrypt
bcrypt = Bcrypt(app)

# Configuración del directorio para guardar imágenes de perfil
app.config['PROFILE_IMAGES_DEST'] = os.path.join(app.root_path, 'static/images/profile_images')
print(app.config['PROFILE_IMAGES_DEST'])

# Asegúrate de que el directorio para guardar imágenes de perfil exista
if not os.path.exists(app.config['PROFILE_IMAGES_DEST']):
    os.makedirs(app.config['PROFILE_IMAGES_DEST'])

# Inicializa Flask-JWT-Extended
jwt = JWTManager(app)

# Ahora importa y registra el Blueprint
from .routes import users
app.register_blueprint(users)

from . import routes, models

if __name__ == "__main__":
    app.run(debug=True)
