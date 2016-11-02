import os

from page_handlers import site
from flask import Flask
from connect_db import init_message_table

def create_app():
    app = Flask(__name__)
    app.register_blueprint(site)
    app.init_message_table = init_message_table()
    return app

def main():
    app=create_app()
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()

