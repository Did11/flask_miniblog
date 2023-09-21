import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_uploads import UploadSet, IMAGES, configure_uploads
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

# Configuración para Flask-Uploads
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'uploads/profile_images')
print(app.config['UPLOADED_PHOTOS_DEST'])
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from . import routes, models

if __name__ == "__main__":
    app.run(debug=True)
