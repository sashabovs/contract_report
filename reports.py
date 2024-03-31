#!/usr/bin/env python3
import datetime
import json
import flask
import sqlalchemy
from sqlalchemy.sql.functions import coalesce

import contract_report_model as model
import db_utils
import token_utils
import base64

reports_app = flask.Blueprint("reports_app", __name__)


@reports_app.route("/reports")
def get_reports():
    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [
                db_utils.Role.TEACHER,
                db_utils.Role.HEAD_OF_CATHEDRA,
                db_utils.Role.INSPECTOR,
                db_utils.Role.HEAD_OF_HUMAN_RESOURCES,
            ],
            role,
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    params_user_id = flask.request.args.get("user_id")

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = (
            sqlalchemy.select(
                model.Reports.id,
                model.Reports.period_of_report,
                model.Reports.contract_id,
                model.Contracts.user_id,
                model.Users.full_name,
                model.Contracts.valid_from,
                model.Contracts.valid_till,
                model.Reports.signed_by_teacher,
                model.Reports.signed_by_head_of_cathedra,
                model.Reports.signed_by_head_of_human_resources,
            )
            .join(model.Reports.contract)
            .join(model.Users, onclause=model.Users.id == model.Contracts.user_id)
        )

        if role == db_utils.Role.TEACHER.value:
            stmt = stmt.where(model.Contracts.user_id == params_user_id)
        elif role == db_utils.Role.HEAD_OF_CATHEDRA.value:
            temp = sqlalchemy.select(model.Cathedras.id).where(
                model.Cathedras.head_id == params_user_id
            )
            cathedra = session.execute(temp).first()
            stmt = (
                stmt.where(model.Reports.signed_by_teacher == True)
                .where(model.Reports.signed_by_head_of_cathedra == False)
                .where(model.Users.cathedra_id == int(cathedra[0]))
            )
        elif role == db_utils.Role.HEAD_OF_HUMAN_RESOURCES.value:
            signed_by_inspectors_table = (
                session.query(
                    model.ReportedParameters.report_id,
                    sqlalchemy.func.min(
                        model.ReportedParameters.signed_by_inspector.cast(
                            sqlalchemy.Integer
                        )
                    )
                    .cast(sqlalchemy.Boolean)
                    .label("signed_by_inspector"),
                )
                .select_from(model.ReportedParameters)
                .group_by(model.ReportedParameters.report_id)
                .cte("signed_by_inspectors_table")
            )

            stmt = (
                stmt.join(
                    signed_by_inspectors_table,
                    signed_by_inspectors_table.c.report_id == model.Reports.id,
                )
                .where(model.Reports.signed_by_teacher == True)
                .where(model.Reports.signed_by_head_of_cathedra == True)
                .where(signed_by_inspectors_table.c.signed_by_inspector == True)
                .where(model.Reports.signed_by_head_of_human_resources == False)
            )

        rows = session.execute(stmt).all()

        stmt = (
            sqlalchemy.select(
                model.ReportedParameters.report_id,
                sqlalchemy.func.min(
                    model.ReportedParameters.signed_by_inspector.cast(
                        sqlalchemy.Integer
                    )
                )
                .cast(sqlalchemy.Boolean)
                .label("signed_by_inspector"),
            )
            .where(model.ReportedParameters.report_id.in_([row[0] for row in rows]))
            .group_by(model.ReportedParameters.report_id)
        )
        rows_signed_by_inspector = session.execute(stmt).all()
        signed_by_inspector_dict = {row[0]: row[1] for row in rows_signed_by_inspector}
        return json.dumps(
            [
                {
                    "id": row[0],
                    "period_of_report": str(row[1]),
                    "contract": {
                        "id": row[2],
                        "name": row[4] + "(" + str(row[5]) + "-" + str(row[6]) + ")",
                    },
                    "user_id": row[3],
                    "valid_from": str(row[5]),
                    "valid_till": str(row[6]),
                    "signed_by_teacher": row[7],
                    "signed_by_inspector": signed_by_inspector_dict.get(row[0], False),
                    "signed_by_head_of_cathedra": row[8],
                    "signed_by_head_of_human_resources": row[9],
                }
                for row in rows
            ]
        )


