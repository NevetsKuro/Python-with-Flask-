from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(Base, UserMixin):
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
    
class PersonalDetails(Base):
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
