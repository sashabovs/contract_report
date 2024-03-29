#!/usr/bin/env python3
from contextlib import contextmanager
from enum import Enum, auto
import bcrypt
import sqlalchemy


engine_reader = sqlalchemy.create_engine(
    "postgresql+psycopg://contract_report_reader:123@localhost:5432/contract_report",
    echo=True,
)
engine_writer = sqlalchemy.create_engine(
    "postgresql+psycopg://contract_report_writer:123@localhost:5432/contract_report",
    echo=True,
)


class Role(Enum):
    ADMINISTRATOR = "administrator"
    HEAD_OF_HUMAN_RESOURCES = "head_of_human_resources"
    INSPECTOR = "inspector"
    TEACHER = "teacher"
    HEAD_OF_CATHEDRA = "head_of_cathedra"


class ReportTypes(Enum):
    EXECUTION_PROGRESS = "execution_progress"
    SIGNING_PROGRESS = "signing_progress"
    SIGNING_LOG = "signing_log"
    DATA_CHANGE_LOG = "data_change_log"


def get_reader_connection_string():
    return "host=localhost port=5432 dbname=contract_report user=contract_report_reader password=123"


def get_writer_connection_string():
    return "host=localhost port=5432 dbname=contract_report user=contract_report_writer password=123"


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt()).decode()


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())


@contextmanager
def auto_session(engine):
    sess = sqlalchemy.orm.Session(engine)
    try:
        yield sess
        sess.commit()
        # sess.refresh()
    except Exception as e:
        sess.rollback()
        raise e
    finally:
        sess.close()
