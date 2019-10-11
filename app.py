from api.api import *
from flask import Flask

app = Flask(__name__)
app.register_blueprint(redmine_api)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
