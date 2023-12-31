from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField, StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class UpdateProfileForm(FlaskForm):
    avatar = FileField('Actualizar Avatar', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrarse')

class CreatePostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    submit = SubmitField('Crear Post')

class CommentForm(FlaskForm):
    comment_text = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Comentar')
