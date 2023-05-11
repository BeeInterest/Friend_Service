from psycopg2 import OperationalError
from sqlalchemy import create_engine, Table, MetaData
import psycopg2

con = psycopg2.connect(
    database="friend_service", user='postgres',
    password='1qwe2rty', host='postgres_friend'
)
con.autocommit = True
cursor = con.cursor()
fd = open('user/postgres/init_postgres.sql', 'r', encoding='utf-8')
sql = fd.read()
fd.close()
sqlcom = sql.split(';')
for command in sqlcom:
    try:
        cursor.execute(sql)
    except OperationalError as msg:
        print("Command skipped: ", msg)
con.commit()
con.close()

engine = create_engine('postgresql://postgres:1qwe2rty@postgres_friend/friend_service')
meta = MetaData()

users_table = Table(
    'users',
    meta,
    extend_existing=True,
    autoload_with=engine
)

relations_table = Table(
    'relations',
    meta,
    extend_existing=True,
    autoload_with=engine
)
conn = engine.connect()