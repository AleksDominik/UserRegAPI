from db.session import DbConnexionHandler
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from db.session import DbConnexionHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def init_scheme(db: DbConnexionHandler):
    try:
        db.connect()
        # Try to create session to check if DB is awake
        db.execute('''
        create table if not exists public.users (
            id serial not null
            ,email varchar(80) not null unique
            ,is_active boolean not null
            , password varchar(90) not null
            ,time_created timestamp
            ,time_updated timestamp
            , CONSTRAINT user_id_pk PRIMARY KEY (id)
            )
        ''')
    except Exception as e:
        logger.error(e)
        raise e

