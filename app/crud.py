
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
# from sqlalchemy.orm import Session
from schemas import *
from core.security import get_password_hash,verify_password
from db.session import DbConnexionHandler
from utils_ import generate_password, send_new_account_email
from datetime import datetime
from core.config import settings

class CRUDUser():
    time_format='%y/%m/%d %H:%M:%S'
    # field_ordered=['id', 'email', 'is_active', 'hashed_password','time_created', 'time_updated' ]

    def __init__(self, model: User):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).(minimal implementation for the test)

        **Parameters**

        * `model`: a pydantic object
        """
        self.model = model
        
    def __formater__(self,type:str, iter):
        """
        field or values
        """
        if type=='fields':
            return ','.join(iter)
        elif type=='values':
            return ','.join([k if isinstance(k,int) else f"\'{k}\'" for k in iter]) # for our column it will be fine 
    def get(self, db: DbConnexionHandler, id: int) -> User:
        """
        
        """
        results= db.execute(f"select {self.__formater__(type='fields',iter=UserInDB.__fields__.keys()) } from users where id={id}")

        results=[dict(zip(UserInDB.__fields__.keys(),k))  for k in results]
        # print(results[0])
        results=[UserInDB(**k) for k in results]
        return results
    def get_by_email(self, db: DbConnexionHandler, email:str)-> User:


        results= db.execute(f"select {self.__formater__(type='fields',iter=UserInDB.__fields__.keys()) } from users where email=\'{email}\'")
        results=[dict(zip(UserInDB.__fields__.keys(),k))  for k in results]
        # print(results)
        results=[UserInDB(**k) for k in results]
        
        return results
    def create(self, db: DbConnexionHandler, obj_in:UserCreate):
        """
        
        #TODO: Adapt insertion string to the scheme format
        """
        obj_in_data=jsonable_encoder(obj_in)
        obj_in_data['time_created']=datetime.now()
        user=self.get_by_email(db=db, email=obj_in.email)
        if len(user)>0:
            print('user already exist')
            return -1
        clear_password=generate_password()
        password=get_password_hash(clear_password) 
        db.execute(f"INSERT INTO users  ( email, password, is_active,time_created ) values (\'{obj_in_data['email']}\',\'{password}\', \'False\', \'{obj_in_data['time_created']}\' )")
        db.commit()
        if settings.EMAILS_ENABLED and obj_in.email:
            send_new_account_email(email_to=obj_in.email,password=clear_password)
        ob_r=UserUpdate(password=clear_password,**obj_in_data)
        return ob_r

    def active_user( self,db:DbConnexionHandler, user:UserBase):
        obj_in_data=jsonable_encoder(user)
        obj_in_data['time_updated']=datetime.now()
        db.execute(f''' 
            
            update users set is_active=True where id=\'{obj_in_data['id']}\'

            ''')
        db.commit()
        user.is_active=True
        return user
    def is_active( self, obj_in):
        d=jsonable_encoder(obj_in)
        return d['is_active']
    def authenticate(self, db: DbConnexionHandler, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if len( user)==0:
            return None
        if not verify_password(password, user[0].password):
            return None
        return user[0]
    def can_be_activate(self, user:UserInDB, db=DbConnexionHandler,):
        user_data=jsonable_encoder(user)
        print(f"the user has been created {user_data['time_created']}")
        print((datetime.now()-user.time_created).total_seconds())
        if (datetime.now()-user.time_created).total_seconds()<settings.TIME_ACTIVATION_SECONDS:
            return True
        else: 
            return False

user=CRUDUser(User)