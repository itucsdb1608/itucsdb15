import os,json,re
import psycopg2 as dbapi2

def get_sqldb_dsn(vcap_services):
    """Returns the data source name for IBM SQL DB."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)',uri)
    user,password,host, _,port,dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={} dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


db_connection = None

def connect_and_init():
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        dsn = get_sqldb_dsn(VCAP_SERVICES)
    else:
        dsn = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    try:
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS MESSAGES")
        cursor.execute("CREATE TABLE IF NOT EXISTS MESSAGES ( message VARCHAR);")
        cursor.execute("INSERT INTO MESSAGES VALUES ('Hello World!')")

        query="DROP TABLE IF EXISTS CHAT_SYSTEM"
        cursor.execute(query)
        query="CREATE TABLE IF NOT EXISTS CHAT_SYSTEM(chat_id INTEGER PRIMARY KEY, chat_content VARCHAR(250));"
        cursor.execute(query)
        query="INSERT INTO CHAT_SYSTEM VALUES (1,'selam dostlar')"
        cursor.execute(query)
        query="INSERT INTO CHAT_SYSTEM VALUES (2,'beelinkledim')"
        cursor.execute(query)

        db_connection.commit()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

    finally:
        if db_connection:
            db_connection.close()
