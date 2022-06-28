import psycopg2
import pandas.io.sql as psql
import pandas as pd
import credentials as creds
from queries import *
#from logger import logger

# Set up a connection to the postgres server.
conn_string = "host=" + creds.PGHOST + " port=" + "17899" + " dbname=" + creds.PGDATABASE + " user=" + creds.PGUSER \
    + " password=" + creds.PGPASSWORD
conn = psycopg2.connect(conn_string)
print("Connected to server!")

# Create a cursor object
cursor = conn.cursor()


def get_table(schema, table):
    """
    get sql table to dataframe
    """
    query = "Select * from kali.meas where ts >= now() - interval '1 week' order by ts".format(str(schema), str(table))
    df = pd.read_sql(query, conn)
    cursor.close()
    return df


def get_15min(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '15 min' order by  sensor_id, timezone"
    timee = pd.read_sql(query, conn)

    # print(timee)
    return(timee)


def get_30min(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val  from kali.meas where ts >= now() - interval '30 min' order by  sensor_id, timezone"
    time_30min = pd.read_sql(query, conn)
    return(time_30min)


def get_1hr(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '1 hour' order by  sensor_id,timezone "
    time_1hr = pd.read_sql(query, conn)
    return(time_1hr)


def get_3hr(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '3 hour' order by  sensor_id, timezone"
    time_3hr = pd.read_sql(query, conn)
    return(time_3hr)


def get_6hr(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '6 hour' order by  sensor_id, timezone"
    time_6hr = pd.read_sql(query, conn)
    return(time_6hr)


def get_12hr(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '12 hour' order by  sensor_id, timezone"
    time_12hr = pd.read_sql(query, conn)
    return(time_12hr)


def get_24hr(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '24 hour' order by  sensor_id, timezone"
    time_24hr = pd.read_sql(query, conn)
    return(time_24hr)


def get_2d(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '2day' order by  sensor_id, timezone"
    time_2d = pd.read_sql(query, conn)
    return(time_2d)


def get_7d(schema, table):
    query = "Select sensor_id, ts AT TIME ZONE 'CEST', variable_type, val from kali.meas where ts >= now() - interval '7day' order by  sensor_id, timezone"
    time_7d = pd.read_sql(query, conn)
    return(time_7d)


def get_battry(schema, table):
    query_bat = "Select distinct on (sensor_id) sensor_id, val, variable_type, ts from kali.meas where variable_type = 'bat' order by sensor_id, ts desc;"

    bat_life = pd.read_sql(query_bat, conn)
    # print(bat_life)
    return bat_life

    # Load the locations of trashbins

    cursor.close()
    print(df.shape)
    return df


def get_location(schema, table):
    query = "select t1.*, t2.latitude, t2.longitude, t2.tree_species,t2.tree_number from kali.v_all_last t1, kali.location t2 where t1.sensor_id = t2.sensor_id"
    location_sensor = pd.read_sql(query, conn)
    return location_sensor
