import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename  # Importamos esta utilidad para asegurar nombres de archivos
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = True

# Importa configuraciones de config.py
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

csrf = CSRFProtect(app)

# Configuración del directorio para guardar imágenes de perfil
app.config['PROFILE_IMAGES_DEST'] = os.path.join(app.root_path, 'static/images/profile_images')
print(app.config['PROFILE_IMAGES_DEST'])

# Asegúrate de que el directorio para guardar imágenes de perfil exista
if not os.path.exists(app.config['PROFILE_IMAGES_DEST']):
    os.makedirs(app.config['PROFILE_IMAGES_DEST'])

from . import routes, models

if __name__ == "__main__":
    app.run(debug=True)
