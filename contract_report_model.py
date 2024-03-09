from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Identity,
    Index,
    Integer,
    LargeBinary,
    PrimaryKeyConstraint,
    Text,
)
from sqlalchemy.dialects.postgresql import DATERANGE, ENUM
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Cathedras(Base):
    __tablename__ = "cathedras"
    __table_args__ = (
        ForeignKeyConstraint(
            ["faculty_id"],
            ["contract_report.faculties.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="cathedras_faculty_fk",
        ),
        ForeignKeyConstraint(
            ["head_id"],
            ["contract_report.users.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="cathedras_head_fk",
        ),
        PrimaryKeyConstraint("id", name="cathedra_pkey"),
        Index("fki_cathedras_faculty_fk", "faculty_id"),
        Index("fki_cathedras_head_fk", "head_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)
    faculty_id = mapped_column(Integer, nullable=False)
    head_id = mapped_column(Text, nullable=False)

    faculty: Mapped["Faculties"] = relationship("Faculties", back_populates="cathedras")
    head: Mapped["Users"] = relationship(
        "Users", foreign_keys=[head_id], back_populates="cathedras"
    )
    users: Mapped[List["Users"]] = relationship(
        "Users",
        uselist=True,
        foreign_keys="[Users.cathedra_id]",
        back_populates="cathedra",
    )


class ContractTemplates(Base):
    __tablename__ = "contract_templates"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="contract_templates_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)

    contracts: Mapped[List["Contracts"]] = relationship(
        "Contracts", uselist=True, back_populates="template"
    )
    parameters_templates: Mapped[List["ParametersTemplates"]] = relationship(
        "ParametersTemplates", uselist=True, back_populates="template"
    )


class Faculties(Base):
    __tablename__ = "faculties"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="faculty_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)

    cathedras: Mapped[List["Cathedras"]] = relationship(
        "Cathedras", uselist=True, back_populates="faculty"
    )


class InspectionPeriods(Base):
    __tablename__ = "inspection_periods"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="inspection_periods_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)

    parameters_templates: Mapped[List["ParametersTemplates"]] = relationship(
        "ParametersTemplates", uselist=True, back_populates="inspection_period"
    )


class JobTitles(Base):
    __tablename__ = "job_titles"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="job_title_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)

    users: Mapped[List["Users"]] = relationship(
        "Users", uselist=True, back_populates="job_title"
    )


class OpenedPeriodForReports(Base):
    __tablename__ = "opened_period_for_reports"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="opened_period_for_reports_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    period = mapped_column(Date, nullable=False)
    time_of_opening = mapped_column(DateTime, nullable=False)
    time_of_closing = mapped_column(DateTime)


class ParameterUnits(Base):
    __tablename__ = "parameter_units"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="parameter_units_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)

    parameters: Mapped[List["Parameters"]] = relationship(
        "Parameters", uselist=True, back_populates="unit"
    )


class ReportParameterConfirmations(Base):
    __tablename__ = "report_parameter_confirmations"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="report_parameter_confirmations_pkey"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    report_id = mapped_column(Integer, nullable=False)
    parameter_id = mapped_column(Integer, nullable=False)
    confirmation = mapped_column(LargeBinary)


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        ForeignKeyConstraint(
            ["cathedra_id"],
            ["contract_report.cathedras.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="users_cathedra_fk",
        ),
        ForeignKeyConstraint(
            ["job_title_id"],
            ["contract_report.job_titles.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="users_job_title_fk",
        ),
        PrimaryKeyConstraint("id", name="users_pkey"),
        Index("fki_users_cathedra_fk", "cathedra_id"),
        Index("fki_users_job_title_fk", "job_title_id"),
        Index("idx_users_login", "login", unique=True),
        {"schema": "contract_report"},
    )

    id = mapped_column(Text)
    full_name = mapped_column(Text, nullable=False)
    role = mapped_column(
        ENUM(
            "roles",
            "administrator",
            "head_of_human_resources",
            "inspector",
            "teacher",
            "head_of_cathedra",
            name="roles",
        ),
        nullable=False,
    )
    login = mapped_column(Text, nullable=False)
    password = mapped_column(Text, nullable=False)
    email = mapped_column(Text, nullable=False)
    job_title_id = mapped_column(Integer)
    cathedra_id = mapped_column(Integer)

    cathedras: Mapped[List["Cathedras"]] = relationship(
        "Cathedras",
        uselist=True,
        foreign_keys="[Cathedras.head_id]",
        back_populates="head",
    )
    cathedra: Mapped[Optional["Cathedras"]] = relationship(
        "Cathedras", foreign_keys=[cathedra_id], back_populates="users"
    )
    job_title: Mapped[Optional["JobTitles"]] = relationship(
        "JobTitles", back_populates="users"
    )
    contracts: Mapped[List["Contracts"]] = relationship(
        "Contracts", uselist=True, back_populates="user"
    )
    data_change_logs: Mapped[List["DataChangeLogs"]] = relationship(
        "DataChangeLogs", uselist=True, back_populates="user"
    )
    parameters: Mapped[List["Parameters"]] = relationship(
        "Parameters", uselist=True, back_populates="inspector"
    )
    signature_logs: Mapped[List["SignatureLogs"]] = relationship(
        "SignatureLogs", uselist=True, back_populates="user"
    )


class Contracts(Base):
    __tablename__ = "contracts"
    __table_args__ = (
        ForeignKeyConstraint(
            ["template_id"],
            ["contract_report.contract_templates.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="contracts_template_fk",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["contract_report.users.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="contracts_user_fk",
        ),
        PrimaryKeyConstraint("id", name="contracts_pkey"),
        Index("fki_contracts_template_fk", "template_id"),
        Index("fki_contracts_user_fk", "user_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    signing_date = mapped_column(Date, nullable=False)
    valid_from = mapped_column(Date, nullable=False)
    valid_till = mapped_column(Date, nullable=False)
    user_id = mapped_column(Text, nullable=False)
    template_id = mapped_column(Integer, nullable=False)
    required_points = mapped_column(Integer, nullable=False)

    template: Mapped["ContractTemplates"] = relationship(
        "ContractTemplates", back_populates="contracts"
    )
    user: Mapped["Users"] = relationship("Users", back_populates="contracts")
    reports: Mapped[List["Reports"]] = relationship(
        "Reports", uselist=True, back_populates="contract"
    )


class DataChangeLogs(Base):
    __tablename__ = "data_change_logs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["contract_report.users.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="data_change_logs_user_fk",
        ),
        PrimaryKeyConstraint("id", name="log_of_data_change_pkey"),
        Index("fki_data_change_logs_user_fk", "user_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    time_of_change = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(Text, nullable=False)
    object_of_change = mapped_column(Text, nullable=False)
    befor_change = mapped_column(Text, nullable=False)
    after_change = mapped_column(Text, nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="data_change_logs")


class Parameters(Base):
    __tablename__ = "parameters"
    __table_args__ = (
        ForeignKeyConstraint(
            ["inspector_id"],
            ["contract_report.users.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="parameters_inspector_fk",
        ),
        ForeignKeyConstraint(
            ["unit_id"],
            ["contract_report.parameter_units.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="parameters_unit_fk",
        ),
        PrimaryKeyConstraint("id", name="parameters_pkey"),
        Index("fki_parameters_inspector_fk", "inspector_id"),
        Index("fki_parameters_unit_fk", "unit_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)
    inspector_id = mapped_column(Text, nullable=False)
    unit_id = mapped_column(Integer, nullable=False)

    inspector: Mapped["Users"] = relationship("Users", back_populates="parameters")
    unit: Mapped["ParameterUnits"] = relationship(
        "ParameterUnits", back_populates="parameters"
    )
    parameters_templates: Mapped[List["ParametersTemplates"]] = relationship(
        "ParametersTemplates", uselist=True, back_populates="parameter"
    )
    reported_parameters: Mapped[List["ReportedParameters"]] = relationship(
        "ReportedParameters", uselist=True, back_populates="parameter"
    )


class ParametersTemplates(Base):
    __tablename__ = "parameters_templates"
    __table_args__ = (
        ForeignKeyConstraint(
            ["inspection_period_id"],
            ["contract_report.inspection_periods.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="parameters_templates_inspection_period_fk",
        ),
        ForeignKeyConstraint(
            ["parameter_id"],
            ["contract_report.parameters.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="parameters_templates_parameter_fk",
        ),
        ForeignKeyConstraint(
            ["template_id"],
            ["contract_report.contract_templates.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="parameters_templates_template_fk",
        ),
        PrimaryKeyConstraint("id", name="parameters_templates_pkey"),
        Index("fki_parameters_templates_inspection_period_fk", "inspection_period_id"),
        Index("fki_parameters_templates_parameter_fk", "parameter_id"),
        Index("fki_parameters_templates_template_fk", "template_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    template_id = mapped_column(Integer, nullable=False)
    parameter_id = mapped_column(Integer, nullable=False)
    needs_inspection = mapped_column(Boolean, nullable=False)
    requirement = mapped_column(Integer)
    points_promised = mapped_column(Integer)
    inspection_period_id = mapped_column(Integer)

    inspection_period: Mapped[Optional["InspectionPeriods"]] = relationship(
        "InspectionPeriods", back_populates="parameters_templates"
    )
    parameter: Mapped["Parameters"] = relationship(
        "Parameters", back_populates="parameters_templates"
    )
    template: Mapped["ContractTemplates"] = relationship(
        "ContractTemplates", back_populates="parameters_templates"
    )


class Reports(Base):
    __tablename__ = "reports"
    __table_args__ = (
        ForeignKeyConstraint(
            ["contract_id"],
            ["contract_report.contracts.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="reports_contract_fk",
        ),
        PrimaryKeyConstraint("id", name="reports_pkey"),
        Index("fki_reports_contract_fk", "contract_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = mapped_column(Text, nullable=False)
    period_of_report = mapped_column(Date, nullable=False)
    contract_id = mapped_column(Integer, nullable=False)
    points_granted = mapped_column(Integer, nullable=False)
    signed_by_teacher = mapped_column(Boolean, nullable=False)
    signed_by_head_of_cathedra = mapped_column(Boolean, nullable=False)
    signed_by_head_of_human_resources = mapped_column(Boolean, nullable=False)

    contract: Mapped["Contracts"] = relationship("Contracts", back_populates="reports")
    reported_parameters: Mapped[List["ReportedParameters"]] = relationship(
        "ReportedParameters", uselist=True, back_populates="report"
    )
    signature_logs: Mapped[List["SignatureLogs"]] = relationship(
        "SignatureLogs", uselist=True, back_populates="report"
    )


class ReportedParameters(Base):
    __tablename__ = "reported_parameters"
    __table_args__ = (
        ForeignKeyConstraint(
            ["parameter_id"],
            ["contract_report.parameters.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="reported_parameters_parameter_fk",
        ),
        ForeignKeyConstraint(
            ["report_id"],
            ["contract_report.reports.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="reported_parameters_report_fk",
        ),
        PrimaryKeyConstraint("id", name="reported_parameters_pkey"),
        Index("fki_reported_parameters_parameter_fk", "parameter_id"),
        Index("fki_reported_parameters_report_fk", "report_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    report_id = mapped_column(Integer, nullable=False)
    parameter_id = mapped_column(Integer, nullable=False)
    done = mapped_column(Integer, nullable=False)
    signed_by_inspector = mapped_column(Boolean, nullable=False)
    confirmation_text = mapped_column(Text)
    inspector_comment = mapped_column(Text)

    parameter: Mapped["Parameters"] = relationship(
        "Parameters", back_populates="reported_parameters"
    )
    report: Mapped["Reports"] = relationship(
        "Reports", back_populates="reported_parameters"
    )


class SignatureLogs(Base):
    __tablename__ = "signature_logs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["contract_report.reports.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="signature_logs_report_fk",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["contract_report.users.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="signature_logs_user_fk",
        ),
        PrimaryKeyConstraint("id", name="log_of_signatures_pkey"),
        Index("fki_signature_logs_report_fk", "report_id"),
        Index("fki_signature_logs_user_fk", "user_id"),
        {"schema": "contract_report"},
    )

    id = mapped_column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    time_of_change = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(Text, nullable=False)
    report_id = mapped_column(Integer, nullable=False)
    action = mapped_column(Text, nullable=False)

    report: Mapped["Reports"] = relationship("Reports", back_populates="signature_logs")
    user: Mapped["Users"] = relationship("Users", back_populates="signature_logs")
