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


