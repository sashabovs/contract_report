#!/usr/bin/env python3

import json

import flask
import psycopg
from psycopg.rows import dict_row
from flask import request

import bcrypt

import jwt

app = flask.Flask(__name__, static_url_path="", static_folder="static")

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

@app.route("/load-templates")
def load_templates():
    with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contract_report.contract_templates")
            rows = cur.fetchall()

    return json.dumps(rows)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("select password, role from contract_report.users where login=%(login)s",{'login':data['login']})

            rows = cur.fetchall()
            if not rows:
                return flask.Response(
                    f"Login {data['login']} is not found",
                    status=401,
                    )

            if not check_password(data['password'], rows[0]['password']):
                return flask.Response(
                    f"Incorrect password for {data['login']}",
                    status=401,
                )

            role = rows[0]['role']

    encoded = jwt.encode({"login": data["login"], "role": role}, JWT_SECRET, algorithm="HS256")
    return {"token": encoded}

@app.route("/users")
def get_users():
    with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, full_name, job_title_id as job_title, cathedra_id as cathedra, role, login, email FROM contract_report.users"
                        )
            rows = cur.fetchall()

    return json.dumps(rows)

@app.route("/users/<id>")
def get_user(id):
    with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, full_name, job_title_id as job_title, cathedra_id as cathedra, role, login, email 
                FROM contract_report.users 
                where id = %(id)s""",
                {'id': id})
            rows = cur.fetchall()
            if not rows:
                return flask.Response(
                    f"User with id {id} is not found",
                    status=401,
                    )
    return json.dumps(rows[0])


