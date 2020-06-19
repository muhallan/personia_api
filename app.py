import os
from flask import Flask
from flask_cors import CORS
from config import config_dict

app = Flask(__name__)
app.config.from_object(config_dict[os.getenv('APP_CONFIG')])
# add support for CORS for all end points
CORS(app, resources={r"/*": {"origins": "*"}})

# for removing trailing slashes enforcement
app.url_map.strict_slashes = False

from models.models import db
from auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run()