@reports_app.route("/reported-parameters")
def get_reported_parameters():
    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [
                db_utils.Role.TEACHER,
                db_utils.Role.HEAD_OF_CATHEDRA,
                db_utils.Role.INSPECTOR,
                db_utils.Role.HEAD_OF_HUMAN_RESOURCES,
            ],
            role,
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    params_report_id = flask.request.args.get("report_id", type=int)

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = (
            sqlalchemy.select(
                model.ReportedParameters.id,
                model.ReportedParameters.report_id,
                model.ReportedParameters.parameter_id,
                model.Parameters.name,
                model.ReportedParameters.done,
                model.ReportedParameters.confirmation_text,
                model.ReportedParameters.inspector_comment,
                model.ReportedParameters.signed_by_inspector,
                model.Users.full_name,
                # (model.ReportedParameters.done >= model.ParametersTemplates.requirement).label("parameter_requirement_fulfilled"),
            )
            .join(model.ReportedParameters.parameter)
            .join(model.Reports, model.Reports.id == model.ReportedParameters.report_id)
            .join(model.Contracts, model.Reports.contract_id == model.Contracts.id)
            .join(model.Users, model.Users.id == model.Contracts.user_id)
            # .join(model.ParametersTemplates, sqlalchemy.sql.operators.and_(model.ParametersTemplates.template_id == model.Contracts.template_id, model.ParametersTemplates.parameter_id == model.Parameters.id))
        )

        if params_report_id:
            stmt = stmt.where(model.ReportedParameters.report_id == params_report_id)

        params_inspector_id = flask.request.args.get("inspector_id")
        if role == db_utils.Role.INSPECTOR.value:

            stmt = stmt.where(model.Reports.signed_by_head_of_cathedra == True)

            if params_inspector_id:
                stmt = stmt.where(
                    model.Parameters.inspector_id == params_inspector_id
                ).where(model.ReportedParameters.signed_by_inspector == False)
            else:
                return flask.Response(
                    "No inspector id",
                    status=400,
                )

        rows = session.execute(stmt).all()

        # done for all parameters
        contracts_cte = (
            session.query(
                model.Reports.contract_id,
            )
            .select_from(model.Reports)
            .where(model.Reports.id == params_report_id)
            .cte("contracts_cte")
        )

        stmt = (
            sqlalchemy.select(
                model.ReportedParameters.parameter_id,
                sqlalchemy.sql.func.sum(model.ReportedParameters.done)
                >= sqlalchemy.sql.func.max(model.ParametersTemplates.requirement),
            )
            .select_from(model.Reports)
            .join(
                model.ReportedParameters,
                model.ReportedParameters.report_id == model.Reports.id,
            )
            .join(
                contracts_cte, contracts_cte.c.contract_id == model.Reports.contract_id
            )
            .join(model.Contracts, contracts_cte.c.contract_id == model.Contracts.id)
            .join(
                model.ParametersTemplates,
                sqlalchemy.sql.operators.and_(
                    model.ParametersTemplates.template_id
                    == model.Contracts.template_id,
                    model.ParametersTemplates.parameter_id
                    == model.ReportedParameters.parameter_id,
                ),
            )
            .where(model.Reports.signed_by_head_of_human_resources)
            .group_by(model.ReportedParameters.parameter_id)
        )
        done_for_all_parameters = session.execute(stmt).all()
        done_for_all_parameters_dict = {
            row[0]: row[1] for row in done_for_all_parameters
        }

        # get confirmation files
        stmt = sqlalchemy.select(
            model.ReportParameterConfirmations.reported_parameter_id,
            model.ReportParameterConfirmations.id,
            model.ReportParameterConfirmations.file_name,
        ).where(
            model.ReportParameterConfirmations.reported_parameter_id.in_(
                [row[0] for row in rows]
            )
        )
        confirmations = session.execute(stmt).all()
        confirmation_dict = {
            row[0]: {"id": row[1], "file_name": row[2]} for row in confirmations
        }

        return json.dumps(
            [
                {
                    "id": row[0],
                    "full_name": row[8],
                    "report_id": row[1],
                    "parameter_id": row[2],
                    "parameter_name": row[3],
                    "done": row[4],
                    "confirmation_text": row[5],
                    "inspector_comment": row[6],
                    "signed_by_inspector": row[7],
                    "confirmation_file": confirmation_dict.get(row[0]),
                    "parameter_requirement_fulfilled": done_for_all_parameters_dict.get(
                        row[2]
                    ),
                }
                for row in rows
            ]
        )


