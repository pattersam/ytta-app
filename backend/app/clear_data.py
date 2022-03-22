# HACK to make this script work while this isn't a proper python package...
import sys
sys.path[:0] = ['.']


from app.db.init_db import clear_db
from app.db.session import SessionLocal


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear() -> None:
    db = SessionLocal()
    clear_db(db, dry_run=False)


def main() -> None:
    logger.info("Deleting data")
    clear()
    logger.info("Data deleted")


if __name__ == "__main__":
    main()
