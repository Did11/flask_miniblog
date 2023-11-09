from app import db
from datetime import datetime
from . import bcrypt

def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Definición de la tabla intermedia comment_likes
comentarios_like = db.Table('comentarios_like',
    db.Column('user_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comentario.id'))
)

from datetime import datetime

class Usuario(db.Model): 
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    avatar_filename = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comentario', backref='author', lazy=True)
    bcrypt_password_hash = db.Column(db.String(128))

        
    def set_password(self, password):
        self.bcrypt_password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.bcrypt_password_hash, password)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    liked_by = db.relationship('Usuario', secondary=comentarios_like, backref=db.backref('comment_likes', lazy='dynamic'))


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)

