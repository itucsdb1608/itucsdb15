import os

from page_handlers import site
from flask import Flask
from connect_db import connect_and_init

app = Flask(__name__)
app.register_blueprint(site)
app.connect_and_init = connect_and_init()

def main():
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
