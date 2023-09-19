import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+mysqldb://miniblog_user:Anchorena88%3F@localhost/datablog')
print("Database URI:", SQLALCHEMY_DATABASE_URI)

SQLALCHEMY_TRACK_MODIFICATIONS = False

STATIC_FOLDER = 'static' 

SECRET_KEY = os.environ.get('SECRET_KEY')