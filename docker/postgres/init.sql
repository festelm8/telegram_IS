\c template1;
CREATE EXTENSION pgcrypto;
CREATE DATABASE rr_logs;

CREATE USER docker with superuser password 'docker';
GRANT ALL privileges ON DATABASE rr_logs TO docker;
