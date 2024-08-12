\connect k3tog_dev_db;


CREATE TABLE IF NOT EXISTS k3tog."language"
(
    id BIGSERIAL NOT NULL,
    name VARCHAR(50) NOT NULL,
    CONSTRAINT laugnage_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."user"
(
    id BIGSERIAL NOT NULL,
    external_id VARCHAR(50) UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    location_state VARCHAR(50),
    location_country VARCHAR(50),
    birthday TIMESTAMP WITH TIME ZONE,
    knitting_since INT,
    bio TEXT,
    avatar_url VARCHAR(500),
    created_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE,
    deactivated_ts TIMESTAMP WITH TIME ZONE,
    preferred_language_id BIGSERIAL NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."project"
(
    id BIGSERIAL NOT NULL,
    title VARCHAR(100) NOT NULL,
    status VARCHAR(50),
    co_date TIMESTAMP WITH TIME ZONE,
    fo_date TIMESTAMP WITH TIME ZONE,
    size VARCHAR(50),
    note TEXT,
    created_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE,
    deleted_ts TIMESTAMP WITH TIME ZONE,
    pattern_id BIGSERIAL NOT NULL,
    user_id BIGSERIAL NOT NULL,
    CONSTRAINT project_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."user_pattern"
(
    id BIGSERIAL NOT NULL,
    name VARCHAR(500) NOT NULL,
    author VARCHAR(100),
    file_attachment VARCHAR(500),
    created_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE,
    deleted_ts TIMESTAMP WITH TIME ZONE,
    user_id BIGSERIAL NOT NULL,
    CONSTRAINT user_pattern_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."user_yarn"
(
    id BIGSERIAL NOT NULL,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(100),
    note TEXT,
    num_used FLOAT,
    created_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE,
    deleted_ts TIMESTAMP WITH TIME ZONE,
    user_id BIGSERIAL NOT NULL,
    CONSTRAINT user_yarn_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."user_needle"
(
    id BIGSERIAL NOT NULL,
    name VARCHAR(300) NOT NULL,
    size VARCHAR(100),
    note TEXT,
    created_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE,
    deleted_ts TIMESTAMP WITH TIME ZONE,
    user_id BIGSERIAL NOT NULL,
    CONSTRAINT user_needle_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."user_gauge"
(
    id BIGSERIAL NOT NULL,
    stitches FLOAT,
    rows FLOAT,
    after_wash BOOLEAN,
    note TEXT,
    created_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE,
    deleted_ts TIMESTAMP WITH TIME ZONE,
    user_id BIGSERIAL NOT NULL,
    yarn_id BIGSERIAL NOT NULL,
    needle_id BIGSERIAL NOT NULL,
    CONSTRAINT user_gauge_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."project_needle"
(
    project_id BIGSERIAL NOT NULL,
    needle_id BIGSERIAL NOT NULL,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."project_yarn"
(
    project_id BIGSERIAL NOT NULL,
    yarn_id BIGSERIAL NOT NULL, 
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS k3tog."project_gauge"
(
    project_id BIGSERIAL NOT NULL,
    gauge_id BIGSERIAL NOT NULL, 
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
TABLESPACE pg_default;


ALTER TABLE IF EXISTS k3tog."language" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."user" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."project" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."user_pattern" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."user_yarn" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."user_needle" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."user_gauge" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."project_needle" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."project_yarn" OWNER to k3tog_api_user;
ALTER TABLE IF EXISTS k3tog."project_gauge" OWNER to k3tog_api_user;
