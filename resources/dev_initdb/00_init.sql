CREATE DATABASE k3tog_dev_db;

\connect k3tog_dev_db;

CREATE SCHEMA k3tog;

CREATE USER k3tog_api_user WITH PASSWORD 'password';

GRANT ALL PRIVILEGES on DATABASE k3tog_dev_db TO k3tog_api_user;
GRANT ALL PRIVILEGES on SCHEMA k3tog TO k3tog_api_user;
GRANT ALL PRIVILEGES on ALL TABLES IN SCHEMA k3tog TO k3tog_api_user;
ALTER DEFAULT PRIVILEGES in SCHEMA k3tog GRANT ALL on SEQUENCES to k3tog_api_user;
