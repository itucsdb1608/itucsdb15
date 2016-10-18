import datetime
import os

from flask import Flask
from flask import Blueprint, render_template
from flask import redirect, url_for
from flask import request

app = Flask(__name__)

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



if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
