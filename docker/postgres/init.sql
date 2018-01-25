\c template1;
CREATE EXTENSION pgcrypto;
CREATE DATABASE telegram_is;

CREATE USER docker with superuser password 'docker';
GRANT ALL privileges ON DATABASE telegram_is TO docker;
