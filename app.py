#!/usr/bin/env python3

import flask
from flask import request
import sqlalchemy
import jwt
import contract_report_model as model
import db_utils
from admin import admin_app
from reports import reports_app
from data_reports import data_reports_app
from head_of_human_resources import head_of_human_resources_app
import token_utils

app = flask.Flask(__name__, static_url_path="", static_folder="static")
app.register_blueprint(head_of_human_resources_app)
app.register_blueprint(admin_app)
app.register_blueprint(reports_app)
app.register_blueprint(data_reports_app)

@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(model.Users).where(model.Users.login == data["login"])
        users = session.scalars(stmt).first()

        if not users:
            return flask.Response(
                f"Login {data['login']} is not found",
                status=401,
            )

        if not db_utils.check_password(data["password"], users.password):
            return flask.Response(
                f"Incorrect password for {data['login']}",
                status=401,
            )

        role = users.role
        user_id = users.id
        cathedra_id=users.cathedra_id

        encoded = jwt.encode(
            {
                "login": data["login"],
                "role": role,
                "user_id": user_id,
                "cathedra_id": cathedra_id,
            },
            token_utils.JWT_SECRET,
            algorithm="HS256",
        )
        return {"token": encoded}
