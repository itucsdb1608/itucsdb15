from flask import Flask
from flask import Blueprint, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site)

    return app


if __name__ == '__main__':
    app = create_app()
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
