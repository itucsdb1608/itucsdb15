from flask import Blueprint, render_template
from flask import current_app
from flask import request, session
from flask import redirect, url_for
from connect_db import add_message_to_table,get_messages_from_table,remove_message_from_table,update_one_message
from message import Message
from login import Person
from connect_db import add_profile_to_table,get_profile_from_table,remove_profile_from_table,update_profile_from_table
from profile import Profile
from connect_db import add_to_login, records_from_login, update_to_login, remove_from_login, search_user_login
from connect_db import ekle_arkadas,tum_arkadaslar,gonder_username,toplam_arkadas,sil_arkadas,guncelle_arkadas
from friend import Friend
from connect_db import send_message,send_username_for_messages,update_personal_message,sil_kisisel_mesaj

site = Blueprint('site', __name__)
@site.route('/')
def home_page():
    return render_template('home.html')

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
        add_to_login(newRecord)
    return render_template('home.html')

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
        else:
            return render_template('error.html')

@site.route('/cikis', methods=['GET'])
def cikis():
    session['name'] = ""
    return redirect(url_for('site.home_page'))


@site.route('/contactus')
def contact():
    return render_template('iletisim.html')

@site.route('/message/<int:messageId>/update',methods=['GET','POST'])
def update_message(messageId):
    if request.method == 'GET':
        return render_template('profile/update_message.html')
    else:
        content = request.form['content']
        subject = request.form['subject']
        update_one_message(content,subject,messageId)
        return redirect(url_for('site.signed_in'))

@site.route('/message/delete',methods=['GET','POST'])
def delete_message():
    if request.method == 'GET':
        return render_template('profile/index.html')
    else:
        id = request.form['delete']
        remove_message_from_table(id)
        return redirect(url_for('site.signed_in'))

@site.route('/message/add',methods=['GET','POST'])
def add_message():
    if request.method == 'GET':
        return render_template('profile/add_message.html')
    else:
        username = request.form['username']
        messageSubject = request.form['subject']
        messageContent = request.form['content']
        newMessage = Message(username,messageContent,messageSubject)
        add_message_to_table(newMessage)
        return redirect(url_for('site.signed_in'))

@site.route('/friends')
def friend_requests():
        return render_template('profile/arkadas.html')

@site.route('/friend/change', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def friend():
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Ekle':
            kullaniciadi = request.form['UserName']
            arkullaniciadi = request.form['FriendUserName']
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            ekle_arkadas(kullaniciadi,arkullaniciadi,isim, soyisim)
            toplamarkadas = toplam_arkadas(kullaniciadi)
            tumu = gonder_username(kullaniciadi)
            username = kullaniciadi
          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = username  )
        elif request.form['submit'] == 'Duzenle':
            id = request.form['FriendID']
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            duzenle_arkadas(id,isim,soyisim);
            return redirect(url_for('site.friend_requests'))
        elif request.form['submit'] == 'Sil':
            id = request.form['FriendID']
            sil_arkadas(id)
            return redirect(url_for('site.friend_requests'))
        elif request.form['submit'] == 'UsernameGonder':
            username = request.form['Username']
            tumu = gonder_username(username)
            toplamarkadas = toplam_arkadas(username)
           # tumu = tum_arkadaslar()
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ) #olmazsa render ile dene



@site.route('/friend/ekle/<my>', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def friend_add(my):
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Ekle':

            arkullaniciadi = request.form['FriendUserName']
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            ekle_arkadas(my,arkullaniciadi,isim, soyisim)
            toplamarkadas = toplam_arkadas(my)
            tumu = gonder_username(my)
            username = my
          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = username  )



@site.route('/friend/gonder', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def gonder_fr():
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.form['submit'] == 'UsernameGonder':
         username = request.form['Username']
         tumu = gonder_username(username)
         toplamarkadas = toplam_arkadas(username)
         # tumu = tum_arkadaslar()
         return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas , myusername = username )
        # return redirect(url_for('site.friend',arkadaslar = tumu , toplam = toplamarkadas ))
        # return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ) #olmazsa render ile dene

@site.route('/friend/arkadasListesi')                       #arkadas.html in icinde kullanildi
def friend_listing():
     tumu = tum_arkadaslar()
     return render_template('profile/arkadas.html', arkadaslar = tumu)


@site.route('/friend/guncel/<my>', methods=['GET', 'POST'])
def friend_update(my):
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Guncelle':
            ad = my
            arkullaniciadi =  request.form['FriendUserName']
            yeniisim = request.form['FriendName']
            yenisoyisim = request.form['FriendSurname']
            guncelle_arkadas(ad, arkullaniciadi,yeniisim, yenisoyisim)
            toplamarkadas = toplam_arkadas(ad)
            tumu = gonder_username(ad)

          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = ad  )

@site.route('/friend/guncelle/<friendusername>/<myname>', methods=['GET', 'POST'])
def friend_real_update(friendusername , myname):
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Guncelle':
            ad = myname
            arkullaniciadi = friendusername
            yeniisim = request.form['FriendName']
            yenisoyisim = request.form['FriendSurname']
            guncelle_arkadas(ad, arkullaniciadi,yeniisim, yenisoyisim)
            toplamarkadas = toplam_arkadas(ad)
            tumu = gonder_username(ad)
            username = ad
          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = username  )

