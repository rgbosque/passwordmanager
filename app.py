import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'pm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRETY_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
