Parts Implemented by Tuncay Demirbaş
================================
Genel
-----
Bu projede sorumlu olduğum kısım için sırayla:

* account (profil sayfası kişisel bilgiler için, tablo)
* accpersonal (profil sayfası kişisel bilgiler için, tablo)
* city (şehir tablosu)
* university (üniversite tablosu)
* hobby (hobi tablosu)
* hobbyall (profil sayfasına hobi ekleme için, tablo)
* interest (ilgi alanları tablosu)
* interestall (profil sayfasına ilgi alanı ekleme için, tablo)
* profile (profil sayfasına blog ekleme için, tablo)


olmak üzere 9 tane varlık geliştirdim. 
Ayrıca bu varlıklar için aşağıda tanımadığım fonksiyonları geliştirdim.
Tüm varlıklar birbiriyle ilişkişi olup, dinamik tablolar oluşturulmuştur.

.. figure:: tuncay/1.PNG
   :figclass: align-center
   
   Resim 1: Veritabanı genel görünümü, tablolar

Operasyonlar
------------

* Tablo Oluşturma
 Bu operasyonu tabloları yaratmak için oluşturdum. Bu operasyon sırasında öncelikle eğer tablo varsa drop yapılır. Daha sonra bu
 tablolar istenilen özelliklerle yaratılır.
* Ekleme
 Bu operasyonu yeni tablolarımıza yeni eleman eklemek için kullandım. 
* Silme
 Bu işlem tablolarımızdan artık bulunmasını istemediğimiz elemanları silmek için kullanılıyor.
* Güncelleme
 Bu işlem ise bazı bilgilerini değiştirmek istediğimiz elemanların verilerini değiştirmek için kullanılıyor.
* Arama
 Bu işlemde belirli bir özelliğe göre tablodan elemanları aramamız için kullanılıyor. 
 
 tablolarının içerikleri ve yeni çoklu ekleme, varolan çokluyu silme, güncelleme arama gibi veritabanı işlemleri bu kısımda açıklanmıştır.
 
 1. Account ve Accpersonal (profil sayfası kişisel bilgiler için, tablo)
 
 Kullanıcı tablosu ile ilişkili olan sayfam,
Öncelikle kullanıcının ;
sisteme üye olması ve giriş yapması gerekir.
Üye olduğu an, üye olan kullanıcı ile ilgili profil sayfamda ilgili tablolara kayıt olan kullanıcının kullanıcı adına göre Ekleme işlemi gerçekleştirilir.

.. code-block:: python

        newAccount = Addaccount(username, name, surname, email)
        add_to_login(newRecord)
        add_account_to_table(newAccount)
        add_accountpersonal_to_table(username)
        
Account Tablosunun genel görünümü şöyledir:

.. figure:: tuncay/2.PNG
   :figclass: align-center
   
   Resim 2: Account Tablosu
   
Gördüğünüz üzere Account Tablosunda birçok sütun bulunmakta.
* user_name
* university_id
* city_id
sütunları dış anahtar ile diğer tablolara bağlanmıştır.
Resim 2'de gördüğünüz tabloyu oluşturmak için şu kodları yazdım:

.. code-block:: python

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
        
Yukarıdaki kod diliminde ACCOUNT tablosu oluşturulmuştur. ACCOUNT tablosu daha önce oluşturulduysa o tablo silinir ve sıfırdan yeni tablo oluşturulur. Kodun bu partında birincil anahtar ve dış anahtarlar da belirlenmiştir. Bağlı olduğu diğer tablolardaki değişikliklerden etkilenme biçimleri de (ON DELETE CASCADE , ON UPDATE CASCADE) yine bu kısımda belirtilmiştir. Profil resmi eklemeyenler için "defaultprofil.png" öntanımlı değişken olarak tanımlanmıştır.

ACCPERSONAL Tablosunun genel görünümü şöyledir:

.. figure:: tuncay/3.PNG
   :figclass: align-center
   
   Resim 2: ACCPERSONAL Tablosu
   
Gördüğünüz üzere Account Tablosunda birçok sütun bulunmakta.
* user_name
sütunu dış anahtar ile diğer tabloya bağlanmıştır.
Resim 3'de gördüğünüz tabloyu oluşturmak için şu kodları yazdım:

.. code-block:: python

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
        
Yukarıdaki kod diliminde ACCPERSONAL tablosu oluşturulmuştur. ACCPERSONAL tablosu daha önce oluşturulduysa o tablo silinir ve sıfırdan yeni tablo oluşturulur. Kodun bu partında birincil anahtar ve dış anahtarlar da belirlenmiştir. Bağlı olduğu diğer tablolardaki değişikliklerden etkilenme biçimleri de (ON DELETE CASCADE , ON UPDATE CASCADE) yine bu kısımda belirtilmiştir.

Mevcut profil için kullanıcının profil bilgilerini güncellemesi için oluşturulan bu tabloların oluşturulması için şöyle bir yöntem izlenmiştir.
Kullanıcı sisteme üye olduğu andan itibaren hemen, Yukarıda da göstermiş olduğum 
 * add_account_to_table(newAccount)
 * add_accountpersonal_to_table(username)
ilgili kod kısmında insert fonksiyonları çalıştırılır ve ilgili kullanıcıya özel,
her iki tabloda da birer kayıt oluşturulur.

**ACCOUNT Insert Komutu:**

.. code-block:: python

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
        
Insert ile ilgili kod kısmından Görüldüğü üzere sisteme üye olan kullanıcının sırayla
* user_name
* name
* surname
* email
bilgileri alınıp ACCOUNT tablosuna insert ediliyor. Böylelikle ilgili kullanıcıya ait bölüm oluşturulmuş olundu.

**ACCPERSONAL Insert Komutu:**

.. code-block:: python

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
        
Insert ile ilgili kod kısmından Görüldüğü üzere sisteme üye olan kullanıcının sırayla
* user_name
bilgisi alınıp ACCPERSONAL UNT tablosuna insert ediliyor. Böylelikle ilgili kullanıcıya ait bölüm oluşturulmuş olundu.        
