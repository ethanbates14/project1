-- location tables
CREATE TABLE p1_cities (
	id SERIAL PRIMARY KEY,
	city_name VARCHAR  NOT NULL,
	state_id INTEGER,
	zipcode VARCHAR(5) NOT NULL,
	latitude NUMERIC  NOT NULL,
	longitude NUMERIC  NOT NULL,
	population_id INTEGER
);

CREATE TABLE p1_states (
	id SERIAL PRIMARY KEY,
	state_name VARCHAR NOT NULL,
	state_abbrev VARCHAR NOT NULL
);

CREATE TABLE p1_population (
	id SERIAL PRIMARY KEY,
	city_id INTEGER NOT NULL,
	population_total INTEGER
);
-- add constraints
ALTER TABLE p1_cities ADD CONSTRAINT fk_states FOREIGN KEY (state_id) REFERENCES p1_states (id);
ALTER TABLE p1_cities ADD CONSTRAINT fk_population FOREIGN KEY (population_id) REFERENCES p1_population (id);

-- user tables
CREATE TABLE p1_users (
	id SERIAL PRIMARY KEY,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	usr_pwd VARCHAR NOT NULL
);

CREATE TABLE p1_user_checkin (
	id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL,
	city_id INTEGER NOT NULL,
	check_in_date DATE,
	user_comments VARCHAR
);
-- add constraints
ALTER TABLE p1_user_checkin ADD CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES p1_users (id);
ALTER TABLE p1_user_checkin ADD CONSTRAINT fk_cities FOREIGN KEY (city_id) REFERENCES p1_cities (id);