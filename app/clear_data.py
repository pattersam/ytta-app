import logging

from app.db.init_db import clear_db
from app.db.session import SessionLocal

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
