import os,json,re
import psycopg2 as dbapi2
import message

def get_sqldb_dsn(vcap_services):
    """Returns the data source name for IBM SQL DB."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)',uri)
    user,password,host, _,port,dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={} dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

def connect():
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        dsn = get_elephantsqldb_dsn(VCAP_SERVICES)
    else:
        dsn = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    return dsn

def init_message_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS MESSAGES
                (
                    USERNAME TEXT  NOT NULL,
                    CONTENT TEXT PRIMARY KEY NOT NULL,
                    SUBJECT TEXT NOT NULL
                )"""
        cursor.execute(query)
        db_connection.commit()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

    finally:
        if db_connection:
            db_connection.close()

def add_message_to_table(message):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO MESSAGES(USERNAME,CONTENT,SUBJECT) VALUES (%s,%s,%s) """
        cursor.execute(query,(message.username,message.content,message.subject))
        db_connection.commit()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

    finally:
        if db_connection:
            db_connection.close()

def get_messages_from_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT USERNAME,CONTENT,SUBJECT FROM MESSAGES"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def remove_message_from_table(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM MESSAGES WHERE USERNAME = %s"""
        cursor.execute(query,(username))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
