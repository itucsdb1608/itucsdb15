import os

from page_handlers import site
from flask import Flask
from flask.globals import session, request
from connect_db import init_message_table
from connect_db import init_profile_table
from connect_db import create_login

def create_app():
    app = Flask(__name__)
    app.register_blueprint(site)
    app.init_message_table = init_message_table()
    app.init_profile_table = init_profile_table()
    app.create_login = create_login()
    return app

def main():
    app=create_app()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()

