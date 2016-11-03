from flask import Blueprint, render_template
from flask import current_app
from flask import request
from flask import redirect, url_for
from connect_db import add_message_to_table,get_messages_from_table,remove_message_from_table,update_one_message
from message import Message
from connect_db import add_to_login, Person

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
    return render_template('profile/index.html')

@site.route('/signin')
def sign_in():
    return render_template('girisyap.html')

@site.route('/contactus')
def contact():
    return render_template('iletisim.html')

@site.route('/message/update',methods=['GET','POST'])
def update_message():
    if request.method == 'GET':
        return render_template('profile/update_message.html')
    else:
        username = request.form['username']
        content = request.form['content']
        subject = request.form['subject']
        update_one_message(content,subject,username)
        return redirect(url_for('site.signed_in'))

@site.route('/message/delete',methods=['GET','POST'])
def delete_message():
    if request.method == 'GET':
        return render_template('profile/delete_message.html')
    else:
        username = request.form['username']
        remove_message_from_table(username)
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

@site.route('/signedin',methods=['GET', 'POST'])
def signed_in():
    if request.method == 'GET':
        messages = get_messages_from_table()
        return render_template('profile/index.html', messages = messages)
    else:
        return redirect(url_for('site.signed_in'))

@site.route('/profile')
def profile():
    return render_template('profile/profil.html')

@site.route('/messages')
def messages():
    return render_template('profile/mesaj.html')

@site.route('/friends')
def friend_requests():
        return render_template('profile/arkadas.html')

@site.route('/aboutus')
def aboutus():
    return render_template('about.html')

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

