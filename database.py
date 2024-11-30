import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlmodel import SQLModel, create_engine, Session
from constants import *

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL, echo=True)


# connection postgres
def create_database_if_not_exists():
    try:

        conn = psycopg2.connect(
            dbname="postgres",
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            charset='utf8mb4'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # check db
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'")
        exists = cursor.fetchone()

        # not exists create
        if not exists:
            cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
            print(f"Database {DATABASE_NAME} created successfully.")
        else:
            print(f"Database {DATABASE_NAME} already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")


# create table
def create_db_and_tables():
    create_database_if_not_exists()
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)


# manage session
def get_session():
    engine = create_engine(DATABASE_URL, echo=True)

    with Session(engine) as session:
        yield session
