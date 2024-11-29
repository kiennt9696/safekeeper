-- Create database
DROP DATABASE IF EXISTS access;

CREATE DATABASE access
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- init tables
BEGIN;


CREATE TABLE IF NOT EXISTS public.client
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default",
    secret character varying COLLATE pg_catalog."default" NOT NULL,
    redirect_uri character varying COLLATE pg_catalog."default",
    login_type character varying COLLATE pg_catalog."default",
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT client_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.role
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default",
    client_id character varying COLLATE pg_catalog."default",
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT role_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.role_permission
(
    role_id character varying COLLATE pg_catalog."default" NOT NULL,
    permission_id character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT role_permission_pkey PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS public.permission
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default",
    client_id character varying COLLATE pg_catalog."default",
    object_id character varying COLLATE pg_catalog."default",
    action_id character varying COLLATE pg_catalog."default",
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT permission_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.permission_action
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT permission_action_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.permission_object
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT permission_object_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.permission_scope
(
    permission_id character varying COLLATE pg_catalog."default" NOT NULL,
    scope_id character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT permission_scope_pkey PRIMARY KEY (permission_id, scope_id)
);

CREATE TABLE IF NOT EXISTS public.scope
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT scope_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.user_role
(
    user_id character varying COLLATE pg_catalog."default" NOT NULL,
    role_id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_role_pkey PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS public."user"
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    password_hash character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    phone character varying COLLATE pg_catalog."default" NOT NULL,
    firstname character varying COLLATE pg_catalog."default" NOT NULL,
    lastname character varying COLLATE pg_catalog."default" NOT NULL,
    active boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT user_pkey PRIMARY KEY (id),
    CONSTRAINT user_email_key UNIQUE (email),
    CONSTRAINT user_password_hash_key UNIQUE (password_hash),
    CONSTRAINT user_username_key UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS public.client_role
(
    client_id character varying COLLATE pg_catalog."default" NOT NULL,
    role_id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT client_role_pkey PRIMARY KEY (client_id, role_id)
);

ALTER TABLE IF EXISTS public.role
    ADD CONSTRAINT role_client_id_fkey FOREIGN KEY (client_id)
    REFERENCES public.client (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.role_permission
    ADD CONSTRAINT role_permission_permission_id_fkey FOREIGN KEY (permission_id)
    REFERENCES public.permission (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.role_permission
    ADD CONSTRAINT role_permission_role_id_fkey FOREIGN KEY (role_id)
    REFERENCES public.role (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.permission
    ADD CONSTRAINT permission_action_id_fkey FOREIGN KEY (action_id)
    REFERENCES public.permission_action (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.permission
    ADD CONSTRAINT permission_client_id_fkey FOREIGN KEY (client_id)
    REFERENCES public.client (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.permission
    ADD CONSTRAINT permission_object_id_fkey FOREIGN KEY (object_id)
    REFERENCES public.permission_object (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.permission_scope
    ADD CONSTRAINT permission_scope_permission_id_fkey FOREIGN KEY (permission_id)
    REFERENCES public.permission (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.permission_scope
    ADD CONSTRAINT permission_scope_scope_id_fkey FOREIGN KEY (scope_id)
    REFERENCES public.scope (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.user_role
    ADD CONSTRAINT user_role_role_id_fkey FOREIGN KEY (role_id)
    REFERENCES public.role (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.user_role
    ADD CONSTRAINT user_role_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.client_role
    ADD CONSTRAINT client_role_client_id_fkey FOREIGN KEY (client_id)
    REFERENCES public.client (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.client_role
    ADD CONSTRAINT client_role_role_id_fkey FOREIGN KEY (role_id)
    REFERENCES public.role (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;
