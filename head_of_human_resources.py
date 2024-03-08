#!/usr/bin/env python3

import json
import flask
import sqlalchemy
import contract_report_model as model
import db_utils
import token_utils

head_of_human_resources_app = flask.Blueprint("head_of_human_resources_app", __name__)


@head_of_human_resources_app.route("/units")
def get_units():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(model.ParameterUnits)
    rows = session.execute(stmt).all()
    mapping = [row._mapping["ParameterUnits"] for row in rows]

    return json.dumps(
        [
            {
                "id": row.id,
                "name": row.name,
            }
            for row in mapping
        ]
    )


@head_of_human_resources_app.route("/inspectors")
def get_inspectors():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(model.Users).where(
        model.Users.role == db_utils.Role.INSPECTOR.value
    )
    rows = session.execute(stmt).all()
    mapping = [row._mapping["Users"] for row in rows]

    return json.dumps(
        [
            {
                "id": row.id,
                "full_name": row.full_name,
            }
            for row in mapping
        ]
    )


@head_of_human_resources_app.route("/contract-templates")
def get_contract_templates():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(model.ContractTemplates)
    rows = session.execute(stmt).all()
    mapping = [row._mapping["ContractTemplates"] for row in rows]

    return json.dumps(
        [
            {
                "id": row.id,
                "name": row.name,
            }
            for row in mapping
        ]
    )


@head_of_human_resources_app.route("/contract-templates/<int:id>", methods=["PUT"])
def edit_contract_template(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("name"):
        error += "Empty name. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    # contract_templates = model.ContractTemplates(id=id, name=data["name"])
    session.query(model.ContractTemplates).filter(
        model.ContractTemplates.id == id
    ).update({model.ContractTemplates.name: data["name"]})
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/contract-templates/<int:id>", methods=["DELETE"])
def delete_contract_template(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.query(model.ContractTemplates).filter(
        model.ContractTemplates.id == id
    ).delete()
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/contract-templates", methods=["POST"])
def save_contract_template():
    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("name"):
        error += "Empty name. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    contract_templates = model.ContractTemplates(name=data["name"])
    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.add(contract_templates)
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/parameters")
def get_parameters():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_reader)
    stmt = sqlalchemy.select(model.Parameters, model.ParameterUnits.name, model.Users.full_name).join(model.Parameters.unit, isouter=True).join(model.Parameters.inspector, isouter=True)
    rows = session.execute(stmt).all()
    mapping = [row._mapping["Parameters"] for row in rows]

    return json.dumps(
        [
            {
                "id": row.id,
                "name": row.name,
                "unit_id": row.unit_id,
                "inspector_id": row.inspector_id,
                "unit": row.unit.name,
                "inspector": row.inspector.full_name
            }
            for row in mapping
        ]
    )


@head_of_human_resources_app.route("/parameters/<int:id>", methods=["PUT"])
def edit_parameters(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("name"):
        error += "Empty name. "
    if not data.get("unit_id"):
        error += "Empty units. "
    if not data.get("inspector_id"):
        error += "Empty inspector. "
    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    # contract_templates = model.ContractTemplates(id=id, name=data["name"])
    session.query(model.Parameters).filter(
        model.Parameters.id == id
    ).update({model.Parameters.name: data["name"], model.Parameters.unit_id: data["unit_id"], model.Parameters.inspector_id: data["inspector_id"]})
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/parameters/<int:id>", methods=["DELETE"])
def delete_parameter(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.query(model.Parameters).filter(
        model.Parameters.id == id
    ).delete()
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/parameters", methods=["POST"])
def save_parameter():
    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(db_utils.Role.HEAD_OF_HUMAN_RESOURCES, role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("name"):
        error += "Empty name. "
    if not data.get("unit_id"):
        error += "Empty units. "
    if not data.get("inspector_id"):
        error += "Empty inspector. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    parameter = model.Parameters(name=data["name"], unit_id=data["unit_id"], inspector_id=data["inspector_id"])
    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.add(parameter)
    session.commit()

    return flask.Response(status=200)
