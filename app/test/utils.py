
from utils_ import generate_password
from schemas import UserCreate
import string,secrets
import random
def generate_random_user():
    alphabet=string.ascii_letters
    email=''.join(secrets.choice(alphabet) for i in range(5))+'@'+''.join([secrets.choice(alphabet)for i in range(4)])+'.com'
    password=generate_password()
    return UserCreate(email=email, password=password)