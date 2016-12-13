import os,json,re
import psycopg2 as dbapi2
import message
import profile
import friend
import personal_message
import login

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

        query = """CREATE TABLE IF NOT EXISTS USERS
                (
                    USERID SERIAL NOT NULL,
                    USERNAME TEXT NOT NULL,
                    UNIQUE(USERNAME),
                    PRIMARY KEY(USERID)
                )"""
        cursor.execute(query)


        query = """CREATE TABLE IF NOT EXISTS MESSAGES
                (
                    MSGID SERIAL PRIMARY KEY NOT NULL,
                    USERNAME TEXT NOT NULL,
                    CONTENT TEXT  NOT NULL,
                    SUBJECT TEXT NOT NULL,
                    FOREIGN KEY (USERNAME) REFERENCES USERS(USERNAME)
                )"""
        cursor.execute(query)
        query="""INSERT INTO USERS (USERNAME) VALUES (%s)"""
        cursor.execute(query,("user1",))
        query="""INSERT INTO USERS (USERNAME) VALUES (%s)"""
        cursor.execute(query,("user2",))
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
        query = """SELECT MSGID,USERNAME,CONTENT,SUBJECT FROM MESSAGES"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def get_users_from_users_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT USERNAME FROM USERS"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def remove_message_from_table(id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM MESSAGES WHERE MSGID = %s"""
        cursor.execute(query,(id,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_one_message(content,subject,messageId):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE MESSAGES SET CONTENT=%s, SUBJECT=%s WHERE MSGID = %s"""
        cursor.execute(query,(content,subject,messageId))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


## Functions for Profile Table

def init_profile_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS PROFILE CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS PROFILE
                (
                    BLOG_ID SERIAL PRIMARY KEY,
                    USER_NAME VARCHAR(80) NOT NULL,
                    TITLE VARCHAR(80),
                    CONTENT TEXT NOT NULL,
                    FOREIGN KEY (USER_NAME)  REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS UNIVERSITY CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS UNIVERSITY
                (
                    UNIVERSITY_ID SERIAL PRIMARY KEY,
                    UNIVERSITY_NAME TEXT

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS CITY CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS CITY
                (
                    CITY_ID SERIAL PRIMARY KEY,
                    CITY_NAME TEXT

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS ACCOUNT CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS ACCOUNT
                (
                    ACCOUNT_ID SERIAL PRIMARY KEY,
                    USER_NAME VARCHAR(80),
                    USER_IMAGE TEXT,
                    NAME VARCHAR(80),
                    SURNAME VARCHAR(80),
                    GENDER VARCHAR(10),
                    UNIVERSITY_ID INTEGER,
                    DEPARTMENT VARCHAR(80),
                    INITIAL_YEAR INTEGER,
                    END_YEAR INTEGER,
                    BIRTHYEAR INTEGER,
                    CITY_ID INTEGER,
                    EMAIL VARCHAR(80),
                    WEBSITE VARCHAR(80),
                    FOREIGN KEY (USER_NAME)  REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (UNIVERSITY_ID)  REFERENCES UNIVERSITY(UNIVERSITY_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (CITY_ID)  REFERENCES CITY(CITY_ID) ON DELETE CASCADE ON UPDATE CASCADE

                )"""
        cursor.execute(query)

        query="""INSERT INTO PROFILE (USER_NAME,TITLE,CONTENT) VALUES (%s,%s,%s)"""
        cursor.execute(query,("cuntay","Hello Everybody","This is my first Blog"))
        query="""
        INSERT INTO UNIVERSITY(UNIVERSITY_NAME) VALUES
        ('İstanbul Teknik Üniversitesi'),
        ('Boğaziçi Üniversitesi'),
        ('Orta Doğu Teknik Üniversitesi'),
        ('Bilkent Üniversitesi');
        """
        cursor.execute(query)
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_profile_to_table(profile):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO PROFILE (USER_NAME,TITLE,CONTENT) VALUES (%s,%s,%s) """
        cursor.execute(query,(profile.user_name,profile.title,profile.content))
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def get_profile_from_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT BLOG_ID,USER_NAME,TITLE,CONTENT FROM PROFILE"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def remove_profile_from_table(blog_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM PROFILE WHERE BLOG_ID = %s"""
        cursor.execute(query,(blog_id,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_profile_from_table (title,content,blog_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE PROFILE SET TITLE=%s, CONTENT=%s WHERE BLOG_ID=%s"""
        cursor.execute(query,(title,content,blog_id))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


## Functions for Login Table

def create_login():
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS LOGIN CASCADE;")
        operate = """CREATE TABLE IF NOT EXISTS LOGIN(
                        name VARCHAR(16) NOT NULL,
                        surname VARCHAR(20) NOT NULL,
                        email VARCHAR(30) NOT NULL,
                        user_name VARCHAR(32) UNIQUE,
                        password VARCHAR(32) NOT NULL,
                        user_id SERIAL NOT NULL PRIMARY KEY
                  )"""
        cursor.execute(operate)
        fill_kisiler_db(cursor)

        operate = """CREATE TABLE IF NOT EXISTS USERLOGIN(
                        id SERIAL NOT NULL PRIMARY KEY,
                        user_name VARCHAR(32),
                        FOREIGN KEY (user_name) REFERENCES LOGIN(user_name)
                  )"""
        cursor.execute(operate)

        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)


def fill_kisiler_db(cursor):
    query = """INSERT INTO LOGIN(name, surname, email, user_name, password)
                   VALUES ('Tuncay','Demirbaş', 'tuncay@hotmail.com' ,'cuntay', '123456');
                INSERT INTO LOGIN(name, surname, email, user_name, password)
                   VALUES ('Enes','Basat', 'enes@hotmail.com' ,'enes', 'enes123');
                INSERT INTO LOGIN(name, surname, email, user_name, password)
                   VALUES ('Furkan','Artunç', 'furkan@hotmail.com' ,'furkan', 'furkan789');"""

    cursor.execute(query)


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

def search_user_login(username, password):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """SELECT * FROM LOGIN WHERE
                    user_name = %s AND password = %s
                    """
        cursor.execute(operate,(username, password,))
        record = cursor.fetchone()
        db.commit()
        db.close()
        if record:
            return 1
        else:
            return 0

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)


def update_to_login(user_id, u_person):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """ UPDATE LOGIN SET name = %s, surname = %s,
                    email = %s, password = %s, user_name = %s WHERE
                    user_id = %s
                    """
        cursor.execute(operate,(u_person.name, u_person.surname, u_person.email,
                                u_person.password, u_person.username ,user_id))
        db.commit()
        db.close()
    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def remove_from_login(user_id):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """DELETE FROM LOGIN WHERE user_id = %s"""
        cursor.execute(operate, (user_id,))

        db.commit()
        db.close()
    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

#----- arkadas.html sayfasi için ekleme , silme , guncelleme fonksiyonlari -    emre kose
def init_friend_table():        #n
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

     #   cursor.execute("DROP TABLE IF EXISTS PERSONFRIENDS")
        query = """CREATE TABLE IF NOT EXISTS PERSONFRIENDS
                (
                    USERNAME TEXT PRIMARY KEY ,
                    NAME TEXT NOT NULL,
                    SURNAME TEXT NOT NULL

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS FRIENDSRELATION")
        query = """CREATE TABLE IF NOT EXISTS FRIENDSRELATION
                (
                    USERNAME TEXT NOT NULL REFERENCES PERSONFRIENDS(USERNAME),
                    FRIENDUSERNAME TEXT NOT NULL,
                    PRIMARY KEY(USERNAME,FRIENDUSERNAME)

                )"""
        cursor.execute(query)

        query = """INSERT INTO PERSONFRIENDS (USERNAME,NAME,SURNAME)  VALUES (%s,%s,%s )"""
        cursor.execute(query, ("emre@","emre","kose",))

        query = """INSERT INTO PERSONFRIENDS (USERNAME,NAME,SURNAME)  VALUES (%s,%s,%s )"""
        cursor.execute(query, ("user2","veli","reis",))

        query = """INSERT INTO FRIENDSRELATION (USERNAME,FRIENDUSERNAME)  VALUES (%s,%s )"""
        cursor.execute(query, ("emre@","user2",))


        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def sil_arkadas(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        q = """DELETE FROM FRIENDSRELATION WHERE FRIENDUSERNAME = %s"""
        cursor.execute(q, (username,))
        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def guncelle_arkadas(ad, arkullaniciadi,yeniisim, yenisoyisim):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        q = """UPDATE PERSONFRIENDS SET NAME = %s, SURNAME = %s
                     WHERE USERNAME = %s"""
        cursor.execute(q, (yeniisim,yenisoyisim,arkullaniciadi))
        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)



def ekle_arkadas(username,fusername,name ,surname):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()


        query = """INSERT INTO PERSONFRIENDS (USERNAME,NAME,SURNAME)  VALUES (%s,%s,%s )"""
        cursor.execute(query, (fusername,name,surname))


        query = """INSERT INTO FRIENDSRELATION (USERNAME,FRIENDUSERNAME)  VALUES (%s,%s )"""
        cursor.execute(query, (username,fusername))


        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)




def gonder_username(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()




        query = """SELECT FRIENDUSERNAME FROM FRIENDSRELATION
                                WHERE USERNAME = %s"""
        cursor.execute(query,(username,))
        tumu = cursor.fetchall()


        db_connection.commit()
        db_connection.close()
        cursor.close()

        return tumu
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)




def toplam_arkadas(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """SELECT COUNT(*) FROM FRIENDSRELATION
                                WHERE USERNAME = %s"""
        cursor.execute(query,(username,))
        toplam = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        cursor.close()

        return toplam
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def tum_arkadaslar():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """SELECT * FROM FRIENDSRELATION
                                WHERE USERNAME = %s"""
        cursor.execute(query)
        tumu = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        cursor.close()

        return tumu
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
#----- arkadas.html sayfasi için ekleme , silme , guncelleme fonksiyonlari sonu-    emre kose
def init_personal_message_table():        #n
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

     #   cursor.execute("DROP TABLE IF EXISTS PERSONFRIENDS")
        query = """CREATE TABLE IF NOT EXISTS PERSONMSSG
                (
                    USERNAME TEXT NOT NULL,
                    NAME TEXT NOT NULL,
                    SURNAME TEXT NOT NULL,
                    PRIMARY KEY(USERNAME)

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS MESSAGERELATION")
        query = """CREATE TABLE IF NOT EXISTS MESSAGERELATION
                (
                    USERNAME TEXT NOT NULL REFERENCES PERSONMSSG(USERNAME),
                    TOUSERNAME TEXT NOT NULL,
                    MESSAGE TEXT NOT NULL,
                    PRIMARY KEY(USERNAME,TOUSERNAME,MESSAGE)

                )"""
        cursor.execute(query)

        query = """INSERT INTO PERSONMSSG (USERNAME,NAME,SURNAME)  VALUES (%s,%s,%s )"""
        cursor.execute(query, ("mert@","mert","ari",))


        query = """INSERT INTO MESSAGERELATION (USERNAME,TOUSERNAME,MESSAGE)  VALUES (%s,%s,%s )"""
        cursor.execute(query, ("mert@","emre@","sa",))


        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def send_message(username,fusername,message):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """INSERT INTO MESSAGERELATION (USERNAME,TOUSERNAME,MESSAGE)  VALUES (%s,%s ,%s)"""
        cursor.execute(query, (username,fusername,message,))


        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)



def update_personal_message(username,fusername,message):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """UPDATE MESSAGERELATION SET MESSAGE = %s
                                        WHERE USERNAME = %s AND
                                                TOUSERNAME =   %s"""
        cursor.execute(query, (message,username,fusername))


        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)




def send_username_for_messages(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()




        query = """SELECT * FROM MESSAGERELATION
                                WHERE USERNAME = %s"""
        cursor.execute(query,(username,))
        all = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        cursor.close()

        return all
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def sil_kisisel_mesaj(tousername,message):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        q = """DELETE FROM MESSAGERELATION WHERE TOUSERNAME = %s
                                            AND MESSAGE = %s"""
        cursor.execute(q, (tousername,message))
        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

