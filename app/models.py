from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

login = LoginManager()


def config(app):
    db.init_app(app)
    app.db = db

    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Faça login para acessar esta página.'
    login.login_message_category = 'info'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tarefas = db.relationship('Tarefas', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    def set_password(self, password):
        """Gera um hash de senha para o usuário"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha é válida"""
        return check_password_hash(self.password_hash, password)


class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    type = db.Column(db.Text)
    priority = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Tarefas {self.title}>'