from flask import render_template, flash, redirect, url_for, request, jsonify, Blueprint, make_response, g
from app import app, db, bcrypt
from app.forms import LoginForm, RegistrationForm, UpdateProfileForm, CreatePostForm, CommentForm
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash
from app.models import Usuario, Post, Comentario
from werkzeug.urls import url_parse
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

jwt = JWTManager(app)
users = Blueprint('users', __name__)

@app.before_request
def before_request():
    g.current_user = get_current_user()


@app.context_processor
def inject_user():
    try:
        return {'current_user': g.current_user}
    except AttributeError:
        # En caso de que g.current_user no esté definido, puedes decidir qué hacer
        # Por ejemplo, puedes devolver un usuario anónimo o None
        return {'current_user': None}


def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        if current_user_id:
            return Usuario.query.get(current_user_id)
    except (RuntimeError, NoAuthorizationError, ExpiredSignatureError, InvalidTokenError):
        # Si no hay un JWT válido, o si hay algún otro error relacionado con JWT, simplemente devolvemos None.
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = Usuario.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya existe. Elige otro.')
            return redirect(url_for('register'))

        new_user = Usuario(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        response = make_response(redirect(url_for('index')))  # Redirige a la página deseada
        set_access_cookies(response, access_token)  # Establece las cookies JWT
        return response

    return render_template('auth/register.html', form=form)


from flask import Response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificar si la solicitud es JSON
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            # Si no es JSON, asumir que es una solicitud de formulario
            username = request.form.get('username')
            password = request.form.get('password')

        user = Usuario.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.bcrypt_password_hash, password):
            access_token = create_access_token(identity=user.id)
            if request.is_json:
                # Respuesta para solicitudes de API
                return jsonify(access_token=access_token), 200
            else:
                # Respuesta para solicitudes de formulario web
                # Aquí manejarías la sesión del usuario y redirigirías
                return redirect(url_for('index'))
        else:
            if request.is_json:
                # Respuesta de error para solicitudes de API
                return jsonify({"msg": "Bad username or password"}), 401
            else:
                # Respuesta de error para solicitudes de formulario web
                return render_template('login.html', error="Bad username or password")
    else:
        # Método GET para mostrar el formulario de inicio de sesión
        return render_template('login.html')

@app.route('/logout')
@jwt_required()
def logout():
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)  # Usa esto para eliminar las cookies JWT
    return response

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route('/create_post', methods=['GET', 'POST'])
@jwt_required()
def create_post():
    form = CreatePostForm()
    current_user_id = get_jwt_identity()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, user_id=current_user_id)
        db.session.add(post)
        db.session.commit()
        flash('Post creado exitosamente.')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user_id = get_jwt_identity()
    if post.author.id != current_user_id:
        flash('No tienes permiso para editar este post.')
        return redirect(url_for('index'))
    form = UpdatePostForm(request.form)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post editado exitosamente.')
        return redirect(url_for('index'))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('edit_post.html', form=form, post=post)


@app.route('/delete_post/<int:post_id>', methods=['POST'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.id != current_user.id:
        flash('No tienes permiso para eliminar este post.')
        return redirect(url_for('index'))
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post eliminado exitosamente.')
    return redirect(url_for('index'))

@app.route('/posts')
def all_posts():
    # Obtener todas las publicaciones ordenadas por fecha de creación
    posts = Post.query.order_by(Post.date_created.desc()).all()

    # Obtener la cantidad de comentarios para cada publicación
    for post in posts:
        post.comments_count = Comentario.query.filter_by(post_id=post.id).count()

    return render_template('posts.html', posts=posts)

@app.route('/test')
def test():
    return render_template('base.html')

@app.route('/prueba')
def prueba():
    return render_template('prueba.html')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comentario.query.filter_by(post_id=post_id).order_by(Comentario.date_created.desc()).all()
    form = CommentForm()  # Crea una instancia del formulario

    if form.validate_on_submit() and current_user.is_authenticated:
        texto = form.comment_text.data
        if texto:
            comment = Comentario(texto=texto, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Comentario agregado exitosamente.')

    return render_template('post_detail.html', post=post, comments=comments, form=form)

@app.route('/comment/<int:comment_id>/like', methods=['POST'])
@jwt_required()
def like_comment(comment_id):
    current_user_id = get_jwt_identity()
    comment = Comentario.query.get_or_404(comment_id)
    user = Usuario.query.get(current_user_id)
    
    if user in comment.liked_by:
        comment.liked_by.remove(user)
    else:
        comment.liked_by.append(user)
    
    db.session.commit()
    flash('Tu reacción ha sido actualizada.')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = Usuario.query.get(current_user_id)
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            filepath = os.path.join(app.root_path, 'static/images/profile_images', filename)
            form.avatar.data.save(filepath)
            
            user.avatar_filename = filename
            db.session.commit()
            flash('Tu perfil ha sido actualizado!', 'success')
            return redirect(url_for('profile'))
    
    image_url = url_for('static', filename=f'images/profile_images/{user.avatar_filename}') if user.avatar_filename else url_for('static', filename='images/default_images/default_avatar.png')
    
    return render_template('profile.html', form=form, image_url=image_url)

@app.route('/profile_images/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'profile_images'), filename)

@app.route('/user/<string:username>')
def user_profile(username):
    user = Usuario.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)
