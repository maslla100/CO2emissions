
import sqlite3

def create_database(db_name):
    """ Create a SQLite database and connect to it. """
    conn = sqlite3.connect(db_name)
    print(f"Database {db_name} created and connected successfully.")
    return conn

def create_table(conn):
    """ Create a table for storing CO2 emissions data. """
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS emissions_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_name TEXT NOT NULL,
        country_code TEXT,
        indicator_name TEXT,
        indicator_code TEXT,
        year_1960 REAL,
        year_1961 REAL,
        year_1962 REAL,
        year_1963 REAL,
        year_1964 REAL,
        year_1965 REAL,
        year_1966 REAL,
        year_1967 REAL,
        year_1968 REAL,
        year_1969 REAL,
        year_1970 REAL,
        year_1971 REAL,
        year_1972 REAL,
        year_1973 REAL,
        year_1974 REAL,
        year_1975 REAL,
        year_1976 REAL,
        year_1977 REAL,
        year_1978 REAL,
        year_1979 REAL,
        year_1980 REAL,
        year_1981 REAL,
        year_1982 REAL,
        year_1983 REAL,
        year_1984 REAL,
        year_1985 REAL,
        year_1986 REAL,
        year_1987 REAL,
        year_1988 REAL,
        year_1989 REAL,
        year_1990 REAL,
        year_1991 REAL,
        year_1992 REAL,
        year_1993 REAL,
        year_1994 REAL,
        year_1995 REAL,
        year_1996 REAL,
        year_1997 REAL,
        year_1998 REAL,
        year_1999 REAL,
        year_2000 REAL,
        year_2001 REAL,
        year_2002 REAL,
        year_2003 REAL,
        year_2004 REAL,
        year_2005 REAL,
        year_2006 REAL,
        year_2007 REAL,
        year_2008 REAL,
        year_2009 REAL,
        year_2010 REAL,
        year_2011 REAL,
        year_2012 REAL,
        year_2013 REAL,
        year_2014 REAL,
        year_2015 REAL,
        year_2016 REAL,
        year_2017 REAL,
        year_2018 REAL,
        year_2019 REAL,
        year_2020 REAL
    );
    '''
    conn.execute(create_table_sql)
    print("Table 'emissions_data' created successfully.")

def close_connection(conn):
    """ Close the connection to the database. """
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    # Database name
    db_name = 'emissions_data.db'

    # Create the database and table
    conn = create_database(db_name)
    create_table(conn)

    # Close the connection
    close_connection(conn)
