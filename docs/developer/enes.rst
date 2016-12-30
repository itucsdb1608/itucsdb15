Hayati Enes Basat Tarafından Tamamlanan Kısımlar
======================================

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
-------

.. code-block:: python
  class Person:
    def __init__(self, name, surname, email, username, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.username = username
        self.password = password

Login.py dosyası altında tutulan bu sınıf, kullanıcı tarafından girilen bu beş değerin olması açısından önemli ve veri tabanı işlemleri için yardımcı olmaktadır.

Kullanıcı Ekleme Sayfası ve İşlemleri
-------

Kullanıcı Ekleme Sayfası
----
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
----
Post methodundaki formun bilgileri request.form aracılığı ile aktarılır ve Person sınıfı yardımı ile yeni kayıt oluşturulur. Oluşturulan kayıt add_to_login fonksiyonuna yönlendirilir.

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
----

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
----
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
----            
Post methodundaki formun bilgileri request.form aracılığı ile aktarılır ve Person sınıfı yardımı ve yetki türü ile yeni kayıt oluşturulur. Oluşturulan kayıt add_from_admin fonksiyonuna yönlendirilir.

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
----     
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
--------------

Kullanıcı Görüntüleme Sayfası
----
Yönetici panelinden tüm kullanıcılar görüntülenebilir.
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
----

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
----

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
----

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
----

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
----

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
----

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
--------------
Giriş
----
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
----
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
----

  .. code-block:: html
  {% extends "base.html" %}
  {% block title %}Oops!{% endblock %}

  {% block content %}

  <script type="text/javascript">
    alert("You have entered invalid username or password.")
  </script>
  {% endblock %}
  
Yönetici Sayfasına Giriş Fonksiyonu
----

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
----

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
----

.. code-block:: python 
  @site.route('/administrator/exit')
  def administrator_exit():
      session['name'] = ""
      return render_template('home.html')

Giriş ve Giriş Sorgulama  
--------------
Giriş
----

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
----

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
----

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
--------------

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


Notları Görüntüleme Sayfası
----

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
    <form action="{{url_for('site.remove_admin_note')}}" method="post" name="delete"><button type="submit" value="{{ i[0] }}" name="delete">Delete</button>
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
----

.. code-block:: python
  @site.route('/administrator/notes', methods=['GET','POST'])
  def administrator_notes():
      username = session['name']
      notes = notes_from_admins(username)
      return render_template('notes.html', notes = notes)
      
Veritabanından Notları Görüntüleme
----

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
----

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
----

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
----

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
----

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
----

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
----

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
----

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
----

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