@reports_app.route("/reports/<int:id>", methods=["DELETE"])
def delete_report(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.TEACHER], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)

    stmt = sqlalchemy.select(model.Reports.signed_by_teacher).where(
        model.Reports.id == id
    )
    is_signed = session.execute(stmt).first()
    if is_signed[0]:
        return flask.Response(
            "Report already signed",
            status=400,
        )

    session.query(model.ReportedParameters).filter(
        model.ReportedParameters.report_id == id
    ).delete()
    session.query(model.Reports).filter(model.Reports.id == id).delete()
    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reports", methods=["POST"])
def save_report():

    data = flask.request.get_json()

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.TEACHER], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("period_of_report") or not data["period_of_report"].get("period"):
        error += "Empty period_of_report. "
    if not data.get("contract") or not data["contract"].get("id"):
        error += "Empty contract_id. "
    if data.get("signed_by_teacher") is None:
        error += "Empty signed_by_teacher. "
    if data.get("signed_by_head_of_cathedra") is None:
        error += "Empty signed_by_head_of_cathedra. "
    if data.get("signed_by_head_of_human_resources") is None:
        error += "Empty signed_by_head_of_human_resources. "

    if error:
        return flask.Response(
            error,
            status=400,
        )
    # data["contract_id"] = int(data["contract_id"])
    reports = model.Reports(
        period_of_report=data["period_of_report"]["period"],
        contract_id=data["contract"]["id"],
        signed_by_teacher=data["signed_by_teacher"],
        signed_by_head_of_cathedra=data["signed_by_head_of_cathedra"],
        signed_by_head_of_human_resources=data["signed_by_head_of_human_resources"],
    )
    session = sqlalchemy.orm.Session(db_utils.engine_writer)

    stmt = (
        sqlalchemy.select(model.ParametersTemplates.parameter_id)
        .join(
            model.Contracts,
            onclause=model.Contracts.template_id
            == model.ParametersTemplates.template_id,
        )
        .where(model.Contracts.id == data["contract"]["id"])
    )
    contract_parameters = session.execute(stmt).all()

    session.add(reports)
    session.flush()
    session.refresh(reports)
    for contract_parameter in contract_parameters:
        param = model.ReportedParameters(
            report_id=reports.id,
            parameter_id=contract_parameter[0],
            done=0,
            confirmation_text="",
            inspector_comment="",
            signed_by_inspector=False,
        )
        session.add(param)
    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reports/<int:id>", methods=["PUT"])
