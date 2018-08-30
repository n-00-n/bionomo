from bionomo_pilot import Components

db = Components.db


class DatabaseService(object):
    def create_database(self):
        db.create_all()
