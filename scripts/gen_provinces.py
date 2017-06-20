import datetime
import random

from random_date import randomDate
# date = datetime.date.

from sqlalchemy import *

db = create_engine('mysql://root:123456@localhost/bionomo_dev')
conn = db.connect()

db.echo = True

metadata = MetaData(db)

collections = Table('collection', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('province', String(100)),
                    )

s = select([collections])
result = conn.execute(s)


def get_random_province():
    provinces = ['Maputo', 'Gaza', 'Inhambane', 'Sofala', 'Manica', 'Tete', 'Quelimane', 'Nampula', 'Niassa',
                 'Cabo Delgado']
    return provinces[random.randrange(0, 9)]

#
# for row in result:
#
#     _province = get_random_province()
#     stmt = collections.update().where(collections.c.id == row['id']).values(province=_province)
#     print('{} => {}' % format(row['id'], _province))
#     conn.execute(stmt)
