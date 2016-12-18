import os,json,re
import psycopg2 as dbapi2
import message
import profile
import account
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
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS MCOMMENTS")
        cursor.execute("DROP TABLE IF EXISTS MESSAGES")

        query = """CREATE TABLE IF NOT EXISTS MESSAGES
                (
                    MSGID SERIAL PRIMARY KEY NOT NULL,
                    USERNAME TEXT NOT NULL,
                    CONTENT TEXT  NOT NULL,
                    SUBJECT TEXT NOT NULL,
                    FOREIGN KEY (USERNAME) REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query="""CREATE TABLE IF NOT EXISTS MCOMMENTS(
                    COMMENTID INTEGER NOT NULL,
                    USERNAME TEXT NOT NULL,
                    CONTENT TEXT  NOT NULL,
                    FOREIGN KEY (USERNAME) REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (COMMENTID) REFERENCES MESSAGES(MSGID) ON DELETE CASCADE ON UPDATE CASCADE
                )"""
        cursor.execute(query)

        db_connection.commit()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

def add_message_to_table(message):
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()
        query = """INSERT INTO MESSAGES(USERNAME,CONTENT,SUBJECT) VALUES (%s,%s,%s) """
        cursor.execute(query,(message.username,message.content,message.subject))
        db_connection.commit()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

def get_messages_from_table():
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()
        query = """SELECT MSGID,USERNAME,CONTENT,SUBJECT FROM MESSAGES"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        return fetchedData;
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

def remove_message_from_table(id):
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()
        query = """DELETE FROM MESSAGES WHERE MSGID = %s"""
        cursor.execute(query,(id,))
        db_connection.commit()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

def update_one_message(content,subject,messageId):
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()
        query = """UPDATE MESSAGES SET CONTENT=%s, SUBJECT=%s WHERE MSGID = %s"""
        cursor.execute(query,(content,subject,messageId))
        db_connection.commit()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

def add_comments_for_message(comId,username,content):
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()
        query = """INSERT INTO MCOMMENTS (COMMENTID,USERNAME,CONTENT) VALUES (%s,%s,%s) """
        cursor.execute(query,(comId,username,content))
        db_connection.commit()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

