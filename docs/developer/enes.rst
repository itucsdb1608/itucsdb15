Hayati Enes Basat Tarafından Tamamlanan Kısımlar
================================================

Kaydol
--------------

Kaydol sayfasının gerçeklenmesi için "LOGIN" adında olan bir tablo eklendi. Bu tabloda "user_id" niteliği birincil anahtardır ve serial olarak tanımlıdır.  "name" niteliği kullanıcının ismini, "surname" niteliği kullanıcının soyadını, "email" niteliği kullanıcının e-posta adresini, "user_name" niteliği kullanıcı adını, "password" niteliği kullanıcının parolasını, "authority" varlığı ise kullanıcının yetkisi atamaktadır.
Varsayılan olarak veri tabanında yönetici yetkisine sahip bir kayıt bulunmaktadır.

.. code-block:: python
  
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
    except dbapi2.DatabaseError as err:
        print("Error is %s." % err)

Kullanıcı Yapısı için Oluşturulan Sınıf
---------------------------------------

Login.py dosyası altında tutulan bu sınıf, kullanıcı tarafından girilen bu beş değerin olması açısından önemli ve veri tabanı işlemleri için yardımcı olmaktadır. Amaç bir kullanıcı kaydının rahat bir şekilde aktarılabilmesidir.

.. code-block:: python

   class Person:
    def __init__(self, name, surname, email, username, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.username = username
        self.password = password


Kullanıcı Ekleme Sayfası ve İşlemleri
--------------------------------------

Kullanıcı Ekleme Sayfası
-------------------------

Ana sayfadan kaydol butonuna basıldığında get methodu ve boş metin kutularından oluşan bu sayfaya yönlendirilir. Bu sayfadan kullanıcı, bu metin kutularına bilgilerini girerek kaydol butonuna bastığında post methoduna geçer. Bilgiler <form> aracılığı ile tutulur.

.. code-block:: html
  
   <header>
						<h2>Yeni misin? Kaydol</h2>
						<p>BeeLink Dünyasına Hoş Geldiniz..</p>
					</header>
					<div class="box">
						<form method="post" action="#">
							<div class="row uniform 50%">
								<div class="6u 12u(mobilep)">
									<input type="text" name="name" id="name" value="" placeholder="Adınız" required autofocus>
								</div>
								<div class="6u 12u(mobilep)">
									<input type="text" name="surname" id="email" value="" placeholder="Soyadınız" required autofocus>
								</div>
							</div>
							<div class="row uniform 50%">
								<div class="12u">
									<input type="email" name="email" id="subject" value="" placeholder="E-posta Adresiniz" required autofocus>
								</div>
							</div>
							<div class="row uniform 50%">
								<div class="12u">
									<input type="text" name="username" id="subject" value="" placeholder="Kullanıcı Adınız" required autofocus>
								</div>
							</div>
							<div class="row uniform 50%">
								<div class="12u">
									<input type="password" name="password" id="name" value="" placeholder="Parola" required autofocus>
								</div>
							</div>
							<div class="row uniform">
								<div class="12u">
									<ul class="actions align-center">
										<li><input type="submit" name="signup" value="Kaydol"></li>
									</ul>
								</div>
							</div>
						</form>
					</div>

Kullanıcı Ekleme Fonksiyonu
---------------------------
Fonksiyon aktif hale getirildiği zaman get methodu ile çalışır. Sonra giris.htmlden aldığı verileri post methodundaki formun bilgileri request.form aracılığı ile aktarılır ve Person sınıfı yardımı ile yeni kayıt oluşturulur. Oluşturulan kayıt add_to_login fonksiyonuna yönlendirilir.Kullanıcı eklendikten sonra BeeLink anasayfasına geri döner.

.. code-block:: python

   @site.route('/signup', methods=['GET','POST'])
   def sign_up():
    if request.method == 'GET':
        return render_template('giris.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        newRecord = Person(name, surname, email, username, password)
        newAccount = Addaccount(username, name, surname, email)
        add_to_login(newRecord)
        add_account_to_table(newAccount)
        add_accountpersonal_to_table(username)
        insert_to_person_friends(username)
     return render_template('home.html')
    
Eklenen Kaydın Veritabanına Aktarılması
---------------------------------------

Kullanıcının girdiği değerler, n_person sınıfında tutulduktan sonra, n_persondaki değerler "INSERT INTO" işlevi ile gerçeklenir. Ve kullanıcı veri tabanına eklenmiş olur.

.. code-block:: python

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

Yönetici Panelinden Kullanıcı Ekleme
------------------------------------
Yönetici panelindeki kullanıcı ekle butonuna basıldığında, boş metin kutularından oluşan bu sayfaya yönlendirilir. Bu sayfadan yönetici, bu metin kutularına eklenecek kullanıcının bilgilerini girerek kaydol butonuna bastığında post methoduna geçer. Bilgiler <form> aracılığı ile tutulur. Burada select ve option şablonları ile yöneticinin kullanıcı veya yönetici yetkisini seçerek eklenecek kullanıcının yetkisini belirlemiş olur.

.. code-block:: html

   <form method="post" action="#">
						<div class="row uniform 50%">
							<div class="12u">
							<select class="form-control" name="type">
									<option value="user">Authority: Normal User</option>
									<option value="admin">Authority: Administrator</option>
							</select>
								</div>
						</div>
							<div class="row uniform 50%">
								<div class="6u 12u(mobilep)">
									<input type="text" name="name" id="name" value="" placeholder="Adınız" required autofocus>
								</div>
								<div class="6u 12u(mobilep)">
									<input type="text" name="surname" id="email" value="" placeholder="Soyadınız" required autofocus>
								</div>
							</div>
							<div class="row uniform 50%">
								<div class="12u">
									<input type="email" name="email" id="subject" value="" placeholder="E-posta Adresiniz" required autofocus>
								</div>
							</div>
							<div class="row uniform 50%">
								<div class="12u">
									<input type="text" name="username" id="subject" value="" placeholder="Kullanıcı Adınız" required autofocus>
								</div>
							</div>
							<div class="row uniform 50%">
								<div class="12u">
									<input type="password" name="password" id="name" value="" placeholder="Parola" required autofocus>
								</div>
							</div>
							<div class="row uniform">
								<div class="12u">
									<ul class="actions align-center">
										<li><input type="submit" name="signup" value="Kaydet"></li>
									</ul>
								</div>
							</div>
						</form>
            
Yönetici Panelinden Kullanıcı Ekleme Fonksiyonu
-----------------------------------------------           
Post methodundaki formun bilgileri request.form aracılığı ile aktarılır ve Person sınıfı yardımı ve yetki türü ile yeni kayıt oluşturulur. Oluşturulan kayıt add_from_admin fonksiyonuna yönlendirilir. Ardından yönetici paneli anasayfasına geri döner.

.. code-block:: python
            
   @site.route('/administrator/add', methods=['GET','POST'])
   def administrator_add_user():
      if request.method == 'GET':
         return render_template('add.html')
      else:
          name = request.form['name']
          surname = request.form['surname']
          email = request.form['email']
          username = request.form['username']
          password = request.form['password']
          newRecord = Person(name, surname, email, username, password)
          authority = request.form['type']
          add_from_admin(newRecord, authority)

      return redirect(url_for('site.administrator'))

Yönetici Tarafından Eklenen Kaydın Veritabanına Aktarılması
-----------------------------------------------------------  
Kullanıcının girdiği değerler, n_person sınıfında tutulduktan sonra, n_person sınıfındaki değerler ve authority değeri "INSERT INTO" işlevi ile gerçeklenir. Ve yönetici tarafından eklenen kullanıcı veri tabanına eklenmiş olur.

.. code-block:: python
 
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

Yönetici Panelinden Kullanıcı Görüntüleme, Güncelleme ve Silme İşlemleri
------------------------------------------------------------------------

Kullanıcı Görüntüleme Sayfası
-----------------------------
Yönetici panelinden tüm kullanıcılar görüntülenebilir. Silme fonksiyonu post methodu ile aktif hale gelir, gönderilecek değer "user_id" değerine eşittir. Güncelleme fonksiyonu get methodu ile aktif hale gelir, gönderilecek değer "user_id" değerine eşittir.

.. code-block:: html

   <table border="1">
    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Surname</th>
    <th>E-mail</th>
    <th>User name</th>
    <th>Password</th>
    <th>Delete</th>
    <th>Update</th>
    <th>Authority</th>
    </tr>
    {% for i in records %}
      {% if i %}
    <tr>
    <td>{{i[5]}}</td>
    <td>{{i[0]}}</td>
    <td>{{i[1]}}</td>
    <td>{{i[2]}}</td>
    <td>{{i[3]}}</td>
    <td>{{i[4]}}</td>
    <td>
    <form action="{{url_for('site.remove_user')}}" method="post" name="delete"><button type="submit" value="{{ i[5] }}" name="delete">Delete</button>
    </form>
    </td>
    <td>
    <form role="form" action="{{url_for('site.update_user', id = i[5])}}" method="get" name="update"><button type="submit" value="{{ i[5] }}" name="update">Update</button>
    </form>
    </td>
    <td>{{i[6]}}</td>
    </tr>
      {% endif %}
    {% endfor %}
    </table>

Kullanıcı Görüntüleme Fonksiyonu
--------------------------------
Tüm kullanıcıları "SELECT" fonksiyonu ile veritabanından çekilir ve bu kayıtlar records adı altında fonksiyonun çağrıldığı yere geri gönderilir.

.. code-block:: python

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
          
Kullanıcı Güncelleme Sayfası
----------------------------
Yönetici, bu sayfadaki boş metinlere güncellemek istediği kaydın bilgilerini girerek post methodu ile gönderir.

.. code-block:: html

   <div class="box">
	<form role="form" method="post" action="" name="update_user">
	<div class="12u">
	<input type="text" name="username" id="subject" value="" placeholder="New Username" required autofocus>
	</div>
	<div class="12u">
	<input type="text" name="name" id="subject" value="" placeholder="New Name" required autofocus>
	</div>
	<div class="12u">
	<input type="text" name="surname" id="subject" value="" placeholder="New Surname" required autofocus>
	</div>
	<div class="12u">
	<input type="text" name="email" id="subject" value="" placeholder="New E-mail" required autofocus>
	</div>
	<div class="12u">
	<input type="text" name="password" id="subject" value="" placeholder="New Password" required autofocus>
	</div>
	<ul class="actions align-center">
	<li><button type="submit">Update</li>
	</ul>
	</form>
	</div>
  
Kullanıcı Güncelleme Fonksiyonu
-------------------------------
Güncelleme işlemi get methodu ile başlar, update.html sayfasından alınan bilgiler ile post methodunda alınan bilgiler request.form da tutulur ve yeni kullanıcı sınıfı oluşturulur. Person sınıfı kayıtları ile id değeri veritabanına güncelleme fonksiyonuna giderek güncelleme işlemi yapılır. Ardından, records_from_login fonksiyonu ile tüm güncel kayıtları alarak yönetici anasayfasına yönlendirilir.

.. code-block:: python

   @site.route('/user/update/<int:id>', methods=['GET', 'POST'])
   def update_user(id):
      if request.method == 'GET':
          return render_template('update.html')
      else:
          username = request.form['username']
          name = request.form['name']
          surname = request.form['surname']
          email = request.form['email']
          password = request.form['password']
          updateRecord = Person(name, surname, email, username, password)
          update_to_login(id, updateRecord)
          records = records_from_login()
          return render_template('administrator.html', records = records)
          
Veritabanında Kullanıcı Güncelleme Fonksiyonu
---------------------------------------------
Kullanıcı bilgileri u_person sınıfı içerisinde saklanır ve user_id değeri ile fonksiyon çağrılır. Fonksiyon user_id nin eşit olduğu kaydı bulur ve "UPDATE" fonksiyonu gerçekleşerek kayıt güncellenir.

.. code-block:: python

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
        
Kullanıcı Silme Fonksiyonu
--------------------------
İlk önce yönetici ana sayfasına yönlendirilir. Ardından butona tıklanarak post methodu ile tıklandığı kaydın user_id si request.formdan alınır. Eğer yönetici kendi kaydını silmek istiyorsa bu kontrol edilir ve eğer kendini silecekse silme işlemi user_id değerini alarak silme fonksiyonuna yönlendirir ve kayıt veritabanından silinir ardından oturum kapanır ve BeeLink anasayfasına yönlendirilir. Yönetici eğer kendini silmek istemiyorsa silme işlemi user_id değerini alarak silme fonksiyonuna yönlendirir, kayıt veritabanından silinir ve ardından yönetici anasayfasına yönlendirilir.

.. code-block:: python

   @site.route('/user/remove', methods=['GET', 'POST'])
   def remove_user():
      if request.method == 'GET':
          return render_template('administrator.html')
      else:
          uname = session['name']
          user_id = request.form['delete']
          check = search_name(user_id, uname)

          if check == 1:
              remove_from_login(user_id)
              return render_template('home.html')
          else:
              remove_from_login(user_id)
              records = records_from_login()
              return render_template('administrator.html', records = records)
              
Veritabanından Kullanıcı Silme Fonksiyonu
-----------------------------------------
User_id değerine sahip kayıt "DELETE" fonksiyonu ile aranarak veritabanından silinir.

.. code-block:: python

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
          
Giriş ve Çıkış İşlemleri
------------------------

Giriş
-----
Giriş yap sayfasında kullanıcı veya yönetici boş metin kutuları üzerine kullanıcı adı ve parolasını girer ve post methodu ile giriş sayfası gerçeklenir.

.. code-block:: html

   <header>
              <h2>Giriş Yap, BeeLink'le..</h2>
              <p>BeeLink Dünyasına Hoş Geldiniz..</p>
            </header>
            <div class="box">
              <form method="post" action="#">
                <div class="row uniform 50%">
                  <div class="12u">
                    <input type="text" name="username" id="subject" value="" placeholder="Kullanıcı Adınız" required autofocus>
                  </div>
                </div>
                <div class="row uniform 50%">
                  <div class="12u">
                    <input type="password" name="password" id="subject" value="" placeholder="Parolanız" required autofocus>
                  </div>
                </div>
                <div class="row uniform">
                  <div class="12u">
                    <ul class="actions align-center">
                      <li><input type="submit" name="signin" value="Giriş Yap"></li>
                    </ul>
                  </div>
                </div>
              </form>
            </div>

Kullanıcı Giriş Fonksiyonu
--------------------------
Signin fonksiyonu post methodu ile gelen kullanıcı adı ve parolayı sorgular. Sorgulama doğru sonuç verirse session yani oturum açılmış olur. Sorgulama sonucunda sonuç 0 ise kullanıcı bilgileri yanlış veya eksik girilmiştir ve hata sayfasına yönlendirilir. Eğer giren yönetici ise sonuç 2 dir ve yönetici paneline yönlendirilir. Eğer giren kullanıcı ise sonuç 1 dir ve BeeLink platformuna giriş yapar ve sayfasına yönlendirilir. Oturum ismi kullanıcı adıdır ve diğer fonksiyonlarla beraber çalışmaktadır.

.. code-block:: python

   @site.route('/signin', methods=['GET','POST'])
   def sign_in():
      if request.method == 'GET':
          return render_template('girisyap.html')
      else:
          username = request.form['username']
          password = request.form['password']
          check = search_user_login(username, password)
          if check == 1:
              session['name'] = username
              return redirect(url_for('site.signed_in'))
          elif check == 2:
              session['name'] = username
              return redirect(url_for('site.administrator'))
          else:
              return render_template('error.html')

Hatalı Giriş Sayfası
--------------------
Kullanıcı veya yönetici, siteye giriş yaparken eksik veya yanlış bir değer girdiğinde yönlendirileceği sayfadır. Alert fonksiyonu ile geçersiz değer girildiğini belirtilir.

  .. code-block:: html

     {% extends "base.html" %}
     {% block title %}Oops!{% endblock %}

     {% block content %}

     <script type="text/javascript">
       alert("You have entered invalid username or password.")
     </script>
     {% endblock %}
  
Yönetici Sayfasına Giriş Fonksiyonu
-----------------------------------
Yönetici sayfasına yönlendirilerek veya tarayıcıda beelink platformunun sonuna /administrator yazılarak girilebilir fakat girilmesi için oturum açılması gerekir. Oturum açan yönetici veya kullanıcı olabilir. Bu sayfaya her gelindiğinde bu fonksiyon kullanıcının veya yöneticinin oturum açıp açmadığını session ile kontrol eder ve oturum açıldıysa yönetici olup olmadığını search_admin fonksiyonu ve kullanıcı adı parameterleri ile kontrol eder. Eğer yönetici sayfaya girmek istiyorsa tüm kayıtlar veritabanından çekilir ve yönetici ana sayfasına yönlendirilir. Fakat kullanıcı sayfaya erişmek istiyorsa BeeLink platformunun ana sayfasına yönlendirilir.

.. code-block:: python

   @site.route('/administrator')
   def administrator():
      if session['name'] == "":
          return render_template('home.html')
      else:
          uname = session['name']
          check = search_admin(uname)
          if check == 1:
              records = records_from_login()
              return render_template('administrator.html', records = records)
          else:
              return render_template('home.html')

Kullanıcı Platformuna Giriş Fonksiyonu
--------------------------------------
Kullanıcı giriş yaptıktan sonra yönlendirileceği sayfadır, session ile oturum açılır, projenin diğer kısımları çalışmaya başlar.

.. code-block:: python
 
   @site.route('/signedin',methods=['GET', 'POST'])
   def signed_in():
      if request.method == 'GET':
          messages = get_messages_from_table()
          comments = get_message_comments()
          user = session['name']
          return render_template('profile/index.html', messages = messages,comments = comments,user=user)
      else:
          return redirect(url_for('site.signed_in'))

             
Yönetici Platformundan Çıkış Fonksiyonu
---------------------------------------
Yönetici çıkış yapmak istediğinde session değeri "" değerini alır ve oturum kapanır, ardından BeeLink anasayfasına yönlendirilir.

.. code-block:: python 

   @site.route('/administrator/exit')
   def administrator_exit():
      session['name'] = ""
      return render_template('home.html')

Giriş ve Giriş Sorgulama  
-------------------------
Giriş
------
Bu tablo giriş işlemleri için tasarlanmıştır ve 2 tane dış anahtarı vardır ve "LOGIN" tablosundan bu değerleri silme ve güncelleme izinli işlemler yapılabilir. id SERIAL ve birincil anahtardır.

.. code-block:: python

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
          
Giriş Sorgulama İşlemleri
-------------------------
Kullanıcı veya yönetici, kullanıcı adını ve parolasını girdikten sonra bu değerler "USERSIGNUP" tablosunda sorgulanır. Girilen değerler veritabanıyla uyuşuyorsa yönetici olup olmadığı sorgulanır. Eğer yönetici giriş yapmışsa 2 değeri geri gönderilerek yönetici ana sayfasına yönlendirilir. Kullanıcı giriş yaptıysa 1 değerini alır ve platforma geçer. Girilen değerler veritabanıyla uyuşmuyorsa 0 değerini geri göndererek hata sayfasına yönlendirilir.

.. code-block:: python

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
          
Yönetici Sorgulama Fonksiyonu
-----------------------------
Username parametresi ve "SELECT" fonksiyonu ile veritabanında sorgulanır. Eğer kayıt varsa bu kaydın yönetici olup olmadığına göre farklı değerler gönderilir. 

.. code-block:: python

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

Yönetici Not İşlemleri  
----------------------
Yönetici not işlemleri için tanımlanan tablodur. Tabloda "note" kaydolacak metinleri içerir. "id" SERIAL ve birincil anahtardır. Dış anahtar ile LOGIN tablosundan kullanıcı adı güncelleme ve silme izinli alınır.

.. code-block:: python

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


Notları Görüntüleme Sayfası
---------------------------
Sayfada tüm notlar görüntülenir ve silme işleminde post methodu ile id alınarak silme fonksiyonu çalışır. Güncelleme işleminde ise get methodu ile id alınarak güncelleme fonksiyonuna gider.

.. code-block:: html

   <table border="1">
    <tr>
    <th>Note ID</th>
    <th>Note</th>
    <th>Delete Note</th>
    <th>Update Note</th>
    </tr>
    </tr>
    {% for i in notes %}
    {% if i %}
    <tr>
    <td>{{i[0]}}</td>
    <td>{{i[1]}}</td>
    <td>
    <form action="{{url_for('site.remove_admin_note')}}" method="post" name="delete"><button type="submit"    value="{{ i[0] }}" name="delete">Delete</button>
    </form>
    </td>
    <td>
    <form role="form" action="{{url_for('site.update_admin_note', id = i[0])}}" method="get" name="update"><button type="submit" value="{{ i[0] }}" name="update">Update</button>
    </form>
    </td>
    </tr>
      {% endif %}
     {% endfor %}
    </table>
  
Notları Görüntüleme Fonksiyonu
------------------------------
Yönetici sadece kendi notlarını görebildiği ve işlem yapabildiği için oturum bilgileri alınır ve sadece kendi notları sorgulanarak alınır. Ve not sayfasına eşleşen notlar gönderilir.

.. code-block:: python

   @site.route('/administrator/notes', methods=['GET','POST'])
   def administrator_notes():
      username = session['name']
      notes = notes_from_admins(username)
      return render_template('notes.html', notes = notes)
      
Veritabanından Notları Görüntüleme
----------------------------------
Username parametresi ile çalışır. "SELECT" fonksiyonu ile ADMINNOTES ve LOGIN tablosundan eşleştiği yerde parametrede ikisiyle eşleşiyorsa, eşleşen notlar alınır ve notes üzerinden gönderilir.

.. code-block:: python

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

Notları Güncelleme Sayfası
--------------------------
Yönetici, kendi notunu boş olan yazı kutusu üzerine yazarak güncelleyebilir. Method post yöntemidir ve yazılan yazı form ile gönderilir.

.. code-block:: html

   <form method="post" action="#">
   <div class="12u">
      <input type="text" name="note" id="note" value="" placeholder="Notu güncelleyin" required autofocus>
   </div>
   <br/>
   <div class="row uniform">
                  <div class="12u">
                    <ul class="actions align-center">
                      <li><input type="submit" name="signup" value="Kaydet"></li>
                    </ul>
                  </div>
   </div>
   </form>
  
Notları Güncelleme Fonksiyonu
-----------------------------
Update.htmlden gelen bilgiler, post methodu ile request.form verileri ile çekilir ve id değeri ile güncelleme fonksiyonuna yönlendirilir. Ardından oturum bilgilerinden kullanıcı adı alınır ve ona ait notlar notes.html sayfasına gönderilir.

.. code-block:: python

   @site.route('/administrator/note/update/<int:id>', methods=['GET', 'POST'])
   def update_admin_note(id):
      if request.method == 'GET':
          return render_template('updatenode.html')
      else:
          note = request.form['note']
          username = session['name']
          update_adminnote(note, id)
          notes = notes_from_admins(username)
          return render_template('notes.html', notes = notes)
          
Veritabanında Notları Güncelleme Fonksiyonu
-------------------------------------------
Veri tabanına note değeri ile id değeri gelerek sorgulanır. Id değerinin uyduğu kayıtta güncelleme yapılır.

.. code-block:: python

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

Notları Ekleme Sayfası
----------------------
Yönetici boş olan text kutusuna girmek istediği notu girerek post methodu ile kaydeder.

.. code-block:: html

   <form method="post" action="#">
   <div class="12u">
      <input type="text" name="note" id="note" value="" placeholder="Notu giriniz" required autofocus>
   </div>
   <br/>
   <div class="row uniform">
                  <div class="12u">
                    <ul class="actions align-center">
                      <li><input type="submit" name="signup" value="Kaydet"></li>
                    </ul>
                  </div>
   </div>
  
Notları Ekleme Fonksiyonu
-------------------------
Post methodu ile gelen veri, oturum ile gelen kullanıcı adı ile birlikte addnote_from_admin fonksiyonuna yönlendirerek veri tabanına ekleme işlemi yapılır. Ardından, yönetici not sayfasına yönlendirilir.

.. code-block:: python

   @site.route('/administrator/addnote', methods=['GET','POST'])
   def administrator_add_note():
      if request.method == 'GET':
          return render_template('addnote.html')
      else:
          note = request.form['note']
          username = session['name']
          addnote_from_admin(note, username)
      return redirect(url_for('site.administrator_notes'))
      
Veritabanına Notları Ekleme Fonksiyonu
--------------------------------------
Note değeri ve username parametreleri ile gelerek, "INSERT" fonksiyonu ile tabloya kayıt eklenir.

.. code-block:: python

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

Notları Silme Fonksiyonu
------------------------
Get methodu ile gelen silme fonksiyonu tekrar aynı sayfaya yönlendirir, bu sefer butona tıklanıldığında post methodu ile yollanır ve tıklanıldığı notun id değerini request.formdan alarak işlem yapılır. Sonra oturum bilgisi alınır ve o yöneticiye ait notların sıralandığı notes.html sayfasına yönlendirilir.

.. code-block:: python

   @site.route('/administrator/note/remove', methods=['GET', 'POST'])
   def remove_admin_note():
      if request.method == 'GET':
          return render_template('notes.html')
      else:
          note_id = request.form['delete']
          remove_adminnote(note_id)
          username = session['name']
          notes = notes_from_admins(username)
          return render_template('notes.html', notes = notes)

Veritabanından Notları Silme
----------------------------
Id parametresini alan remove_adminnote veritabanından id sorgulanarak eğer doğru sonuç verdiyse veritabanından kayıt silinir.

.. code-block:: python

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
