#!/usr/bin/env python3
import datetime
import json
import flask
import requests
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(model.ParameterUnits).order_by(
            model.ParameterUnits.name
        )
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = (
            sqlalchemy.select(
                model.Parameters, model.ParameterUnits.name, model.Users.full_name
            )
            .join(model.Parameters.unit, isouter=True)
            .join(model.Parameters.inspector, isouter=True)
        )
        rows = session.execute(stmt).all()
        mapping = [row._mapping["Parameters"] for row in rows]

        return json.dumps(
            [
                {
                    "id": row.id,
                    "name": row.name,
                    "unit_id": row.unit_id,
                    # "inspector_id": row.inspector_id,
                    "unit": row.unit.name,
                    "inspector": {
                        "id": row.inspector_id,
                        "full_name": row.inspector.full_name,
                    },
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
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
    if not data.get("inspector") or not data["inspector"].get("id"):
        error += "Empty inspector. "
    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    # contract_templates = model.ContractTemplates(id=id, name=data["name"])
    session.query(model.Parameters).filter(model.Parameters.id == id).update(
        {
            model.Parameters.name: data["name"],
            model.Parameters.unit_id: data["unit_id"],
            model.Parameters.inspector_id: data["inspector"]["id"],
        }
    )
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.query(model.Parameters).filter(model.Parameters.id == id).delete()
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
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
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
    if not data.get("inspector") or not data["inspector"].get("id"):
        error += "Empty inspector. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    parameter = model.Parameters(
        name=data["name"], unit_id=data["unit_id"], inspector_id=data["inspector"]["id"]
    )
    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.add(parameter)
    session.commit()

    return flask.Response(status=200)


# //////////////


@head_of_human_resources_app.route("/inspection-periods")
def get_inspection_periods():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(model.InspectionPeriods)
        rows = session.execute(stmt).all()
        mapping = [row._mapping["InspectionPeriods"] for row in rows]

        return json.dumps(
            [
                {
                    "id": row.id,
                    "name": row.name,
                }
                for row in mapping
            ]
        )


@head_of_human_resources_app.route("/parameters-in-template/<int:id>")
def get_parameters_in_template(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(model.ParametersTemplates).where(
            model.ParametersTemplates.template_id == id
        )
        rows = session.execute(stmt).all()
        mapping = [row._mapping["ParametersTemplates"] for row in rows]

        return json.dumps(
            [
                {
                    "id": row.id,
                    "template_id": row.template_id,
                    "parameter": {"id":row.parameter_id, "name":row.parameter.name},
                    "needs_inspection": row.needs_inspection,
                    "inspection_period_id": row.inspection_period_id,
                    "requirement": row.requirement,
                    "points_promised": row.points_promised,
                    "template_name": row.template.name,
                    # "parameter_name": row.parameter.name,
                    "inspection_period_name": row.inspection_period.name,
                }
                for row in mapping
            ]
        )


@head_of_human_resources_app.route("/parameters-in-template/<int:id>", methods=["PUT"])
def edit_parameter_in_template(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""

    if not data.get("parameter") or not data["parameter"].get("id"):
        error += "Empty parameter. "
    if data.get("needs_inspection") is None:
        error += "Empty need_inspection. "
    if not data.get("inspection_period_id"):
        error += "Empty inspection period. "
    if not data.get("requirement"):
        error += "Empty requirement. "
    if not data.get("points_promised"):
        error += "Empty points_promised. "
    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    # contract_templates = model.ContractTemplates(id=id, name=data["name"])
    session.query(model.ParametersTemplates).filter(
        model.ParametersTemplates.id == id
    ).update(
        {
            model.ParametersTemplates.parameter_id: data["parameter"]["id"],
            model.ParametersTemplates.needs_inspection: data["needs_inspection"],
            model.ParametersTemplates.inspection_period_id: data[
                "inspection_period_id"
            ],
            model.ParametersTemplates.requirement: data["requirement"],
            model.ParametersTemplates.points_promised: data["points_promised"],
        }
    )
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route(
    "/parameters-in-template/<int:id>", methods=["DELETE"]
)
def delete_parameter_in_template(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.query(model.ParametersTemplates).filter(
        model.ParametersTemplates.id == id
    ).delete()
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/parameters-in-template", methods=["POST"])
def save_parameter_in_template():
    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("template_id"):
        error += "Empty template. "
    if not data.get("parameter") or not data["parameter"].get("id"):
        error += "Empty parameter. "
    if not data.get("inspection_period_id"):
        error += "Empty inspection period. "
    if data.get("needs_inspection") is None:
        error += "Empty need_inspection. "
    if not data.get("requirement"):
        error += "Empty requirement. "
    if not data.get("points_promised"):
        error += "Empty points_promised. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    parameter = model.ParametersTemplates(
        template_id=data["template_id"],
        parameter_id=data["parameter"]["id"],
        inspection_period_id=data["inspection_period_id"],
        needs_inspection=data["needs_inspection"],
        requirement=data["requirement"],
        points_promised=data["points_promised"],
    )
    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.add(parameter)
    session.commit()

    return flask.Response(status=200)


# ////////////////////////


@head_of_human_resources_app.route("/teachers-without-contract")
def get_teachers_without_contract():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = (
            sqlalchemy.select(model.Users)
            .where(model.Users.role == db_utils.Role.TEACHER.value)
            .where(model.Users.id != model.Contracts.user_id)
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


@head_of_human_resources_app.route("/contracts")
def get_contracts():
    params_user_id = flask.request.args.get("user_id")
    params_is_active = flask.request.args.get("is_active")

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [db_utils.Role.HEAD_OF_HUMAN_RESOURCES, db_utils.Role.TEACHER], role
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(model.Contracts)
        if params_user_id:
            stmt = stmt.where(model.Contracts.user_id == params_user_id)
        if params_is_active == True:
            stmt = stmt.where(model.Contracts.valid_till >= datetime.date.today())
        stmt = stmt.order_by(model.Contracts.signing_date)
        rows = session.execute(stmt).all()
        mapping = [row._mapping["Contracts"] for row in rows]

        return json.dumps(
            [
                {
                    "id": row.id,
                    "name": row.user.full_name +'('+ str(row.valid_from)+ '-' + str(row.valid_till) +')',
                    "user": {"id":row.user_id,"full_name":row.user.full_name},
                    "signing_date": str(row.signing_date),
                    "valid_from": str(row.valid_from),
                    "valid_till": str(row.valid_till),
                    "template_id": row.template_id,
                    "required_points": row.required_points,
                    # "user_name": row.user.full_name,
                    "template_name": row.template.name,
                }
                for row in mapping
            ]
        )


@head_of_human_resources_app.route("/contracts/<int:id>", methods=["PUT"])
def edit_contracts(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""

    if not data.get("user") or not data["user"].get("id"):
        error += "Empty user. "
    if not data.get("signing_date"):
        error += "Empty signing_date. "
    if not data.get("valid_from"):
        error += "Empty valid from. "
    if not data.get("valid_till"):
        error += "Empty valid till. "
    if not data.get("template_id"):
        error += "Empty template. "
    if not data.get("required_points"):
        error += "Empty required_points. "
    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    # contract_templates = model.ContractTemplates(id=id, name=data["name"])
    session.query(model.Contracts).filter(model.Contracts.id == id).update(
        {
            model.Contracts.user_id: data["user"]["id"],
            model.Contracts.signing_date: data["signing_date"],
            model.Contracts.valid_from: data["valid_from"],
            model.Contracts.valid_till: data["valid_till"],
            model.Contracts.template_id: data["template_id"],
            model.Contracts.required_points: data["required_points"],
        }
    )
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/contracts/<int:id>", methods=["DELETE"])
def delete_contract(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.query(model.Contracts).filter(model.Contracts.id == id).delete()
    session.commit()

    return flask.Response(status=200)


@head_of_human_resources_app.route("/contracts", methods=["POST"])
def save_contract():
    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.HEAD_OF_HUMAN_RESOURCES], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("user") or not data["user"].get("id"):
        error += "Empty user. "
    if not data.get("signing_date"):
        error += "Empty signing_date. "
    if not data.get("valid_from"):
        error += "Empty valid from. "
    if not data.get("valid_till"):
        error += "Empty valid till. "
    if not data.get("template_id"):
        error += "Empty template. "
    if not data.get("required_points"):
        error += "Empty required_points. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    contract = model.Contracts(
        user_id=data["user"]["id"],
        signing_date=data["signing_date"],
        valid_from=data["valid_from"],
        valid_till=data["valid_till"],
        template_id=data["template_id"],
        required_points=data["required_points"],
    )
    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    session.add(contract)
    session.commit()

    return flask.Response(status=200)
