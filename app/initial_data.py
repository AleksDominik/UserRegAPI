import logging

from db.init_db import init_scheme
from db.session import DbConnexionHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = DbConnexionHandler()
    init_scheme(db)
    db.commit()
    db.close( )


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
