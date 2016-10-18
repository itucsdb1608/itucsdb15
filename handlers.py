from flask import Blueprint, render_template
from flask import redirect, url_for
from flask import request

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