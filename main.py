from scrapy_tool.scrapy_req import My_Spider 
from flask import Flask, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.utils import _security, hash_password, _pwd_context, get_hmac

#from database import db
#from model.Tables import User, db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\sqlite3\\test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'thisisnotsalt'

db = SQLAlchemy(app)


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    pd = db.relationship('PersonalDetails', backref="details")#, lazy='dynamic')
        
    def __repr__(self):
        return '<User : %r>' % self.email
    
class PersonalDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    education = db.Column(db.String(50), nullable=False)
    exp = db.Column(db.String(10), nullable=False)
    is_athelete= db.Column(db.Boolean, default=False, nullable=False)
    hobbies = db.Column(db.String(70), nullable=False)
    #uid = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Personal Details of  \'%s\'>' % self.full_name

#class User(db.Model)
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(40), nullable=False)
#    password = db.Column(db.String(40), nullable=False)
    

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
#@app.before_first_request
#def create_user():
with app.app_context():
    #recreate the db file
    db.drop_all()
    db.create_all()
    #insert statements
    #user_datastore.create_user(email='Steven', password='1234')
    user1 = User(id='201', email='Midoriya', password=hash_password('password'))
    user4 = User(id='205', email='Steven', password=hash_password('1234'))
    #user1 = db.session.query.filter_by(email='Steven').get()
    db.session.add(user4)
    userDetails1 = PersonalDetails(id='1', full_name='Deku Midoriya', age='16', gender='male', address='Mumbai', education='Graduate', exp='1+ yrs', 
                            is_athelete=True, hobbies='Movies and Music', details=user1)
    userDetails2 = PersonalDetails(id='2', full_name='Steven Fernandes', age='23', gender='Male', address='Mumbai, India', education='Graduate', exp='1+ yrs', 
                            is_athelete=True, hobbies='Movies and Music', details=user4)
    db.session.add(userDetails1)
    db.session.add(userDetails2)
    db.session.commit()


#records = User.query.filter_by(username='Midoriya').first()
#records1 = PersonalDetails.query.filter_by(id='1').first()
#app.logger.info('{} logged in'.format(records.username))
#app.logger.info('{} logged in as '.format(records1.full_name))

spider = My_Spider()

@app.route('/',defaults={"err": ""})
@app.route('/<err>')
def loginPage(err):
    return render_template('index.html',err=err)
    
@app.route('/Home',methods=['POST','GET'])
def loginAuth():
    error = None

    if request.method == 'POST':
        userInput = request.form['user_input']
        pwd = request.form['pwd']
        user = User.query.filter_by(email=userInput).first()
        if user.email:
            password = pwd
            if _security.password_hash != 'plaintext':
                password = get_hmac(password)
            if userInput == user.email and  _pwd_context.verify(get_hmac(pwd), user.password):
                userDetails = PersonalDetails.query.filter_by(details=user).first()
                return render_template('index.html', teaminfo = spider.teamInfo(), teamtab = spider.parseTeamPos(), virus = spider.caronaInfo(), temp = spider.parseTemp(), user = user, userDetails = userDetails)
            else:
                error = 'Invalid credentials'
    return render_template('login.html',err = error)
    

@app.route('/logout',methods=['GET'])
def logout():
    return redirect(url_for('login'))

app.add_url_rule('/', 'Home', loginAuth)
app.add_url_rule('/', 'logout', logout)

if __name__ == '__main__':
   app.run()