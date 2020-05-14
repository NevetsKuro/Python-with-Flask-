from .. import db

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<User : %r>' % self.username
    
class PersonalDetails(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    education = db.Column(db.String(50), nullable=False)
    exp = db.Column(db.String(10), nullable=False)
    is_athelete= db.Column(db.Boolean, default=False, nullable=False)
    hobbies = db.Column(db.String(70), nullable=False)
    log_user = db.relationship('Users', backref='personalDetails', lazy='dynamic')

    def __repr__(self):
        return '<Personal Details of  \'%s\'>' % self.full_name
    