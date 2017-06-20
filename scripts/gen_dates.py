import random
from random_date import randomDate
from sqlalchemy import *

db = create_engine('mysql://root:123456@localhost/bionomo_dev')
conn = db.connect()

db.echo = True

metadata = MetaData(db)

collections = Table('collection', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('last_date', Date),
                    Column('last_year', String(100)),
                    Column('province', String(100))
                    )

s = select([collections]).where(collections.c.last_date != None)
result = conn.execute(s)

start_date = '1/1/1940'
end_date = '1/1/2005'
_format = '%d/%m/%Y'


def get_random_province():
    provinces = ['Maputo', 'Gaza', 'Inhambane', 'Sofala', 'Manica', 'Tete', 'Quelimane', 'Nampula', 'Niassa',
                 'Cabo Delgado']
    return provinces[random.randrange(0, 9)]


def get_cabo_delgado():
    return 'Cabo Delgado'

row_index_list = [i for i in range(110185)]

max_items_to_set_to_cabo_delgado = int(110185/15)
from random import randrange
index_list = [randrange(0, 110185) for _ in range(max_items_to_set_to_cabo_delgado)]


def udpate_to_cabo_delgado():
    for row in result:
        if row['id'] in index_list:
            _date = randomDate(start_date, end_date, random.random(), format=_format).date()
            _year = _date.year
            _province = get_cabo_delgado()
            stmt = collections.update().where(collections.c.id == row['id'])\
                              .values(province=_province)
            print('Updating province [{} => \'{}\']'.format(row['id'], _province))
            conn.execute(stmt)


def update_all():
    for row in result:
        _date = randomDate(start_date, end_date, random.random(), format=_format).date()
        _year = _date.year
        _province = get_random_province()
        stmt = collections.update().where(collections.c.id == row['id'])\
                          .values(last_date=_date, last_year=_year, province=_province)
        print('{} =>(\'{}\', \'{}\')'.format(row['id'], _province, _year))
        conn.execute(stmt)


udpate_to_cabo_delgado()
