from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings
import string, random,time
def test_user_creation(client: TestClient)-> None:
    create_data= {
        "email": f"{''.join( random.choices(string.ascii_letters,k=13))}@gmail.com", #cant be generated by crud test
    }
    r = client.post(f"{settings.API_STR}/user/", json=create_data)
    response=r.json()
    print(response)
    assert r.status_code==200
    user_email=response['email']
    user_password=response["password"]
    # time.sleep(0.3)
    authenticate_data={
        'username': user_email,
        'password': user_password
    }   
    r = client.post(f"{settings.API_STR}/login/access-token", data=authenticate_data)
    response=r.json()
    assert r.status_code==200
    #for slow user
def test_user_failed_auth( client:TestClient)->None:

    create_data= {
        "email": f"{''.join( random.choices(string.ascii_letters,k=13))}@gmail.com", #cant be generated by crud test
    }
    r = client.post(f"{settings.API_STR}/user/", json=create_data)
    response=r.json()
    print(response)
    assert r.status_code==200
    user_email=response['email']
    user_password=response['password']
    print(f'the time to wait {settings.TIME_ACTIVATION_SECONDS}')
    time.sleep( settings.TIME_ACTIVATION_SECONDS+4)
    authenticate_data={
        'username': user_email,
        'password': user_password
    }   
    r = client.post(f"{settings.API_STR}/login/access-token", data=authenticate_data)
    response=r.json()
    assert r.status_code!=200