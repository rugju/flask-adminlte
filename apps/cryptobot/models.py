from apps import db, login_manager
from apps.exceptions.exception import InvalidUsage
from apps.authentication.models import Users
from google.cloud import datastore
from google.cloud.datastore.query import PropertyFilter
import enum

class Enums(enum.Enum):
    @classmethod
    def choices(cls):
        return [(choice.value, choice.value) for choice in cls]
class EnumTimePeriod(Enums):
    m1 = "1m"
    m5 = "5m"
    h1 = "1h"
    h2 = "2h"
# average_type': 'SMA',  # 'SMA', 'EMA', 'WMA', 'DCM' 
class EnumAverageType(Enums):
    SMA = 'SMA'
    EMA = 'EMA'
    WMA = 'WMA'
    DCM = 'DCM'
class EnumMarginMode(Enums):
    isolated = 'isolated'
    cross = 'cross'
class EnumSymbols(Enums):
    BTC = 'BTC/USDT:USDT'

class API():
    __tablename__ = 'crypto_api2'
    __entity__ = None #datastore.Entity(db.key( __tablename__ ))  

    def to_dict(self):
        return {
            "name": self.name,
            "apiKey": self.apiKey,
            "secret": self.secret,
            "password": self.password
        }

    def get_id(self):
        return self.__entity__.key.id_or_name

    def initFromDB(self, entity : datastore.Entity):
        self.__entity__ = entity
        for k in entity.keys():
            setattr(self, k, entity[k])
   
    def save(self, currentUser : Users) -> None:
        if self.__entity__ == None:
            parent_key = db.key(currentUser.__tablename__, currentUser.get_id())
            key = db.key(self.__tablename__ , self.name, parent=parent_key)
            self.__entity__ = datastore.Entity(key=key  )
        self.__entity__.update(self.to_dict())
        db.put(self.__entity__)

    """
        Get a list of API for the current user
    """
    @classmethod
    def getList(cls, currentUser : Users):
        query = db.query(kind=cls.__tablename__, ancestor = db.key(currentUser.__tablename__, currentUser.get_id()) )
        apis = []
        for res in list(query.fetch()):
            api = API()
            api.initFromDB(res)
            apis.append(api)
        return apis

    """
        Get a list of API key names for the current user *keys only
    """
    @classmethod
    def getListKeys(cls, currentUser : Users):
        query = db.query(kind=cls.__tablename__, ancestor = db.key(currentUser.__tablename__, currentUser.get_id()) )
        query.keys_only()
        return [res.key.name for res in list(query.fetch())]


    @classmethod
    def find_by_id(cls, id, currentUser : Users):
        complete_key = db.key(cls.__tablename__, id, parent = db.key(currentUser.__tablename__, currentUser.get_id()) )
        entity = db.get(complete_key) #datastore.Entity(key=complete_key)
        res = API() 
        res.initFromDB(entity)   
        return res
        #return cls.query.filter_by(id=_id).first()        

class StrategyParams():
    __tablename__ = 'StrategyParams'

    def __init__(self, formdata : dict = {}):
        if 'csrf_token' in formdata:
            del formdata['csrf_token']
        for k in formdata.keys():
            setattr(self, k, formdata[k])    

    def to_dict(self):
        keys = [i for i in dir(self) if not i.startswith('__')]
        return { k : getattr(self,k) for k in keys if not callable(getattr(self,k)) }

    def initFromDB(self, entity : datastore.Entity):
        self.__entity__ = entity
        for k in entity.keys():
            setattr(self, k, entity[k])

    def save(self, currentAPI : API= None, currentAPI_ID : str = None) -> None:
        if not hasattr(self, '__entity__') or self.__entity__ == None:
            parent_key = db.key(currentAPI.__tablename__, currentAPI.get_id()) if currentAPI else db.key(API.__tablename__, currentAPI_ID)
            key = db.key(self.__tablename__ , self.name, parent=parent_key)
            self.__entity__ = datastore.Entity(key=key)
        self.__entity__.update(self.to_dict())
        db.put(self.__entity__)

    @classmethod
    def getList(cls, currentAPI : API): 
        query = db.query(kind=cls.__tablename__, ancestor = db.key(currentAPI.__tablename__, currentAPI.get_id()) )
        apis = []
        for res in list(query.fetch()):
            api = StrategyParams()
            api.initFromDB(res)
            apis.append(api)
        return apis

    @classmethod
    def getListKeys(cls, currentAPI : API):
        query = db.query(kind=cls.__tablename__, ancestor = db.key(currentAPI.__tablename__, currentAPI.get_id()) )
        query.keys_only()
        return [res.key.name for res in list(query.fetch())]

    @classmethod
    def find_by_id(cls, id, currentAPI : API= None, currentAPI_ID : str = None):
        parent_key = db.key(currentAPI.__tablename__, currentAPI.get_id()) if currentAPI else db.key(API.__tablename__, currentAPI_ID)
        complete_key = db.key(cls.__tablename__, id, parent=parent_key )
        entity = db.get(complete_key) #datastore.Entity(key=complete_key)
        res = StrategyParams() 
        res.initFromDB(entity)   
        return res    
