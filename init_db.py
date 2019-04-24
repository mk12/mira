"""This script initializes the Mira database."""

import sys

from mira.database import db, is_db_running
import mira.models


def main():
    if not is_db_running():
        print("ERROR: database is not running")
        sys.exit(1)
    db.create_all()


main()
