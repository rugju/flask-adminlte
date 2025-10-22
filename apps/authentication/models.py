# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

#from sqlalchemy.exc import SQLAlchemyError, IntegrityError
#from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager
from google.cloud import datastore
from google.cloud.datastore.query import PropertyFilter
from apps.authentication.util import hash_pass

class Users(UserMixin):

    __tablename__ = 'users'
    __entity__ = datastore.Entity(db.key( __tablename__ ))

    username      = ""
    email         = "" #db.Column(db.String(64), unique=True)
    password      = "" #str #db.Column(db.LargeBinary)
    bio           = "" #db.Column(db.Text(), nullable=True)
    password = ""
    oauth_github  = "" #db.Column(db.String(100), nullable=True)
    oauth_google  = "" #db.Column(db.String(100), nullable=True)

    readonly_fields = ["id", "username", "email", "oauth_github", "oauth_google"]

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "oauth_github": self.oauth_github,
            "oauth_google": self.oauth_google,
            "password": self.password
        }

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)
    def get_id(self):
        return self.__entity__.id

    def initFromDB(self, entity : datastore.Entity):
        self.__entity__ = entity
        #print ("==== ID=== ", entity.id)
        #print ("==== KEYS ===", entity)
        for k in entity.keys():
            #print (f"k {k} = {entity[k]}")
            setattr(self, k, entity[k])
    def __repr__(self):
        return str(self.username)

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        query = db.query(kind=cls.__tablename__)
        query.add_filter(filter=PropertyFilter('email', '=', email))
        res = list(query.fetch(1))
        return res[0] if res else None

    @classmethod
    def find_by_username(cls, username: str):
        query = db.query(kind=cls.__tablename__)
        query.add_filter(filter=PropertyFilter('username', '=', username))
        query_res = list(query.fetch(1))
        print("Result query_res (find_by_username): ", query_res)
        if query_res:
            res = Users() 
            res.initFromDB(query_res[0])
            return res
        else:
            return None
        #return cls.__init__(res[0]) if res else None
        #return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, id) -> "Users":
        complete_key = db.key(cls.__tablename__, id)
        #task = datastore.Entity(key=complete_key)
        entity = db.get(complete_key) #datastore.Entity(key=complete_key)
        res = Users() 
        res.initFromDB(entity)        
        return res
        #return cls.query.filter_by(id=_id).first()
   
    def save(self) -> None:
        try:
            self.__entity__.update(self.to_dict())
            db.put(self.__entity__)
 
        except Exception as e:
            print ("ERRPR", e, self.to_dict())
            #db.session.rollback()
            #db.session.close()
            #error = str(e.__dict__['orig'])
            #raise Exception(e, 422)
    
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise IntegrityError(error, 422)
        return

@login_manager.user_loader
def user_loader(id):
    print("user_loader id", id)
    u = Users.find_by_id(id=id)
    print ("Username", u.username)
    return u

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.find_by_username(username)
    return user if user else None

#class OAuth(OAuthConsumerMixin):
#    pass
    #user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=False)
    #user = db.relationship(Users)
