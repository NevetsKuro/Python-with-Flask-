from scrapy_tool.scrapy_req import My_Spider 
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from model.Tables import User, db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\sqlite3\\test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    pd = db.relationship('PersonalDetails', backref="details")#, lazy='dynamic')
    
    def __repr__(self):
        return '<User : %r>' % self.username
    
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

#recreate the db file
db.drop_all()
db.create_all()

#insert statements
user1 = User(id='201', username='Midoriya', password='password')
user2 = User(id='202', username='Rivane', password='password')
user3 = User(id='203', username='Kirito', password='password')
user4 = User(id='205', username='Steven', password='1234')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
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
    return render_template('login.html',err=err)
    
@app.route('/Home',methods=['POST','GET'])
def loginAuth():
    error = None

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['user_input']).first()
        if user.username:
            if request.form['user_input'] == user.username and request.form['pwd'] == user.password:
                userDetails = PersonalDetails.query.filter_by(details=user).first()
                return render_template('index.html', teaminfo = spider.teamInfo(), teamtab = spider.parseTeamPos(), virus = spider.caronaInfo(), temp = spider.parseTemp(), user = user, userDetails = userDetails)
            else:
                error = 'Invalid credentials'
    return render_template('login.html',err = error)
    #return('<h><strong> Access Denied </strong></h>')
    

app.add_url_rule('/', 'Home', loginAuth)

if __name__ == '__main__':
   app.run()