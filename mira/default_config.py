"""This module defines the default configuration for Mira."""

DB_CONNECTION = {
    "dialect": "postgresql",
    "driver": "psycopg2",
    "dbname": "mira",
    "host": "localhost",
    "port": 5432,
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_HTTPONLY= True
