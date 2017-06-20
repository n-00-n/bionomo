from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from bionomo_pilot import Components, create_app
from bionomo_pilot.config import env
from bionomo_pilot.config import config_by_name

app = create_app(env)
db = Components.db
app.debug = True

# ugly but the migrate needs it's models
from bionomo_pilot.models import Provider, Collection, Multimedia
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host=config_by_name[env].SERVER_HOST, port=config_by_name[env].SERVER_PORT))

if __name__ == '__main__':
    manager.run()