def edit_report(id):

    data = flask.request.get_json()

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.TEACHER], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    if not data.get("period_of_report") or not data["period_of_report"].get("period"):
        error += "Empty period_of_report. "
    if not data.get("contract") or not data["contract"].get("id"):
        error += "Empty contract_id. "
    if data.get("signed_by_teacher") is None:
        error += "Empty signed_by_teacher. "
    if data.get("signed_by_head_of_cathedra") is None:
        error += "Empty signed_by_head_of_cathedra. "
    if data.get("signed_by_head_of_human_resources") is None:
        error += "Empty signed_by_head_of_human_resources. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)


    stmt = sqlalchemy.select(model.Reports.signed_by_teacher).where(
        model.Reports.id == id
    )
    is_signed = session.execute(stmt).first()
    if is_signed[0]:
        return flask.Response(
            "Report already signed",
            status=400,
        )


    session.query(model.Reports).filter(model.Reports.id == id).update(
        {
            model.Reports.period_of_report: data["period_of_report"]["period"],
            model.Reports.contract_id: data["contract"]["id"],
            model.Reports.signed_by_teacher: data["signed_by_teacher"],
            model.Reports.signed_by_head_of_cathedra: data[
                "signed_by_head_of_cathedra"
            ],
            model.Reports.signed_by_head_of_human_resources: data[
                "signed_by_head_of_human_resources"
            ],
        }
    )
    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reported-parameters/<int:id>/sign", methods=["POST"])
def sign_reported_parameter(id):

    data = flask.request.get_json()

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [
                db_utils.Role.INSPECTOR,
            ],
            role,
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    stmt = session.query(model.ReportedParameters).filter(
        model.ReportedParameters.id == id
    )

    stmt.update({model.ReportedParameters.signed_by_inspector: True})

    stmt2 = (
        sqlalchemy.select(model.ReportedParameters.report_id, model.Parameters.name)
        .join(model.ReportedParameters.parameter)
        .where(model.ReportedParameters.id == id)
    )
    reported_parameter_row = session.execute(stmt2).first()

    log = model.SignatureLogs(
        time_of_change=datetime.datetime.now(),
        user_id=token_utils.get_user_id(),
        report_id=reported_parameter_row[0],
        action=str(reported_parameter_row[1]) + " signed",
    )
    session.add(log)

    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reports/<int:id>/sign", methods=["POST"])
def sign_report(id):

    data = flask.request.get_json()

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [
                db_utils.Role.TEACHER,
                db_utils.Role.HEAD_OF_CATHEDRA,
                db_utils.Role.HEAD_OF_HUMAN_RESOURCES,
            ],
            role,
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    stmt = session.query(model.Reports).filter(model.Reports.id == id)

    if role == db_utils.Role.TEACHER.value:
        stmt.update({model.Reports.signed_by_teacher: True})
    elif role == db_utils.Role.HEAD_OF_CATHEDRA.value:
        stmt.update({model.Reports.signed_by_head_of_cathedra: True})
    elif role == db_utils.Role.HEAD_OF_HUMAN_RESOURCES.value:
        stmt.update({model.Reports.signed_by_head_of_human_resources: True})

    log = model.SignatureLogs(
        time_of_change=datetime.datetime.now(),
        user_id=token_utils.get_user_id(),
        report_id=id,
        action="Report signed",
    )
    session.add(log)

    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reports/<int:id>/sign", methods=["DELETE"])
def unsign_report(id):

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [
                db_utils.Role.INSPECTOR,
            ],
            role,
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    stmt = session.query(model.Reports).filter(model.Reports.id == id)

    stmt.update(
        {
            model.Reports.signed_by_teacher: False,
            model.Reports.signed_by_head_of_cathedra: False,
        }
    )

    log = model.SignatureLogs(
        time_of_change=datetime.datetime.now(),
        user_id=token_utils.get_user_id(),
        report_id=id,
        action="Report unsigned",
    )
    session.add(log)

    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reported-parameters", methods=["PUT"])
