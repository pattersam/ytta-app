# HACK to make this script work while this isn't a proper python package...
import sys
sys.path[:0] = ['.']


from app.db.init_db import init_db
from app.db.session import SessionLocal


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
