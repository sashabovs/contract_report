#!/usr/bin/env python3

import json
from datetime import datetime

import flask
import pandas as pd
import sqlalchemy
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.sql.operators import and_

import contract_report_model as model
import db_utils
import token_utils
import base64

data_reports_app = flask.Blueprint("data_reports_app", __name__)


@data_reports_app.route("/data-reports/<id>", methods=["PUT"])
def get_reports(id):
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

    if not id in [
        db_utils.ReportTypes.SIGNING_PROGRESS.value,
        db_utils.ReportTypes.EXECUTION_PROGRESS.value,
        db_utils.ReportTypes.SIGNING_LOG.value,
        db_utils.ReportTypes.DATA_CHANGE_LOG.value,
    ]:
        return flask.Response(
            "Unknown id for data report selected",
            status=400,
        )
    data = flask.request.get_json()
    error = ""
    if data.get("from") is None:
        error += "Empty from. "
    if data.get("till") is None:
        error += "Empty till. "
    if data.get("extended") is None:
        error += "Empty extended. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    date_from = datetime.strptime(data["from"], "%Y-%m-%d").date()
    date_till = (datetime.strptime(data["till"], "%Y-%m-%d").date(),)

    with db_utils.auto_session(db_utils.engine_reader) as session:
        if id == db_utils.ReportTypes.EXECUTION_PROGRESS.value:
            contracts_tmp = (
                session.query(model.Contracts.id.label("contract_id"))
                .select_from(model.Contracts)
                .join(model.Users, model.Users.id == model.Contracts.user_id)
                .join(model.Cathedras, model.Cathedras.id == model.Users.cathedra_id)
                .filter(
                    sqlalchemy.sql.operators.and_(
                        model.Contracts.valid_from <= date_from,
                        model.Contracts.valid_till >= date_till,
                    )
                )
            )

            if data.get("user"):
                contracts_tmp = contracts_tmp.filter(
                    model.Users.id == data["user"]["id"]
                )
            elif data.get("cathedra"):
                contracts_tmp = contracts_tmp.filter(
                    model.Users.cathedra_id == int(data["cathedra"]["id"])
                )
            elif data.get("faculty"):
                contracts_tmp = contracts_tmp.filter(
                    model.Cathedras.faculty_id == int(data["faculty"]["id"])
                )

            contracts_tmp = contracts_tmp.cte("contracts_tmp")

            done_params = (
                session.query(
                    contracts_tmp.c.contract_id,
                    model.ReportedParameters.parameter_id,
                    sqlalchemy.sql.func.sum(model.ReportedParameters.done).label(
                        "done"
                    ),
                )
                .select_from(contracts_tmp)
                .join(
                    model.Reports,
                    sqlalchemy.sql.operators.and_(
                        model.Reports.contract_id == contracts_tmp.c.contract_id,
                        model.Reports.signed_by_head_of_human_resources,
                    ),
                )
                .join(
                    model.ReportedParameters,
                    model.ReportedParameters.report_id == model.Reports.id,
                )
                .group_by(
                    contracts_tmp.c.contract_id, model.ReportedParameters.parameter_id
                )
                .cte("done_params")
            )

            if data["extended"]:
                stmt = sqlalchemy.select(
                    contracts_tmp.c.contract_id,
                    model.ParametersTemplates.parameter_id,
                    model.ParametersTemplates.requirement,
                    model.ParametersTemplates.points_promised,
                    sqlalchemy.sql.func.coalesce(done_params.c.done, 0).label("done"),
                    (
                        sqlalchemy.sql.func.coalesce(done_params.c.done, 0).cast(
                            sqlalchemy.DECIMAL
                        )
                        / model.ParametersTemplates.requirement
                        * 100
                    )
                    .cast(sqlalchemy.Integer)
                    .label("done_perc"),
                    (
                        model.ParametersTemplates.points_promised
                        * sqlalchemy.sql.func.coalesce(done_params.c.done, 0).cast(
                            sqlalchemy.DECIMAL
                        )
                        / model.ParametersTemplates.requirement
                    )
                    .cast(sqlalchemy.Integer)
                    .label("done_points"),
                )
            else:
                stmt = sqlalchemy.select(
                    contracts_tmp.c.contract_id,
                    sqlalchemy.sql.func.sum(
                        model.ParametersTemplates.points_promised
                    ).label("points_promised"),
                    sqlalchemy.sql.func.sum(
                        (
                            model.ParametersTemplates.points_promised
                            * sqlalchemy.sql.func.coalesce(done_params.c.done, 0).cast(
                                sqlalchemy.DECIMAL
                            )
                            / model.ParametersTemplates.requirement
                        ).cast(sqlalchemy.Integer)
                    ).label("done_points"),
                    (
                        100
                        * sqlalchemy.sql.func.sum(
                            (
                                model.ParametersTemplates.points_promised
                                * sqlalchemy.sql.func.coalesce(
                                    done_params.c.done, 0
                                ).cast(sqlalchemy.DECIMAL)
                                / model.ParametersTemplates.requirement
                            ).cast(sqlalchemy.Integer)
                        )
                        / sqlalchemy.sql.func.sum(
                            model.ParametersTemplates.points_promised
                        )
                    )
                    .cast(sqlalchemy.Integer)
                    .label("done_perc"),
                )

            stmt = (
                stmt.select_from(contracts_tmp)
                .join(
                    model.Contracts,
                    model.Contracts.id == contracts_tmp.c.contract_id,
                    isouter=True,
                )
                .join(
                    model.ParametersTemplates,
                    model.ParametersTemplates.template_id
                    == model.Contracts.template_id,
                    isouter=True,
                )
                .join(
                    done_params,
                    sqlalchemy.sql.operators.and_(
                        done_params.c.parameter_id
                        == model.ParametersTemplates.parameter_id,
                        done_params.c.contract_id == contracts_tmp.c.contract_id,
                    ),
                    isouter=True,
                )
            )

            if not data["extended"]:
                stmt = stmt.group_by(contracts_tmp.c.contract_id)

            df = pd.read_sql(stmt, session.bind)

            def color_negative_red(val):
                color = "red" if val < 0 else "black"
                return f"color: {color}"

            df.style.applymap(color_negative_red)
            report_html_body = df.to_html()
            return flask.Response(report_html_body, mimetype="text/xml")
        elif id == db_utils.ReportTypes.SIGNING_PROGRESS.value:

            teachers_table = (
                session.query(
                    model.Contracts.user_id.label("user_id"),
                    model.Reports.id.label("report_id"),
                )
                .select_from(model.Reports)
                .join(model.Contracts, model.Reports.contract_id == model.Contracts.id)
                .filter(model.Reports.period_of_report.between(date_from, date_till))
                .filter(model.Reports.signed_by_teacher == False)
                .cte("teachers_table")
            )

            head_of_cathedra_table = (
                session.query(
                    model.Cathedras.head_id.label("user_id"),
                    model.Reports.id.label("report_id"),
                )
                .select_from(model.Reports)
                .join(model.Contracts, model.Reports.contract_id == model.Contracts.id)
                .join(model.Users, model.Users.id == model.Contracts.user_id)
                .join(model.Cathedras, model.Cathedras.id == model.Users.cathedra_id)
                .join(
                    model.OpenedPeriodForReports,
                    model.OpenedPeriodForReports.period
                    == model.Reports.period_of_report,
                )
                .filter(model.Reports.period_of_report.between(date_from, date_till))
                .filter(model.Reports.signed_by_head_of_cathedra == False)
                .filter(model.OpenedPeriodForReports.time_of_closing < datetime.today())
                .cte("head_of_cathedra_table")
            )

            inspectors_table = (
                session.query(
                    model.Parameters.inspector_id.label("user_id"),
                    model.Reports.id.label("report_id"),
                )
                .select_from(model.Reports)
                .join(
                    model.ReportedParameters,
                    model.ReportedParameters.report_id == model.Reports.id,
                )
                .join(
                    model.Parameters,
                    model.Parameters.id == model.ReportedParameters.parameter_id,
                )
                .join(
                    model.OpenedPeriodForReports,
                    model.OpenedPeriodForReports.period
                    == model.Reports.period_of_report,
                )
                .filter(model.Reports.period_of_report.between(date_from, date_till))
                .filter(model.OpenedPeriodForReports.time_of_closing < datetime.today())
                .filter(model.ReportedParameters.signed_by_inspector == False)
                .cte("inspectors_table")
            )

            stmt_teachers = create_html_table_for_report(teachers_table, data)
            stmt_head_of_cathedra_table = create_html_table_for_report(
                head_of_cathedra_table, data
            )
            stmt_inspectors_table = create_html_table_for_report(inspectors_table, data)

            df_1 = pd.read_sql(stmt_teachers, session.bind)
            df_2 = pd.read_sql(stmt_head_of_cathedra_table, session.bind)
            df_3 = pd.read_sql(stmt_inspectors_table, session.bind)

            def color_negative_red(val):
                color = "red" if val < 0 else "black"
                return f"color: {color}"

            df_1.style.applymap(color_negative_red)
            df_2.style.applymap(color_negative_red)
            df_3.style.applymap(color_negative_red)

            report_html_body = (
                "<label>Teachers:</label>"
                + df_1.to_html()
                + "<label>Head of cathedra:</label>"
                + df_2.to_html()
                + "<label>Inspectors:</label>"
                + df_3.to_html()
            )
            return flask.Response(report_html_body, mimetype="text/plain")
        elif id == db_utils.ReportTypes.SIGNING_LOG.value:

            log_table = (
                sqlalchemy.select(
                    model.SignatureLogs.time_of_change,
                    model.Users.full_name,
                    model.Reports.period_of_report,
                    model.SignatureLogs.action,
                )
                .join(model.SignatureLogs.report)
                .join(model.SignatureLogs.user)
                .where(model.SignatureLogs.time_of_change.between(date_from, date_till))
                .order_by(model.SignatureLogs.time_of_change)
            )

            df = pd.read_sql(log_table, session.bind)

            def color_negative_red(val):
                color = "red" if val < 0 else "black"
                return f"color: {color}"

            df.style.applymap(color_negative_red)

            return flask.Response(df.to_html(), mimetype="text/plain")
        elif id == db_utils.ReportTypes.DATA_CHANGE_LOG.value:

            log_table = (
                sqlalchemy.select(
                    model.DataChangeLogs.time_of_change,
                    model.Users.full_name,
                    model.DataChangeLogs.object_of_change,
                    model.DataChangeLogs.befor_change,
                    model.DataChangeLogs.after_change,
                )
                .join(model.DataChangeLogs.user)
                .where(model.DataChangeLogs.time_of_change.between(date_from, date_till))
                .order_by(model.DataChangeLogs.time_of_change)
            )

            df = pd.read_sql(log_table, session.bind)

            def color_negative_red(val):
                color = "red" if val < 0 else "black"
                return f"color: {color}"

            df.style.applymap(color_negative_red)

            return flask.Response(df.to_html(), mimetype="text/plain")


