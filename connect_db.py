import os,json,re
import psycopg2 as dbapi2
import message

def get_elephantsqldb_dsn(vcap_services):
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
        cursor.execute("DROP TABLE IF EXISTS MESSAGES")
        query = """CREATE TABLE IF NOT EXISTS MESSAGES
                (
                    USERNAME TEXT PRIMARY KEY  NOT NULL,
                    CONTENT TEXT  NOT NULL,
                    SUBJECT TEXT NOT NULL
                )"""
        cursor.execute(query)
        query="""INSERT INTO MESSAGES VALUES(%s,%s,%s)"""
        cursor.execute(query,("ExampleUser","Hello Everybody","Hello Message"))
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_message_to_table(message):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO MESSAGES(USERNAME,CONTENT,SUBJECT) VALUES (%s,%s,%s) """
        cursor.execute(query,(message.username,message.content,message.subject))
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

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
        cursor.execute(query,(username,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_one_message(content,subject,username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE MESSAGES SET CONTENT=%s, SUBJECT=%s WHERE USERNAME=%s"""
        cursor.execute(query,(content,subject,username))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


## Functions for Login Table

class Person:
    def __init__(self, name, surname, email, username, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.username = username
        self.password = password

def create_login():
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS LOGIN")
        operate = """CREATE TABLE IF NOT EXISTS LOGIN(
                        name VARCHAR(16),
                        surname VARCHAR(20),
                        email VARCHAR(30),
                        user_name VARCHAR(32) PRIMARY KEY,
                        password VARCHAR(32)
                  )"""
        cursor.execute(operate)
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def add_to_login(n_person):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """INSERT INTO LOGIN(name, surname, email, user_name, password)
                     VALUES (%s,%s,%s,%s,%s)
                  """
        cursor.execute(operate,(n_person.name, n_person.surname, n_person.email,
                                n_person.username, n_person.password))
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def records_from_login():
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM LOGIN""")
        records = cursor.fetchall()
        db.commit()
        db.close()
        return records

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def update_to_login(username, u_person):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """ UPDATE LOGIN SET name = %s, surname = %s,
                    email = %s, password = %s WHERE
                    user_name = %s
                    """
        cursor.execute(operate,(u_person.name, u_person.surname, u_person.email,
                                u_person.password, username))
        db.commit()
        db.close()
    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def remove_from_login(username):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """DELETE FROM LOGIN WHERE user_name = %s"""
        cursor.execute(operate, username)

        db.commit()
        db.close()
    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)
