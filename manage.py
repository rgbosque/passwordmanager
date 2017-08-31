# import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'pm.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = 'thisissecret'

migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
