from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from Flask_Quiz import app, db

app.config.from_object('config.DevelopmentConfig')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()
