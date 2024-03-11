#!/usr/bin/env python3

import json
import flask
import sqlalchemy
import contract_report_model as model
import db_utils
import token_utils

admin_app = flask.Blueprint('admin_app', __name__)

@admin_app.route("/users")
def get_users():
    session = sqlalchemy.orm.Session(db_utils.engine_reader)
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


@admin_app.route("/roles")
def get_roles():
    roles = [role.value for role in db_utils.Role]
    return json.dumps(roles)

@admin_app.route("/job_titles")
def get_job_titles():
    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(model.JobTitles)

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

@admin_app.route("/cathedras")
def get_cathedras():
    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(model.Cathedras)

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

@admin_app.route("/users/<id>")
def get_user(id):
    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(
        model.Users.id,
        model.Users.full_name,
        model.Users.job_title_id,
        model.Users.cathedra_id,
        model.Users.role,
        model.Users.login,
        model.Users.email,
    ).where(model.Users.id == id)

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

@admin_app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.ADMINISTRATOR], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.query(model.Users).filter(model.Users.id == id).delete()
    session.commit()

    return flask.Response(status=200)


@admin_app.route("/users/<id>", methods=["POST"])
def save_user(id):
    # TODO: check if new user has the same id
    data = flask.request.get_json()

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.ADMINISTRATOR], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    if data["password"]:
        new_pass = db_utils.get_hashed_password(data["password"])
    else:
        session = sqlalchemy.orm.Session(db_utils.engine_reader)
        stmt = sqlalchemy.select(model.Users.password).where(model.Users.id == id)

        row = session.execute(stmt).first()
        if not row:
            return flask.Response(
                f"Password required for new user",
                status=400,
            )
        new_pass = row[0]

    error = ""
    if not data["user"].get("id"):
        error += "Empty id. "
    if not data["user"].get("full_name"):
        error += "Empty full_name. "
    if not data["user"].get("role"):
        error += "Empty role. "
    if not data["user"].get("login"):
        error += "Empty login. "
    if not data["user"].get("email"):
        error += "Empty email. "
    if not new_pass:
        error += "Empty password. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    new_user_role = data["user"].get("role")
    if new_user_role == db_utils.Role.TEACHER.value:
        if not data["user"].get("job_title_id"):
            error += "Empty job_title_id for teacher. "
        if not data["user"].get("cathedra_id"):
            error += "Empty cathedra_id for teacher. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    user = model.Users(
        id=data["user"]["id"],
        full_name=data["user"]["full_name"],
        job_title_id=(
            data["user"]["job_title_id"]
            if "job_title_id" in data["user"] and data["user"]["job_title_id"]
            else None
        ),
        cathedra_id=(
            data["user"]["cathedra_id"]
            if "cathedra_id" in data["user"] and data["user"]["cathedra_id"]
            else None
        ),
        role=data["user"]["role"],
        login=data["user"]["login"],
        email=data["user"]["email"],
        password=new_pass,
    )
    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.merge(user)
    session.commit()

    return flask.Response(status=200)
