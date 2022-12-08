import psycopg2
from core.config import settings
import contextlib

class DbConnexionHandler():
    """
    Basic Session class
    """
    def __init__(self):
        self.cursor=False
        self.connexion=False

    def __create_connexion__(self):
        """
        :return: Connect and return connection object and close once execution finished
        """
        if not self.connexion:
            self.connexion = psycopg2.connect(
                    host=settings.POSTGRES_SERVER
                    ,user=settings.POSTGRES_USER
                    ,password=settings.POSTGRES_PASSWORD
                    ,dbname=settings.POSTGRES_DB
                )

            # self.connection = psycopg2.connect(host="localhost", database="cvims")
            self.connexion.set_session(autocommit=False)
            self.cursor = self.connexion.cursor()
    def connect(self):
        self.__create_connexion__()

    def commit(self):
        if self.connexion:
            self.connexion.commit()
        else:
            raise ValueError('The connexion is not initialized')
    def execute(self,query):
        self.cursor.execute(query)
        try :
            return self.cursor.fetchall()
        except Exception as e :
            print('Not fetchable')
        return -1
    def close(self):
        self.connexion.close()
    
    def add( obj):
        pass 
    def remove(obj):
        pass