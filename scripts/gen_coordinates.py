import random
from random_date import randomDate
from sqlalchemy import *

db = create_engine('mysql://root:123456@localhost/bionomo_dev')
conn = db.connect()

db.echo = True

metadata = MetaData(db)

collections = Table('collection', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('latitude', Date),
                    Column('longitude', String(100)),
                    )

s = select([collections])
result = conn.execute(s)

# limits on latitude and longitude
# lat_min: -16.4571588
# lat_max: -14.99785187
# lon_min: 32.87658691
# lon_max: 40.46813965
lat = (-16.4571588, -14.99785187)
lon = (32.87658691, 40.46813965)


def get_cabo_delgado():
    return 'Cabo Delgado'

row_index_list = [i for i in range(110185)]

max_items_to_set_to_cabo_delgado = int(110185/15)
from random import randrange
index_list = [randrange(0, 110185) for _ in range(max_items_to_set_to_cabo_delgado)]


def udpate_coordinates_longitude():
    for row in result:
        if row['id'] in index_list:
            _lon = random.uniform(lon[0], lon[1])

            stmt = collections.update().where(collections.c.id == row['id'])\
                              .values(longitude=_lon)

            print('Updating longitude [{} => \'{}\']'.format(row['id'], _lon))
            conn.execute(stmt)


udpate_coordinates_longitude()
