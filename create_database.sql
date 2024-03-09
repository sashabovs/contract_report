CREATE DATABASE contract_report
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'

CREATE ROLE contract_report_reader WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1
	PASSWORD '123';
	
CREATE ROLE contract_report_writer WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1
	PASSWORD '123';
	
GRANT CONNECT ON DATABASE contract_report TO contract_report_reader;
GRANT CONNECT ON DATABASE contract_report TO contract_report_writer;
	
CREATE SCHEMA contract_report
    AUTHORIZATION postgres;

GRANT USAGE ON SCHEMA contract_report TO contract_report_reader;
GRANT USAGE ON SCHEMA contract_report TO contract_report_writer;

CREATE TABLE contract_report.contract_templates
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.contract_templates
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.contract_templates TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.contract_templates TO contract_report_writer;

CREATE TABLE contract_report.users
(
    id text NOT NULL,
    full_name text NOT NULL,
    job_title_id integer,
    cathedra_id integer,
    role contract_report.roles NOT NULL,
    login text NOT NULL,
    password text NOT NULL,
    email text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.users
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.users TO contract_report_reader;

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE contract_report.users TO contract_report_writer;

CREATE UNIQUE INDEX idx_users_login
    ON contract_report.users USING btree
    (login ASC NULLS LAST)
    WITH (deduplicate_items=True)
;




INSERT INTO contract_report.users(
	id, full_name, job_title_id, cathedra_id, role, login, password, email)
	VALUES ('1111', 'Admin', null, null, 'administrator', 'admin', '$2b$12$fP3Rhl8pTIwgDT5.S8Zx..1uIc/JMcPpqDZLkFrlbn8V/opPrFygi', 'admin@admin.com');
	
	
	
CREATE TYPE contract_report.roles AS ENUM
    ('administrator', 'head_of_human_resources', 'inspector', 'teacher', 'head_of_cathedra');

ALTER TYPE contract_report.roles
    OWNER TO postgres;

GRANT USAGE ON TYPE contract_report.roles TO contract_report_reader;

GRANT USAGE ON TYPE contract_report.roles TO contract_report_writer;

CREATE TABLE contract_report.faculties
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.faculties
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.faculties TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.faculties TO contract_report_writer;

CREATE TABLE contract_report.parameter_units
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.parameter_units
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.parameter_units TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.parameter_units TO contract_report_writer;



CREATE TABLE contract_report.cathedras
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    name text NOT NULL,
	faculty_id integer NOT NULL,
	head_id text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.cathedras
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.cathedras TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.cathedras TO contract_report_writer;

CREATE TABLE contract_report.job_titles
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.job_titles
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.job_titles TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.job_titles TO contract_report_writer;

CREATE TABLE contract_report.data_change_logs
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    time_of_change timestamp without time zone NOT NULL,
    user_id text NOT NULL,
    object_of_change text NOT NULL,
    befor_change text NOT NULL,
    after_change text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.data_change_logs
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.data_change_logs TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.data_change_logs TO contract_report_writer;

CREATE TABLE contract_report.signature_logs
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    time_of_change timestamp without time zone NOT NULL,
    user_id text NOT NULL,
    report_id integer NOT NULL,
    "action" text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.signature_logs
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.signature_logs TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.signature_logs TO contract_report_writer;

CREATE TABLE contract_report.opened_period_for_reports
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    period date NOT NULL,
    time_of_opening timestamp without time zone NOT NULL,
    time_of_closing timestamp without time zone,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.opened_period_for_reports
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.opened_period_for_reports TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.opened_period_for_reports TO contract_report_writer;

CREATE TABLE contract_report.parameters
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    name text NOT NULL,
    unit_id integer NOT NULL,
    inspector_id text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.parameters
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.parameters TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.parameters TO contract_report_writer;

CREATE TABLE contract_report.contracts
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    signing_date date NOT NULL,
    valid_from date NOT NULL,
    valid_till date NOT NULL,
    user_id text NOT NULL,
    template_id integer NOT NULL,
    required_points integer NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.contracts
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.contracts TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.contracts TO contract_report_writer;

CREATE TABLE contract_report.parameters_templates
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    template_id integer NOT NULL,
    parameter_id integer NOT NULL,
    needs_inspection boolean NOT NULL,
    inspection_period_id integer,
    requirement integer,
	points_promised integer,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.parameters_templates
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.parameters_templates TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.parameters_templates TO contract_report_writer;

CREATE TABLE contract_report.reports
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    name text NOT NULL,
    period_of_report date NOT NULL,
    contract_id integer NOT NULL,
    signed_by_teacher boolean,
    signed_by_head_of_cathedra boolean,
	signed_by_head_of_human_resources boolean,
	points_granted integer NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.reports
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.reports TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.reports TO contract_report_writer;

CREATE TABLE contract_report.reported_parameters
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    report_id integer NOT NULL,
	parameter_id integer NOT NULL,
	done integer NOT NULL,
	confirmation_text text,
	inspector_comment text,
	signed_by_inspector boolean,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.reported_parameters
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.reported_parameters TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.reported_parameters TO contract_report_writer;

CREATE TABLE contract_report.report_parameter_confirmations
(
    id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
    report_id integer NOT NULL,
	parameter_id integer NOT NULL,
	confirmation bytea,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.report_parameter_confirmations
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.report_parameter_confirmations TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.report_parameter_confirmations TO contract_report_writer;

CREATE TABLE contract_report.inspection_periods
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS contract_report.inspection_periods
    OWNER to postgres;

GRANT SELECT ON TABLE contract_report.inspection_periods TO contract_report_reader;
GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE contract_report.inspection_periods TO contract_report_writer;
---------------

ALTER TABLE IF EXISTS contract_report.cathedras
    ADD CONSTRAINT cathedras_faculty_fk FOREIGN KEY (faculty_id)
    REFERENCES contract_report.faculties (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_cathedras_faculty_fk
    ON contract_report.cathedras(faculty_id);


ALTER TABLE IF EXISTS contract_report.cathedras
    ADD CONSTRAINT cathedras_head_fk FOREIGN KEY (head_id)
    REFERENCES contract_report.users (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_cathedras_head_fk
    ON contract_report.cathedras(head_id);

ALTER TABLE IF EXISTS contract_report.contracts
    ADD CONSTRAINT contracts_user_fk FOREIGN KEY (user_id)
    REFERENCES contract_report.users (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_contracts_user_fk
    ON contract_report.contracts(user_id);

ALTER TABLE IF EXISTS contract_report.contracts
    ADD CONSTRAINT contracts_template_fk FOREIGN KEY (template_id)
    REFERENCES contract_report.contract_templates (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_contracts_template_fk
    ON contract_report.contracts(template_id);

ALTER TABLE IF EXISTS contract_report.data_change_logs
    ADD CONSTRAINT data_change_logs_user_fk FOREIGN KEY (user_id)
    REFERENCES contract_report.users (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_data_change_logs_user_fk
    ON contract_report.data_change_logs(user_id);

ALTER TABLE IF EXISTS contract_report.signature_logs
    ADD CONSTRAINT signature_logs_user_fk FOREIGN KEY (user_id)
    REFERENCES contract_report.users (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_signature_logs_user_fk
    ON contract_report.signature_logs(user_id);

ALTER TABLE IF EXISTS contract_report.signature_logs
    ADD CONSTRAINT signature_logs_report_fk FOREIGN KEY (report_id)
    REFERENCES contract_report.reports (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_signature_logs_report_fk
    ON contract_report.signature_logs(report_id);

ALTER TABLE IF EXISTS contract_report.parameters
    ADD CONSTRAINT parameters_inspector_fk FOREIGN KEY (inspector_id)
    REFERENCES contract_report.users (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_parameters_inspector_fk
    ON contract_report.parameters(inspector_id);

ALTER TABLE IF EXISTS contract_report.parameters_templates
    ADD CONSTRAINT parameters_templates_template_fk FOREIGN KEY (template_id)
    REFERENCES contract_report.contract_templates (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_parameters_templates_template_fk
    ON contract_report.parameters_templates(template_id);


ALTER TABLE IF EXISTS contract_report.parameters_templates
    ADD CONSTRAINT parameters_templates_parameter_fk FOREIGN KEY (parameter_id)
    REFERENCES contract_report.parameters (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_parameters_templates_parameter_fk
    ON contract_report.parameters_templates(parameter_id);

ALTER TABLE IF EXISTS contract_report.reported_parameters
    ADD CONSTRAINT reported_parameters_report_fk FOREIGN KEY (report_id)
    REFERENCES contract_report.reports (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_reported_parameters_report_fk
    ON contract_report.reported_parameters(report_id);

ALTER TABLE IF EXISTS contract_report.reported_parameters
    ADD CONSTRAINT reported_parameters_parameter_fk FOREIGN KEY (parameter_id)
    REFERENCES contract_report.parameters (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_reported_parameters_parameter_fk
    ON contract_report.reported_parameters(parameter_id);

ALTER TABLE IF EXISTS contract_report.reports
    ADD CONSTRAINT reports_contract_fk FOREIGN KEY (contract_id)
    REFERENCES contract_report.contracts (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_reports_contract_fk
    ON contract_report.reports(contract_id);

ALTER TABLE IF EXISTS contract_report.users
    ADD CONSTRAINT users_job_title_fk FOREIGN KEY (job_title_id)
    REFERENCES contract_report.job_titles (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_users_job_title_fk
    ON contract_report.users(job_title_id);

ALTER TABLE IF EXISTS contract_report.users
    ADD CONSTRAINT users_cathedra_fk FOREIGN KEY (cathedra_id)
    REFERENCES contract_report.cathedras (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_users_cathedra_fk
    ON contract_report.users(cathedra_id);

ALTER TABLE IF EXISTS contract_report.parameters
    ADD CONSTRAINT parameters_unit_fk FOREIGN KEY (unit_id)
    REFERENCES contract_report.parameter_units (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_parameters_unit_fk
    ON contract_report.parameters(unit_id);

ALTER TABLE IF EXISTS contract_report.parameters_templates
    ADD CONSTRAINT parameters_templates_inspection_period_fk FOREIGN KEY (inspection_period_id)
    REFERENCES contract_report.inspection_periods (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_parameters_templates_inspection_period_fk
    ON contract_report.parameters_templates(inspection_period_id);

