import csv
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, String, Integer, Numeric, Float
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
metadata = MetaData()

def create_staging():

    staging_table = Table('p1_zips_staging', metadata,
    Column('zipcode', String),
    Column('city', String),
    Column('state', String),
    Column('lat', Float),
    Column('lng', Float),
    Column('population', Integer)
    )

    staging_table.drop(engine, checkfirst=True)
    staging_table.create(engine, checkfirst=True)

def load_csv_data():

    # Open a file using Python CSV reader.
    f = open("zips.csv")
    reader = csv.reader(f)
    next(reader) #skip header

    # Iterate over the rows of the zips.csv file.
    try:
        for row in reader:

        # Execute database queries, one per row; then print out confirmation.
            db.execute("INSERT INTO p1_zips_staging (zipcode,city,state,lat,lng,population) VALUES (:zip, :cit, :sta, :lat, :lng, :pop)",
            {"zip": row[0], "cit": row[1], "sta": row[2], "lat": row[3], "lng": row[4],"pop": row[5]})
            print(f"Inserting data into [p1_zips_staging] [ {row[0]} , {row[1]} , {row[2]} , {row[3]} , {row[4]} , {row[5]} ]")
    except:
        print(f"Error with Row: {row}")

    # Commit Transaction
    db.commit()

if __name__ == "__main__":
    create_staging()
    load_csv_data()

