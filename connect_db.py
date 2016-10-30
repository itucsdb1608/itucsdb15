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

        cursor.execute("DROP TABLE IF EXISTS LOGIN")
        cursor.execute("CREATE TABLE IF NOT EXISTS LOGIN(username VARCHAR(50) PRIMARY KEY, password VARCHAR(32));")
        cursor.execute("INSERT INTO LOGIN VALUES ('ebasat', 'aaaa')")
        cursor.execute("INSERT INTO LOGIN VALUES ('artuncf', 'bbbb')")
        cursor.execute("INSERT INTO LOGIN VALUES ('cuntay', 'cccc')")
        cursor.execute("INSERT INTO LOGIN VALUES ('koseemre', 'dddd')")
        cursor.execute("INSERT INTO LOGIN VALUES ('arime', 'eeee')")


        sql = """DROP TABLE IF EXISTS PROFILE"""
        cursor.execute(sql)

        sql = """CREATE TABLE PROFILE (
        PROFILE_ID SERIAL PRIMARY KEY,
        USER_ID INTEGER NOT NULL,
        PHOTO VARCHAR(80),
        WEB_SITE VARCHAR(30) NOT NULL,
        CITY VARCHAR(25) NOT NULL,
        AGE INTEGER,
        UNIVERSITY VARCHAR(55),
        JOB VARCHAR(35))"""

        cursor.execute(sql)

        sql = """INSERT INTO PROFILE (USER_ID, PHOTO, WEB_SITE, CITY, AGE, UNIVERSITY, JOB) VALUES (1, '2016_1.jpg', 'www.tuncaydemirbas.com', 'İstanbul', 24, 'İstanbul Teknik Üniversitesi', 'Öğrenci');
        INSERT INTO PROFILE (USER_ID, PHOTO, WEB_SITE, CITY, AGE, UNIVERSITY, JOB) VALUES (2, '2016_2.jpg', 'www.emrekose.com', 'İstanbul', 22, 'İstanbul Teknik Üniversitesi', 'Öğrenci');
        INSERT INTO PROFILE (USER_ID, PHOTO, WEB_SITE, CITY, AGE, UNIVERSITY, JOB) VALUES (3, '2016_3.jpg', 'Kullanmıyorum', 'İstanbul', 21, 'İstanbul Teknik Üniversitesi', 'Öğrenci');"""

        cursor.execute(sql)

        db_connection.commit()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

    finally:
        if db_connection:
            db_connection.close()
