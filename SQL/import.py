import os
import csv
import psycopg2

def set_connection():
    global db_conn
    #depends on env.sh file
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pwd =  os.getenv("DB_PWD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    #build Postgres connect string and open db connection
    cs = "dbname=%s user=%s password=%s host=%s port=%s" % (db_name,db_user,db_pwd,db_host,db_port)
    try:
        db_conn = psycopg2.connect(cs)
    except:
        print("Unable to connect to the database.")

def create_staging():
    #create staging table for zips CSV data
	cur = db_conn.cursor()
	cs_stmt = """
	CREATE TABLE p1_zips_staging (
		zipcode INTEGER,
		city VARCHAR,
		state VARCHAR,
		lat NUMERIC,
		lng NUMERIC,
		population INTEGER)
		"""

	print("Creating staging Table")
	cur.execute(cs_stmt)

def destory_staging():
    cur = db_conn.cursor()
    ds_stmt = "DROP TABLE IF EXISTS p1_zips_staging"
    cur.execute(ds_stmt)

def load_csv_data(input_file,table_name):
    cur = db_conn.cursor()
    #load data from CSV
    print(f"Loading data from {input_file} into {table_name}")
    with open(input_file, 'r') as f:
    	next(f)  # Skip the header row.
    	cur.copy_from(f, table_name, sep=',')

    db_conn.commit()

def load_main():
    #load data from staging table into main tables
    cur = db_conn.cursor()
    sql_1 = "INSERT INTO p1_states (state_abbrev) (SELECT DISTINCT state FROM p1_zips_staging ORDER BY state)"
    sql_2 = """
    INSERT INTO p1_cities (city_name,state_id,zipcode,latitude,longitude,population)
    (
    SELECT DISTINCT
    sg.city as city_name,
    st.id as state_id,
    lpad(sg.zipcode::text,5,'0') as zipcode,
    sg.lat,
    sg.lng,
    sg.population
    FROM p1_zips_staging sg
    JOIN p1_states st ON st.state_abbrev = sg.state)
    """

    print("Loading Data into p1_states")
    cur.execute(sql_1)

    print("Loading Data into p1_cities")
    cur.execute(sql_2)

    db_conn.commit()

if __name__ == "__main__":
    set_connection()

    # Drop/Re-Create staging table
    destory_staging()
    create_staging()
    load_csv_data("zips.csv","p1_zips_staging")

    load_main()

    #Close DB Connection
    destory_staging()
    db_conn.close()