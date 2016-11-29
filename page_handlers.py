from flask import Blueprint, render_template
from flask import current_app
from flask import request
from flask import redirect, url_for
from connect_db import add_message_to_table,get_messages_from_table,remove_message_from_table,update_one_message
from message import Message
from login import Person
from connect_db import add_profile_to_table,get_profile_from_table,remove_profile_from_table,update_profile_from_table
from profile import Profile
from connect_db import add_to_login, records_from_login, update_to_login, remove_from_login, search_user_login
from connect_db import ekle_arkadas, sil_arkadas, duzenle_arkadas,tum_arkadaslar
from friend import Friend
from connect_db import add_personal_message, tum_mesajlar,update_personal_message,remove_personal_message

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
            return redirect(url_for('site.signed_in'))
        else:
            return render_template('error.html')


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

@site.route('/friend/change', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def friend():
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Ekle':
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            ekle_arkadas(isim, soyisim)
            return redirect(url_for('site.friend_requests'))
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

@site.route('/friend/arkadasListesi')                       #arkadas.html in icinde kullanildi
def friend_listing():
     tumu = tum_arkadaslar()
     return render_template('profile/arkadas.html', arkadaslar = tumu)



@site.route('/signedin',methods=['GET', 'POST'])
def signed_in():
    if request.method == 'GET':
        messages = get_messages_from_table()
        return render_template('profile/index.html', messages = messages)
    else:
        return redirect(url_for('site.signed_in'))


@site.route('/admin/blog/update',methods=['GET','POST'])
def update_blog():
    if request.method == 'GET':
        return render_template('admin/blog_guncelle.html')
    else:
        blog_id = request.form['blog_id']
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        update_profile_from_table(username,title,content,blog_id)
        return redirect(url_for('site.blog'))

@site.route('/admin/blog/delete',methods=['GET','POST'])
def delete_blog():
    if request.method == 'GET':
        return render_template('admin/blog_sil.html')
    else:
        blog_id = request.form['blog_id']
        remove_profile_from_table(blog_id)
        return redirect(url_for('site.blog'))
@site.route('/admin/blog/add',methods=['GET','POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('admin/blog_ekle.html')
    else:
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        newProfile = Profile(username,title,content)
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

@site.route('/friends')
def friend_requests():
        return render_template('profile/arkadas.html')

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

@site.route('/messages/add', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def personal_send():
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Add':
            touser = request.form['UserName']
            content = request.form['PersonalContent']
            add_personal_message(touser, content)
            return redirect(url_for('site.personel_message_request'))
@site.route('/messages/mesajlar')
def mesaj_listing(): #yeni
     tumu = tum_mesajlar()
     return render_template('profile/mesaj.html', mesajlar = tumu)
@site.route('/messages/update',methods=['GET','POST'])
def update_message_1():
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    else:
        username = request.form['UserName']
        content = request.form['PersonalContent']
        update_personal_message(username,content)
        return redirect(url_for('site.personel_message_request'))
@site.route('/messages/delete',methods=['GET','POST'])
def delete_personel_message():
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    else:
        username = request.form['UserName']
        remove_personal_message(username)
        return redirect(url_for('site.personel_message_request'))