def get_message_comments():
    dsn = connect()
    db_connection = dbapi2.connect(dsn)
    try:
        cursor = db_connection.cursor()
        query = """SELECT COMMENTID,USERNAME,CONTENT FROM MCOMMENTS"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        return fetchedData
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)
        db_connection.rollback()
    finally:
        if db_connection:
            db_connection.close()

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

        cursor.execute("DROP TABLE IF EXISTS HOBBY CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS HOBBY
                (
                    HOBBY_ID SERIAL PRIMARY KEY,
                    HOBBY_NAME TEXT

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS INTEREST CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS INTEREST
                (
                    INTEREST_ID SERIAL PRIMARY KEY,
                    INTEREST_NAME TEXT

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS ACCOUNT CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS ACCOUNT
                (
                    ACCOUNT_ID SERIAL PRIMARY KEY,
                    USER_NAME VARCHAR(80),
                    USER_IMAGE TEXT DEFAULT 'http://www.lovemarks.com/wp-content/uploads/profile-avatars/default-avatar-tech-guy.png',
                    NAME VARCHAR(80),
                    SURNAME VARCHAR(80),
                    GENDER VARCHAR(10) DEFAULT 'Bay',
                    UNIVERSITY_ID INTEGER DEFAULT 1,
                    DEPARTMENT VARCHAR(80),
                    INITIAL_YEAR INTEGER,
                    END_YEAR INTEGER,
                    BIRTHYEAR INTEGER,
                    CITY_ID INTEGER DEFAULT 1,
                    EMAIL VARCHAR(80),
                    WEBSITE VARCHAR(80),
                    FOREIGN KEY (USER_NAME)  REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (UNIVERSITY_ID)  REFERENCES UNIVERSITY(UNIVERSITY_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (CITY_ID)  REFERENCES CITY(CITY_ID) ON DELETE CASCADE ON UPDATE CASCADE

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS ACCPERSONAL CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS ACCPERSONAL
                (
                    ACC_ID SERIAL PRIMARY KEY,
                    USER_NAME VARCHAR(80) UNIQUE,
                    ABOUTME TEXT,
                    CODE TEXT,
                    SUM1 VARCHAR(80),
                    SUM2 VARCHAR(80),
                    SUM3 VARCHAR(80),
                    WORD TEXT,
                    SCHOOL VARCHAR(255),
                    SCHOOL_GRADE INTEGER,
                    FOREIGN KEY (USER_NAME)  REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE
                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS HOBBYALL CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS HOBBYALL
                (
                    ID SERIAL PRIMARY KEY,
                    USER_NAME VARCHAR(80),
                    HOBBY_ID INTEGER,
                    ORD INTEGER,
                    FOREIGN KEY (USER_NAME)  REFERENCES ACCPERSONAL(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (HOBBY_ID)  REFERENCES HOBBY(HOBBY_ID) ON DELETE CASCADE ON UPDATE CASCADE


                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS INTERESTALL CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS INTERESTALL
                (
                    ID SERIAL PRIMARY KEY,
                    USER_NAME VARCHAR(80),
                    INTEREST_ID INTEGER,
                    ORD INTEGER,
                    FOREIGN KEY (USER_NAME)  REFERENCES ACCPERSONAL(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (INTEREST_ID)  REFERENCES INTEREST(INTEREST_ID) ON DELETE CASCADE ON UPDATE CASCADE

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
        query="""
        INSERT INTO CITY(CITY_NAME) VALUES
        ('İstanbul'),
        ('Ankara'),
        ('İzmir'),
        ('Bursa');
        """
        cursor.execute(query)
        query="""
        INSERT INTO HOBBY(HOBBY_NAME) VALUES
        ('Kitap okumak'),
        ('Müzik dinlemek'),
        ('Futbol oynamak'),
        ('Sinemaya gitmek'),
        ('Uyumak :)'),
        ('Yüzmek'),
        ('Tenis oynamak'),
        ('Fotoğraf çekmek');
        """
        cursor.execute(query)

        query="""
        INSERT INTO INTEREST(INTEREST_NAME) VALUES
        ('İnternet'),
        ('Bilgisayar'),
        ('Seyehat'),
        ('Veri Madenciliği'),
        ('Yemek'),
        ('Kahve'),
        ('Çay'),
        ('Programlama');
        """
        cursor.execute(query)
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_account_to_table(addaccount):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO ACCOUNT (USER_NAME,NAME,SURNAME,EMAIL) VALUES (%s,%s,%s,%s) """
        cursor.execute(query,(addaccount.user_name,addaccount.name,addaccount.surname,addaccount.email))
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def add_accountpersonal_to_table(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO ACCPERSONAL (USER_NAME) VALUES (%s) """
        cursor.execute(query,[username])
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def get_account_from_table(asd):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT A.USER_NAME, A.USER_IMAGE, A.NAME, A.SURNAME, A.GENDER,
        U.UNIVERSITY_NAME, A.DEPARTMENT, A.INITIAL_YEAR, A.END_YEAR, A.BIRTHYEAR,
        C.CITY_NAME, A.EMAIL, A.WEBSITE
        FROM ACCOUNT AS A, UNIVERSITY AS U, CITY AS C
        WHERE (A.UNIVERSITY_ID= U.UNIVERSITY_ID) AND (A.CITY_ID= C.CITY_ID) AND (USER_NAME = %s)"""
        print(asd)
        cursor.execute(query,[asd])
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def get_accountpersonal_from_table(asd):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT * FROM ACCPERSONAL WHERE (USER_NAME = %s)"""
        cursor.execute(query,[asd])
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_account_from_table (username,ad,soyad,resim,cinsiyet,universite,bolum,giris,bitis,dogum,sehir,eposta,web):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE ACCOUNT SET
        USER_IMAGE=%s, NAME=%s, SURNAME=%s, GENDER=%s, UNIVERSITY_ID=%s, DEPARTMENT=%s, INITIAL_YEAR=%s,
        END_YEAR=%s, BIRTHYEAR=%s, CITY_ID=%s , EMAIL=%s , WEBSITE=%s
        WHERE USER_NAME=%s"""
        cursor.execute(query,(resim,ad,soyad,cinsiyet,universite,bolum,giris,bitis,dogum,sehir,eposta,web,username))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_accountpersonal_from_table(username,hakkimda,kod,sum1,sum2,sum3,soz,lise,ort):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE ACCPERSONAL SET
        ABOUTME=%s , CODE=%s, SUM1=%s, SUM2=%s, SUM3=%s, WORD=%s, SCHOOL=%s, SCHOOL_GRADE=%s
        WHERE USER_NAME=%s"""
        cursor.execute(query,(hakkimda,kod,sum1,sum2,sum3,soz,lise,ort,username))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def get_university_from_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT * FROM UNIVERSITY"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def get_city_from_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT * FROM CITY"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

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

def get_profile_from_table(asd):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT BLOG_ID,USER_NAME,TITLE,CONTENT FROM PROFILE WHERE (USER_NAME = %s)"""
        cursor.execute(query,[asd])
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


def get_hobby_from_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT * FROM HOBBY"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_hobby_to_table(title):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO HOBBY (HOBBY_NAME) VALUES (%s) """
        cursor.execute(query,[title])
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def remove_hobby_from_table(hobby_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM HOBBY WHERE HOBBY_ID = %s"""
        cursor.execute(query,(hobby_id,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_hobby_from_table (title,hobby_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE HOBBY SET HOBBY_NAME=%s WHERE HOBBY_ID=%s"""
        cursor.execute(query,(title,hobby_id))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)



def get_hobbyall_from_table(asd):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT HOBBYALL.ORD, HOBBY.HOBBY_NAME FROM HOBBYALL, HOBBY
        WHERE (HOBBYALL.HOBBY_ID = HOBBY.HOBBY_ID) AND (USER_NAME = %s)"""
        cursor.execute(query,[asd])
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_hobbyall_to_table(userid,hobi,ord):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO HOBBYALL (USER_NAME, HOBBY_ID, ORD) VALUES (%s,%s,%s) """
        cursor.execute(query,(userid, hobi, ord))
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def remove_hobbyall_from_table(hobbyall_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM HOBBYALL WHERE ID = %s"""
        cursor.execute(query,(hobbyall_id,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)






def get_ilgiall_from_table(asd):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT INTERESTALL.ORD, INTEREST.INTEREST_NAME FROM INTERESTALL, INTEREST
        WHERE (INTERESTALL.INTEREST_ID = INTEREST.INTEREST_ID) AND (USER_NAME = %s)"""
        cursor.execute(query,[asd])
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_ilgiall_to_table(userid,ilgi,ord):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO INTERESTALL (USER_NAME, INTEREST_ID, ORD) VALUES (%s,%s,%s) """
        cursor.execute(query,(userid, ilgi, ord))
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def remove_ilgiall_from_table(hobbyall_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM INTERESTALL WHERE ID = %s"""
        cursor.execute(query,(hobbyall_id,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)








def get_ilgi_from_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """SELECT * FROM INTEREST"""
        cursor.execute(query)
        fetchedData = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return fetchedData;

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def add_ilgi_to_table(title):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """INSERT INTO INTEREST (INTEREST_NAME) VALUES (%s) """
        cursor.execute(query,[title])
        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


def remove_ilgi_from_table(ilgi_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """DELETE FROM INTEREST WHERE INTEREST_ID = %s"""
        cursor.execute(query,(ilgi_id,))
        db_connection.commit()
        db_connection.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def update_ilgi_from_table (title,ilgi_id):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        query = """UPDATE INTEREST SET INTEREST_NAME=%s WHERE INTEREST_ID=%s"""
        cursor.execute(query,(title,ilgi_id))
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
                        name VARCHAR(25) NOT NULL,
                        surname VARCHAR(25) NOT NULL,
                        email VARCHAR(35) NOT NULL,
                        user_name VARCHAR(32) UNIQUE,
                        password VARCHAR(32) UNIQUE NOT NULL,
                        user_id SERIAL NOT NULL PRIMARY KEY,
                        authority VARCHAR(10) NOT NULL
                  )"""
        cursor.execute(operate)
        operate = """INSERT INTO LOGIN(name, surname, email, user_name, password, authority)
                   VALUES ('administrator','admin', 'admin@beelink.com' ,'admin', 'admin123', 'admin');"""

        cursor.execute(operate)




        cursor.execute("DROP TABLE IF EXISTS USERSIGNUP CASCADE;")
        operate = """CREATE TABLE IF NOT EXISTS USERSIGNUP(
                        id SERIAL NOT NULL PRIMARY KEY,
                        password VARCHAR(32),
                        user_name VARCHAR(32),
                        FOREIGN KEY (password) REFERENCES LOGIN(password) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (user_name) REFERENCES LOGIN(user_name) ON DELETE CASCADE ON UPDATE CASCADE
                  )"""
        cursor.execute(operate)

        operate = """INSERT INTO USERSIGNUP(user_name, password) VALUES('admin', 'admin123')"""

        cursor.execute(operate)

        fill_kisiler_db(cursor)

        cursor.execute("DROP TABLE IF EXISTS ADMINNOTES CASCADE;")
        operate = """CREATE TABLE IF NOT EXISTS ADMINNOTES(
                        id SERIAL NOT NULL PRIMARY KEY,
                        note VARCHAR(200),
                        user_name VARCHAR(32),
                        FOREIGN KEY (user_name) REFERENCES LOGIN(user_name) ON DELETE CASCADE ON UPDATE CASCADE
                  )"""
        cursor.execute(operate)
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def addnote_from_admin(note, username):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """INSERT INTO ADMINNOTES(note, user_name)
                     VALUES (%s, %s)
                  """
        cursor.execute(operate,(note, username))
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def search_name(id, username):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """SELECT * FROM LOGIN WHERE (user_id = %s AND user_name = %s)
                  """
        cursor.execute(operate, (id, username))
        record = cursor.fetchone()
        db.commit()
        db.close()
        if record:
            return 1
        else:
            return 0

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def fill_kisiler_db(cursor):
    query = """INSERT INTO LOGIN(name, surname, email, user_name, password, authority)
                   VALUES ('Tuncay','Demirbaş', 'tuncayitu@gmail.com' ,'cuntay', '123456', 'user');"""

    cursor.execute(query)
    operate = """INSERT INTO USERSIGNUP(user_name, password) VALUES('cuntay', '123456')"""
    cursor.execute(operate)

def notes_from_admins(username):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """SELECT id, note FROM ADMINNOTES, LOGIN WHERE (ADMINNOTES.USER_NAME = %s AND
                    LOGIN.USER_NAME = %s)
                  """
        cursor.execute(operate,(username, username))
        notes = cursor.fetchall()
        db.commit()
        db.close()
        return notes

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def remove_adminnote(id):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """DELETE FROM ADMINNOTES WHERE id = %s"""
        cursor.execute(operate, (id,))
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)


def update_adminnote(note, id):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """UPDATE ADMINNOTES SET note = %s WHERE
                    id = %s
                  """
        cursor.execute(operate,(note, id))
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)


def search_admin(username):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """SELECT authority FROM LOGIN WHERE user_name = %s
                  """
        cursor.execute(operate, (username,))
        authority = cursor.fetchone()
        db.commit()
        db.close()
        if authority[0] == 'admin':
            return 1
        else:
            return 0
    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

def add_from_admin(n_person, authority):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """INSERT INTO LOGIN(name, surname, email, user_name, password, authority)
                     VALUES (%s,%s,%s,%s,%s,%s)
                  """
        cursor.execute(operate,(n_person.name, n_person.surname, n_person.email,
                                n_person.username, n_person.password, authority))

        operate = """INSERT INTO USERSIGNUP(user_name, password) VALUES(%s, %s)"""

        cursor.execute(operate, (n_person.username, n_person.password))
        db.commit()
        db.close()

    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)


def add_to_login(n_person):
    try:
        db = dbapi2.connect(connect())
        cursor = db.cursor()
        operate = """INSERT INTO LOGIN(name, surname, email, user_name, password, authority)
                     VALUES (%s,%s,%s,%s,%s,%s)
                  """
        cursor.execute(operate,(n_person.name, n_person.surname, n_person.email,
                                n_person.username, n_person.password, 'user'))

        operate = """INSERT INTO USERSIGNUP(user_name, password) VALUES(%s, %s)"""

        cursor.execute(operate, (n_person.username, n_person.password))

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

        operate = """SELECT * FROM USERSIGNUP WHERE
                    password = %s AND user_name = %s
                    """
        cursor.execute(operate,(password, username,))
        record = cursor.fetchone()

        if record:
            operate = """SELECT authority FROM LOGIN WHERE
                    user_name = %s AND password = %s
                    """
            cursor.execute(operate,(username, password,))
            authorization = cursor.fetchone()
            db.commit()
            db.close()
            if authorization[0] == "admin":
                return 2
            else:
                return 1
        else:
            db.commit()
            db.close()
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

#----- FRIENDS RELATIONS PART - EMRE KOSE
def init_friend_table():
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS PERSONFRIENDS CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS PERSONFRIENDS
                 (
                     USER_NAME VARCHAR(80) NOT NULL REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                     NAME VARCHAR(80) NOT NULL REFERENCES LOGIN(USER_NAME),
                     SURNAME VARCHAR(80) NOT NULL REFERENCES LOGIN(USER_NAME),
                     NICKNAME VARCHAR(80),
                     PRIMARY KEY(USER_NAME)

                 )"""
        cursor.execute(query)


        cursor.execute("DROP TABLE IF EXISTS FRIENDSRELATION CASCADE;")
        query = """CREATE TABLE IF NOT EXISTS FRIENDSRELATION
                (
                    USER_NAME VARCHAR(80) NOT NULL REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FRIENDUSERNAME VARCHAR(80)  NOT NULL REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    PRIMARY KEY(USER_NAME,FRIENDUSERNAME)

                )"""
        cursor.execute(query)

        cursor.execute("DROP TABLE IF EXISTS CANDIDATE_FRIENDS;")
        query = """CREATE TABLE IF NOT EXISTS CANDIDATE_FRIENDS
                (
                    USER_NAME VARCHAR(80) NOT NULL REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    FRIENDUSERNAME VARCHAR(80)  NOT NULL REFERENCES LOGIN(USER_NAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    PRIMARY KEY(USER_NAME,FRIENDUSERNAME)

                )"""
        cursor.execute(query)



        db_connection.commit()
        db_connection.close()

    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def sil_arkadas(username,myusername):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        q = """DELETE FROM FRIENDSRELATION
                    WHERE FRIENDUSERNAME = %s
                            AND USER_NAME = %s"""
        cursor.execute(q, (username,myusername))

        q = """DELETE FROM FRIENDSRELATION
                    WHERE FRIENDUSERNAME = %s
                            AND USER_NAME = %s"""
        cursor.execute(q, (myusername,username))
        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def guncelle_arkadas(ad, yeni_nickname):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()
        q = """UPDATE PERSONFRIENDS SET NICKNAME = %s
                     WHERE USER_NAME = %s"""
        cursor.execute(q, (yeni_nickname,ad))
        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def insert_to_person_friends(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """SELECT NAME,SURNAME FROM LOGIN
                                WHERE USER_NAME = %s"""
        cursor.execute(query,(username,))
        bilgi = cursor.fetchone()

        query = """INSERT INTO PERSONFRIENDS (USER_NAME,NAME,SURNAME,NICKNAME)  VALUES (%s,%s,%s,%s )"""
        cursor.execute(query, (username,bilgi[0],bilgi[1],"nickname"))


        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def ekle_arkadas(username,fusername):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """SELECT COUNT(*) FROM PERSONFRIENDS
                                WHERE USER_NAME = %s"""
        cursor.execute(query,(fusername,))
        kontrol = cursor.fetchone()

        if kontrol:
                query = """INSERT INTO FRIENDSRELATION (USER_NAME,FRIENDUSERNAME)  VALUES (%s,%s )"""
                cursor.execute(query, (username,fusername,))
                query = """INSERT INTO FRIENDSRELATION (USER_NAME,FRIENDUSERNAME)  VALUES (%s,%s )"""
                cursor.execute(query, (fusername,username,))



        db_connection.commit()
        db_connection.close()
        cursor.close()
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def yakin_arkadas_bul(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        toplam = toplam_arkadas(username)

        if toplam:
                    query = """(SELECT FRIENDUSERNAME FROM FRIENDSRELATION
                                    WHERE USER_NAME IN (SELECT FRIENDUSERNAME FROM FRIENDSRELATION
                                            WHERE USER_NAME = %s))
                                                EXCEPT
                                                ((SELECT FRIENDUSERNAME FROM FRIENDSRELATION
                                                    WHERE USER_NAME = %s)
                                                        UNION
                                                        (SELECT USER_NAME FROM FRIENDSRELATION
                                                        WHERE USER_NAME = %s) )


                                    """
                    cursor.execute(query,(username,username,username))
                    tumu = cursor.fetchall()

                    if tumu:
                        for olasi_arkadaslar in tumu:
                            query =""" INSERT INTO CANDIDATE_FRIENDS (USER_NAME,FRIENDUSERNAME)  VALUES (%s,%s )"""
                            cursor.execute(query,(username,olasi_arkadaslar[0]))

        db_connection.commit()
        db_connection.close()
        cursor.close()


    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def yakin_arkileri_al(username):
        try:
            dsn = connect()
            db_connection = dbapi2.connect(dsn)
            cursor = db_connection.cursor()

            yakin_arkadas_bul(username)

            query = """ SELECT FRIENDUSERNAME FROM CANDIDATE_FRIENDS
                                WHERE USER_NAME = %s"""
            cursor.execute(query,(username))
            tumu = cursor.fetchall()


            db_connection.commit()
            db_connection.close()
            cursor.close()

            return tumu
        except dbapi2.DatabaseError as error:
            print("Error %s" % error)

def gonder_username(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()




        query = """SELECT * FROM PERSONFRIENDS
                    WHERE USER_NAME IN
                            (SELECT FRIENDUSERNAME FROM FRIENDSRELATION
                                WHERE USER_NAME = %s)
                                    """
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
                                WHERE USER_NAME = %s"""
        cursor.execute(query,(username,))
        toplam = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        cursor.close()

        return toplam
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)

def get_myinfos(username):
    try:
        dsn = connect()
        db_connection = dbapi2.connect(dsn)
        cursor = db_connection.cursor()

        query = """SELECT NICKNAME FROM PERSONFRIENDS
                                WHERE USER_NAME = %s"""
        cursor.execute(query,(username,))
        bilgi = cursor.fetchall()

        db_connection.commit()
        db_connection.close()
        cursor.close()

        return bilgi
    except dbapi2.DatabaseError as error:
        print("Error %s" % error)


# END FOR FRIENDS RELATIONS



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

