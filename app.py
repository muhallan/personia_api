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

if __name__ == '__main__':
    app.run()