def edit_reported_parameters():

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role([db_utils.Role.TEACHER], role)
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    data = flask.request.get_json()
    error = ""
    for reported_parameter in data:
        if reported_parameter.get("done") is None:
            error += "Empty done. "
        if reported_parameter.get("confirmation_text") is None:
            error += "Empty confirmation_text. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    for reported_parameter in data:
        stmt = (
            sqlalchemy.select(
                model.ReportedParameters.done,
                model.ReportedParameters.confirmation_text,
                model.Reports.period_of_report,
            )
            .join(model.ReportedParameters.report)
            .where(model.ReportedParameters.id == reported_parameter["id"])
        )
        old_row = session.execute(stmt).first()

        if old_row[0] != reported_parameter["done"]:
            log = model.DataChangeLogs(
                time_of_change=datetime.datetime.now(),
                user_id=token_utils.get_user_id(),
                object_of_change="Report " + str(old_row[2]) + ', field "done" changed',
                befor_change=old_row[0],
                after_change=reported_parameter["done"],
            )
            session.add(log)

        if old_row[1] != reported_parameter["confirmation_text"]:
            log = model.DataChangeLogs(
                time_of_change=datetime.datetime.now(),
                user_id=token_utils.get_user_id(),
                object_of_change="Report "
                + str(old_row[2])
                + ', field "confirmation_text" changed',
                befor_change=old_row[1],
                after_change=reported_parameter["confirmation_text"],
            )
            session.add(log)

        session.query(model.ReportedParameters).filter(
            model.ReportedParameters.id == reported_parameter["id"]
        ).update(
            {
                model.ReportedParameters.done: reported_parameter["done"],
                model.ReportedParameters.confirmation_text: reported_parameter[
                    "confirmation_text"
                ],
            }
        )

    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reported-parameters/<int:id>/upload_file", methods=["POST"])
def upload_confirmation(id):
    if "file" not in flask.request.files:
        return flask.Response(
            "No file to save",
            status=400,
        )
    file = flask.request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        return flask.Response(
            "File name is empty",
            status=400,
        )
    if not file:
        return flask.Response(
            "Bad file",
            status=400,
        )

    filename = file.filename
    # file.save("C:\\Users\\stas\\Desktop\\Diplomna\\Codes\\trash", filename)
    binary = file.read()

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    if (
        "reported_parameter_confirmation_id" in flask.request.form
        and flask.request.form.get("reported_parameter_confirmation_id")
    ):
        reported_parameter_confirmation_id = flask.request.form.get(
            "reported_parameter_confirmation_id", type=int
        )
        session.query(model.ReportParameterConfirmations).filter(
            model.ReportParameterConfirmations.id == reported_parameter_confirmation_id
        ).update(
            {
                model.ReportParameterConfirmations.file_name: filename,
                model.ReportParameterConfirmations.confirmation: binary,
            }
        )
    else:
        confirmation = model.ReportParameterConfirmations(
            reported_parameter_id=id,
            file_name=filename,
            confirmation=binary,
        )
        session.add(confirmation)
    session.commit()

    return flask.Response(status=200)


@reports_app.route("/reported-parameter-confirmations/<int:id>/download-file")
def get_reported_parameter_confirmation_file(id):
    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(
            model.ReportParameterConfirmations.confirmation,
            model.ReportParameterConfirmations.file_name,
        ).where(model.ReportParameterConfirmations.id == id)
        row = session.execute(stmt).first()

        binary_data_encoded = base64.b64encode(row[0])

        return json.dumps(
            {
                "binary": binary_data_encoded.decode("ascii"),
                "file_name": row[1],
            }
        )


@reports_app.route("/reported-parameter/<int:id>/save-comment", methods=["POST"])
def save_comment(id):
    data = flask.request.get_json()

    try:
        role = token_utils.get_role()
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )
    try:
        token_utils.check_role(
            [
                db_utils.Role.INSPECTOR,
            ],
            role,
        )
    except RuntimeError as e:
        return flask.Response(
            str(e),
            status=400,
        )

    session = sqlalchemy.orm.Session(db_utils.engine_writer)
    stmt = (
        session.query(model.ReportedParameters)
        .filter(model.ReportedParameters.id == id)
        .update({model.ReportedParameters.inspector_comment: data["inspector_comment"]})
    )

    session.commit()

    return flask.Response(status=200)
