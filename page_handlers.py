from flask import Blueprint, render_template
from flask import current_app
from flask import request
from flask import redirect, url_for

site = Blueprint('site', __name__)

@site.route('/')
def home_page():
    return render_template('home.html')

@site.route('/signup')
def sign_up():
    return render_template('giris.html')

@site.route('/signin')
def sign_in():
    return render_template('girisyap.html')

@site.route('/contactus')
def contact():
    return render_template('iletisim.html')

@site.route('/signedin',methods=['GET', 'POST'])
def signed_in():
    if request.method == 'GET':
        return render_template('profile/index.html')
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
