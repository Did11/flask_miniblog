from flask import render_template, redirect, url_for, flash, send_from_directory, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, photos
from app.models import Usuario, Post, Comentario, comentarios_like
from app.forms import UpdateProfileForm
from .forms import RegistrationForm, LoginForm
from flask_uploads import UploadSet, configure_uploads, IMAGES


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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

        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()  # Instancia el formulario

    if form.validate_on_submit():  # Si el formulario es válido al hacer POST
        user = Usuario.query.filter_by(username=form.username.data).first()  # Usa el formulario para obtener datos
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')

    return render_template('auth/login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('index'))

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash('Título y contenido son obligatorios.')
            return redirect(url_for('create_post'))
        
        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        
        flash('Post creado exitosamente.')
        return redirect(url_for('index'))
    
    return render_template('create_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.id != current_user.id:
        flash('No tienes permiso para editar este post.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        
        if not post.title or not post.content:
            flash('Título y contenido son obligatorios.')
            return redirect(url_for('edit_post', post_id=post_id))
        
        db.session.commit()
        flash('Post editado exitosamente.')
        return redirect(url_for('index'))
    
    return render_template('edit_post.html', post=post)


@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
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
    posts = Post.query.order_by(Post.date_created.desc()).all()
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

    if request.method == 'POST' and current_user.is_authenticated:
        texto = request.form['comment_text']
        if texto:
            comment = Comentario(texto=texto, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Comentario agregado exitosamente.')

    return render_template('post_detail.html', post=post, comments=comments)

@app.route('/comment/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comentario.query.get_or_404(comment_id)
    if current_user in comment.liked_by:
        comment.liked_by.remove(current_user)
        db.session.commit()
        flash('Ya no te gusta este comentario.')
    else:
        comment.liked_by.append(current_user)
        db.session.commit()
        flash('Te gusta este comentario.')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        if form.avatar.data:
            # Aquí guardamos la imagen y obtenemos su nombre
            filename = photos.save(form.avatar.data)
            
            # Aquí asignamos ese nombre de archivo al avatar del usuario actual
            current_user.avatar_filename = filename
            
            # Luego, guardamos los cambios en la base de datos
            db.session.commit()
            
            flash('Tu perfil ha sido actualizado!', 'success')
            return redirect(url_for('profile'))
    
    # Si no hay datos POST, o si hay errores en el formulario, mostramos la página de perfil
    if current_user.avatar_filename:
        image_url = url_for('uploaded_file', filename='profile_images/' + current_user.avatar_filename)
    else:
        image_url = url_for('static', filename='images/default_images/default_avatar.png')
    
    return render_template('profile.html', form=form, image_url=image_url)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)
