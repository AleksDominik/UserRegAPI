import pytest 
from db.session import DbConnexionHandler
import crud
from schemas import UserCreate, UserInDB
from utils import generate_random_user
import string, random

def test_user_creation(db:DbConnexionHandler):
    
    user=generate_random_user()
    crud.user.create(db=db, obj_in=user)


def test_user_retrieval(db:DbConnexionHandler):
    s= crud.user.get(db=db, id=1)
    print(s)
    email_test= ''.join(random.choices(string.ascii_letters, k=4))+ '@test.com'
    password_test=''.join(random.choices(string.digits, k=4))
    crud.user.create(db=db, obj_in=UserCreate(email=email_test, password=password_test))
    l=crud.user.get_by_email(db=db,email=email_test)
    assert len(l)>0
    assert isinstance(l[0],UserInDB)
    one= crud.user.get(db=db, id=1)
    assert len(one)>0
