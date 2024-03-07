#!/usr/bin/env python3

import json

import flask
import psycopg
from psycopg.rows import dict_row
from flask import request

import bcrypt

import sqlalchemy

import jwt
import contract_report_model as model
import contract_report_table_model as table_model
from sqlalchemy.dialects.postgresql import insert

app = flask.Flask(__name__, static_url_path="", static_folder="static")
engine_reader = sqlalchemy.create_engine(
    "postgresql+psycopg://contract_report_reader:123@localhost:5432/contract_report",
    echo=True,
)
engine_writer = sqlalchemy.create_engine(
    "postgresql+psycopg://contract_report_writer:123@localhost:5432/contract_report",
    echo=True,
)

routes = []
JWT_SECRET = "secret"


@app.route("/")
def index():
    return app.send_static_file("index.html")


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


# @app.route("/load-templates")
# def load_templates():
#     with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
#         with conn.cursor() as cur:
#             cur.execute("SELECT * FROM contract_report.contract_templates")
#             rows = cur.fetchall()
#
#     return json.dumps(rows)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    session = sqlalchemy.orm.Session(engine_reader)

    stmt = sqlalchemy.select(model.Users).where(model.Users.login == data["login"])
    users = session.scalars(stmt).first()

    if not users:
        return flask.Response(
            f"Login {data['login']} is not found",
            status=401,
        )

    if not check_password(data["password"], users.password):
        return flask.Response(
            f"Incorrect password for {data['login']}",
            status=401,
        )

    role = users.role

    encoded = jwt.encode(
        {"login": data["login"], "role": role}, JWT_SECRET, algorithm="HS256"
    )
    return {"token": encoded}


@app.route("/users")
def get_users():
    session = sqlalchemy.orm.Session(engine_reader)
    stmt = (
        sqlalchemy.select(
            model.Users.id,
            model.Users.full_name,
            model.JobTitles.name,
            model.Cathedras.name,
            model.Users.role,
            model.Users.login,
            model.Users.email,
        )
        .join(model.Users.job_title, isouter=True)
        .join(model.Users.cathedra, isouter=True)
    )
    rows = session.execute(stmt).all()

    return json.dumps(
        [
            {
                "id": row[0],
                "full_name": row[1],
                "job_title": row[2],
                "cathedra": row[3],
                "role": row[4],
                "login": row[5],
                "email": row[6],
            }
            for row in rows
        ]
    )

@app.route("/cathedras")
def get_cathedras():
    session = sqlalchemy.orm.Session(engine_reader)
    stmt = (
        sqlalchemy.select(
            model.Cathedras
        )
    )

    rows = session.execute(stmt).all()
    mapping = [row._mapping["Cathedras"] for row in rows]

    return json.dumps(
        [
            {
                "id": row.id,
                "name": row.name,
            }
            for row in mapping
        ]
    )

@app.route("/job_titles")
def get_job_titles():
    session = sqlalchemy.orm.Session(engine_reader)
    stmt = (
        sqlalchemy.select(
            model.JobTitles
        )
    )

    rows = session.execute(stmt).all()
    mapping = [row._mapping["JobTitles"] for row in rows]

    return json.dumps(
        [
            {
                "id": row.id,
                "name": row.name,
            }
            for row in mapping
        ]
    )

@app.route("/users/<id>")
def get_user(id):
    session = sqlalchemy.orm.Session(engine_reader)
    stmt = (
        sqlalchemy.select(
            model.Users.id,
            model.Users.full_name,
            model.Users.job_title_id,
            model.Users.cathedra_id,
            model.Users.role,
            model.Users.login,
            model.Users.email,
        ).where(model.Users.id == id)
    )

    row = session.execute(stmt).first()
    if not row:
        return flask.Response(
            f"User with id {id} is not found",
            status=401,
        )

    return json.dumps(
        {
            "id": row[0],
            "full_name": row[1],
            "job_title_id": row[2],
            "cathedra_id": row[3],
            "role": row[4],
            "login": row[5],
            "email": row[6],
        }
    )


@app.route("/users/<id>", methods=["POST"])
def save_user(id):
    data = request.get_json()

    if data["password"]:
        new_pass = get_hashed_password(data["password"])
    else:
        session = sqlalchemy.orm.Session(engine_reader)
        stmt = sqlalchemy.select(model.Users.password).where(model.Users.id == id)

        row = session.execute(stmt).first()
        if not row:
            return flask.Response(
                f"Password required for new user",
                status=400,
            )
        new_pass = row[0]

    user = model.Users(
        id=data["user"]["id"],
        full_name=data["user"]["full_name"],
        job_title_id=data["user"]["job_title_id"],
        cathedra_id=data["user"]["cathedra_id"],
        role=data["user"]["role"],
        login=data["user"]["login"],
        email=data["user"]["email"],
        password=new_pass,
    )
    session = sqlalchemy.orm.Session(engine_writer)
    session.add(user)
    session.commit()


    return flask.Response(status=200)
