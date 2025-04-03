from datetime import datetime

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    ip = db.Column(db.String(255))
    last_login_date = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_ip(self, ip):
        try:
            self.ip = ip
            self.last_login_date = datetime.now()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新失败: {str(e)}")
            return False

    def __repr__(self):
        return f'<User {self.username}>'