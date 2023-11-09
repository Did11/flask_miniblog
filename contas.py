from app import app, db, bcrypt
from app.models import Usuario

def update_passwords():
    with app.app_context():
        users = Usuario.query.all()
        for user in users:
            # Replace 'Passworduniversal11' with the password you want to set
            hashed_password = bcrypt.generate_password_hash('Passworduniversal11').decode('utf-8')
            user.bcrypt_password_hash = hashed_password
            db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    update_passwords()
