import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+mysqldb://miniblog_user:Anchorena88%3F@localhost/datablog')
print("Database URI:", SQLALCHEMY_DATABASE_URI)

SQLALCHEMY_TRACK_MODIFICATIONS = False

STATIC_FOLDER = 'static' 

SECRET_KEY = os.environ.get('SECRET_KEY')

# Configuraciones para Flask-JWT-Extended
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)  # Usando la misma clave secreta para JWT. Se puede cambiar.
JWT_ACCESS_TOKEN_EXPIRES = 3600  # Duración del token de acceso en segundos. Está configurado para 1 hora.
JWT_ALGORITHM = 'HS256'

# Modo de depuración
DEBUG = True  # Asegúrate de cambiar esto a False en producción