def create_html_table_for_report(table, data):
    userReport = sqlalchemy.orm.aliased(model.Users)
    stmt = (
        sqlalchemy.select(
            (model.Users.full_name + " (" + table.c.user_id + ")").label("user_id"),
            (
                model.Reports.period_of_report.cast(sqlalchemy.String)
                + " ("
                + userReport.full_name
                + ")"
            ).label("report_id"),
        )
        .select_from(table)
        .join(model.Users, model.Users.id == table.c.user_id)
        .join(model.Reports, model.Reports.id == table.c.report_id)
        .join(model.Contracts, model.Contracts.id == model.Reports.contract_id)
        .join(userReport, userReport.id == model.Contracts.user_id)
        .join(model.Cathedras, model.Cathedras.id == userReport.cathedra_id)
    )

    if data.get("user_id"):
        stmt = stmt.filter(userReport.id == data["user_id"])
    elif data.get("cathedra_id"):
        stmt = stmt.filter(userReport.cathedra_id == int(data["cathedra_id"]))
    elif data.get("faculty_id"):
        stmt = stmt.filter(model.Cathedras.faculty_id == int(data["faculty_id"]))
    return stmt


@data_reports_app.route("/faculties")
def get_faculties():
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

    with db_utils.auto_session(db_utils.engine_reader) as session:
        stmt = sqlalchemy.select(model.Faculties)

        rows = session.execute(stmt).all()
        mapping = [row._mapping["Faculties"] for row in rows]

        return json.dumps(
            [
                {
                    "id": row.id,
                    "name": row.name,
                }
                for row in mapping
            ]
        )
