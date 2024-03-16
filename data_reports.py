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


@data_reports_app.route("/data-reports/<int:id>", methods=["PUT"])
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

    if id != 1 and id != 0:
        return flask.Response(
            "No id for data report selected",
            status=400,
        )
    data = flask.request.get_json()
    error = ""
    if data.get("from") is None:
        error += "Empty from. "
    if data.get("till") is None:
        error += "Empty till. "
    if data.get("faculty_id") is None:
        error += "Empty faculty_id. "
    # if data.get("cathedra_id") is None:
    #     error += "Empty cathedra_id. "
    # if data.get("user_id") is None:
    #     error += "Empty user_id. "
    if data.get("extended") is None:
        error += "Empty extended. "

    if error:
        return flask.Response(
            error,
            status=400,
        )

    #     with contracts_tmp as (
    #             select contr.id as contract_id
    #     FROM contract_report.contracts as contr
    #     inner join contract_report.users on users.id = contr.user_id
    #     left join contract_report.cathedras on cathedras.id = users.cathedra_id
    #     where contr.valid_from <= '2024-03-30' and contr.valid_till >= '2024-03-30'
    #     and cathedras.faculty_id = 2
    #     ),
    #         done_params as(
    #         SELECT contr.contract_id, rep_par.parameter_id, sum(rep_par.done) as done
    #     FROM contracts_tmp as contr
    #     left join contract_report.reports as reports on reports.contract_id = contr.contract_id and reports.signed_by_head_of_human_resources
    #     left join contract_report.reported_parameters as rep_par on rep_par.report_id = reports.id
    #     group by contr.contract_id, rep_par.parameter_id)
    #
    #     SELECT contr.contract_id, par_temp.parameter_id, par_temp.requirement, par_temp.points_promised, coalesce(done_params.done, 0) as done,
    #     (coalesce(done_params.done, 0)::decimal/par_temp.requirement*100)::int as done_perc,
    #     (par_temp.points_promised*coalesce(done_params.done, 0)::decimal/par_temp.requirement)::int as done_points
    # FROM contracts_tmp as contr
    # left join contract_report.contracts on contracts.id = contr.contract_id
    # left join contract_report.parameters_templates as par_temp on par_temp.template_id = contracts.template_id
    # left join done_params on done_params.contract_id = contr.contract_id and done_params.parameter_id = par_temp.parameter_id
    # order by contract_id, parameter_id

    with db_utils.auto_session(db_utils.engine_reader) as session:
        if id == 0:
            contracts_tmp = (
                session.query(model.Contracts.id.label("contract_id"))
                .select_from(model.Contracts)
                .join(model.Users, model.Users.id == model.Contracts.user_id)
                .join(model.Cathedras, model.Cathedras.id == model.Users.cathedra_id)
                .filter(
                    sqlalchemy.sql.operators.and_(
                        model.Contracts.valid_from
                        <= datetime.strptime("2024-03-30", "%Y-%m-%d").date(),
                        model.Contracts.valid_till
                        >= datetime.strptime("2024-03-30", "%Y-%m-%d").date(),
                    )
                )
                .filter(model.Cathedras.faculty_id == 2)
                .cte("contracts_tmp")
            )

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

            stmt = (
                sqlalchemy.select(
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
                .select_from(contracts_tmp)
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

            # if data["extended"]:
            #     stmt = sqlalchemy.select(
            #         model.Users.full_name,
            #         model.Parameters.name,
            #         model.ReportedParameters.done,
            #         model.Contracts.required_points,
            #     )
            # else:
            #     stmt = sqlalchemy.select(model.Reports)
            #
            # stmt = (
            #     stmt.join(
            #         model.Contracts, model.Reports.contract_id == model.Contracts.id
            #     )
            #     .join(model.Users, model.Contracts.user_id == model.Users.id)
            #     .join(model.Cathedras, model.Users.cathedra_id == model.Cathedras.id)
            #     .join(
            #         model.ReportedParameters,
            #         model.ReportedParameters.report_id == model.Reports.id,
            #     )
            #     .join(
            #         model.Parameters,
            #         model.Parameters.id == model.ReportedParameters.parameter_id,
            #     )
            # )
            #
            # if data.get("user_id"):
            #     stmt = stmt.where(model.Users.id == data["user_id"])
            # elif data.get("cathedra_id"):
            #     stmt = stmt.where(model.Users.cathedra_id == int(data["cathedra_id"]))
            # elif data.get("faculty_id"):
            #     stmt = stmt.where(model.Cathedras.faculty_id == int(data["faculty_id"]))
            #
            # date_from = datetime.strptime(data["from"], "%Y-%m-%d").date()
            # date_till = datetime.strptime(data["till"], "%Y-%m-%d").date()
            # stmt = stmt.where(model.Reports.period_of_report >= date_from).where(
            #     model.Reports.period_of_report <= date_till
            # )

            df = pd.read_sql(stmt, session.bind)

            def color_negative_red(val):
                color = "red" if val < 0 else "black"
                return f"color: {color}"

            df.style.applymap(color_negative_red)
            report_html_body = df.to_html()
            return flask.Response(report_html_body, mimetype="text/xml")
        else:
            stmt = sqlalchemy.select(model.Reports)

            df = pd.read_sql(stmt, session.bind)

            def color_negative_red(val):
                color = "red" if val < 0 else "black"
                return f"color: {color}"

            df.style.applymap(color_negative_red)
            report_html_body = df.to_html()
            return flask.Response(report_html_body, mimetype="text/xml")


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
