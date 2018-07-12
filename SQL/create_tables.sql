-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d5ksc1bu97p6l";

DROP TABLE IF EXISTS "p1_cities";
DROP SEQUENCE IF EXISTS p1_cities_id_seq;
CREATE SEQUENCE p1_cities_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."p1_cities" (
    "id" integer DEFAULT nextval('p1_cities_id_seq') NOT NULL,
    "city_name" character varying NOT NULL,
    "state_id" integer,
    "zipcode" character varying(5) NOT NULL,
    "latitude" numeric NOT NULL,
    "longitude" numeric NOT NULL,
    "population" integer,
    CONSTRAINT "p1_cities_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "fk_states" FOREIGN KEY (state_id) REFERENCES p1_states(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "p1_states";
DROP SEQUENCE IF EXISTS p1_states_id_seq;
CREATE SEQUENCE p1_states_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."p1_states" (
    "id" integer DEFAULT nextval('p1_states_id_seq') NOT NULL,
    "state_abbrev" character varying NOT NULL,
    CONSTRAINT "p1_states_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "p1_user_checkin";
DROP SEQUENCE IF EXISTS p1_user_checkin_id_seq;
CREATE SEQUENCE p1_user_checkin_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."p1_user_checkin" (
    "id" integer DEFAULT nextval('p1_user_checkin_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "city_id" integer NOT NULL,
    "check_in_date" date,
    "user_comments" character varying,
    CONSTRAINT "p1_user_checkin_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "fk_cities" FOREIGN KEY (city_id) REFERENCES p1_cities(id) NOT DEFERRABLE,
    CONSTRAINT "fk_users" FOREIGN KEY (user_id) REFERENCES p1_users(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "p1_users";
DROP SEQUENCE IF EXISTS p1_users_id_seq;
CREATE SEQUENCE p1_users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."p1_users" (
    "id" integer DEFAULT nextval('p1_users_id_seq') NOT NULL,
    "first_name" character varying NOT NULL,
    "last_name" character varying NOT NULL,
    "username" character varying NOT NULL,
    "usr_pwd" character varying NOT NULL,
    CONSTRAINT "p1_users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-12 05:41:57.661738+00
