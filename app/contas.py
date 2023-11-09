from app import db, bcrypt
from app.models import Usuario

# Asegúrate de que tu entorno virtual está activo y que has importado todo correctamente

def update_passwords():
    users = Usuario.query.all()
    for user in users:
        # Genera un nuevo hash de contraseña usando bcrypt
        hashed_password = bcrypt.generate_password_hash('tu_nueva_contraseña').decode('utf-8')
        user.bcrypt_password_hash = hashed_password
        db.session.add(user)
    db.session.commit()

# Ejecuta la función
update_passwords()