@site.route('/friend/sil/<username>/<myusername>', methods=['GET', 'POST'])
def friend_delete(username, myusername):
    if request.method == 'POST':
        a = username
        sil_arkadas(a)

        tumu = gonder_username(myusername)
        toplamarkadas = toplam_arkadas(myusername)
        return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas , myusername = myusername )
    else:
        return redirect(url_for('site.friend'))



@site.route('/un')
def usernamefr_requests():
        return render_template('profile/arkadasgiris.html')


@site.route('/signedin',methods=['GET', 'POST'])
def signed_in():
    if request.method == 'GET':
        messages = get_messages_from_table()
        return render_template('profile/index.html', messages = messages)
    else:
        return redirect(url_for('site.signed_in'))


@site.route('/admin/blog/<int:blog_id>/update',methods=['GET','POST'])
def update_blog(blog_id):
    if request.method == 'GET':
        return render_template('admin/blog_guncelle.html')
    else:
        title = request.form['title']
        content = request.form['content']
        update_profile_from_table(title,content,blog_id)
        return redirect(url_for('site.blog'))

@site.route('/admin/blog/delete',methods=['GET','POST'])
def delete_blog():
    if request.method == 'GET':
        return render_template('admin/blog.html')
    else:
        blog_id = request.form['delete']
        remove_profile_from_table(blog_id)
        return redirect(url_for('site.blog'))
@site.route('/admin/blog/add',methods=['GET','POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('admin/blog_ekle.html')
    else:
        user_name = session['name']
        title = request.form['title']
        content = request.form['content']
        newProfile = Profile(user_name,title,content)
        add_profile_to_table(newProfile)
        return redirect(url_for('site.blog'))

@site.route('/admin/blog',methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        profile_blog = get_profile_from_table()
        return render_template('admin/blog.html', profile_blog = profile_blog)
    else:
        return redirect(url_for('site.blog'))

@site.route('/profile')
def profile():
    profile_blog = get_profile_from_table()
    return render_template('profile/profil.html', profile_blog = profile_blog)

@site.route('/messages')
def personel_message_request():
    return render_template('profile/mesaj.html')



@site.route('/aboutus')
def aboutus():
    records = records_from_login()
    return render_template('about.html', records = records)

@site.route('/user/remove', methods=['GET', 'POST'])
def remove_user():
    if request.method == 'GET':
        return render_template('about.html')
    else:
        user_id = request.form['delete']
        remove_from_login(user_id)
        records = records_from_login()
        return render_template('about.html', records = records)

@site.route('/user/update/', methods=['GET', 'POST'])
def update_user():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        id = request.form['id_num']
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        updateRecord = Person(name, surname, email, username, password)
        update_to_login(id, updateRecord)
        records = records_from_login()
        return render_template('about.html', records = records)

@site.route('/admin/login')
def admin_login():
        return render_template('admin/login.html')

@site.route('/admin/home',methods=['GET', 'POST'])
def admin_home():
    if request.method == 'GET':
        return redirect(url_for('site.home_page'))
    else:
        return render_template('admin/index.html')

@site.route('/admin/kisisel')
def admin_kisisel():
        return render_template('admin/kisisel.html')

@site.route('/messages')
def message_request():
        return render_template('profile/mesaj.html')


@site.route('/personalmessage/send/<my>', methods=['GET', 'POST'])
def personal_send(my):
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Add':

            touser = request.form['UserName']
            mesaj = request.form['PersonalContent']

            send_message(my,touser,mesaj)

            all = send_username_for_messages(my)
            username = my
            return render_template('profile/mesaj.html',bilgiler = all ,  myusername = username )


@site.route('/personalmessageupdate/<my>', methods=['GET', 'POST'])
def personal_message_update(my):
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Update':

            touser = request.form['UserName']
            mesaj = request.form['PersonalContent']

            update_personal_message(my,touser,mesaj)

            all = send_username_for_messages(my)
            username = my
            return render_template('profile/mesaj.html',bilgiler = all ,  myusername = username )




@site.route('/mesaj/gonder', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def take_username():
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.form['submit'] == 'Send':
         username = request.form['Username']
         all = send_username_for_messages(username)
         return render_template('profile/mesaj.html',bilgiler = all , myusername = username )


@site.route('/pmgiris')
def pmessage_request():
        return render_template('profile/mesajgiris.html')




@site.route('/mesaj/sil/<username>/<myusername>/<mesaj>', methods=['GET', 'POST'])
def personal_message_delete(username, myusername,mesaj):
    if request.method == 'POST':

        sil_kisisel_mesaj(username,mesaj)
        all = send_username_for_messages(myusername)

        return render_template('profile/mesaj.html',bilgiler = all , myusername = myusername )
    else:
        return redirect(url_for('site.message_request'))
