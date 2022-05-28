import logging
from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import Pool

load_dotenv()

log = logging.getLogger('kernel-application')
env = environ

if 'DB_ENGINE' in env:
	engine_url = env['DB_ENGINE']
else:
	engine_url = f'postgresql+psycopg2://{env["DB_USER"]}:' \
    	         f'{env["DB_PASS"]}@{env["DB_HOST"]}/' \
        	     f'{env["DB_NAME"]}'

@event.listens_for(Pool, 'checkout')
def on_pool_checkout(dbapi_conn, connection_rec, connection_proxy):

	if 'DB_ENGINE' in env:
		return False

	if not Base.metadata.schema:
		#log.warning('POOL CHECKOUT without schema')
		#print('WARN.... NOT BASE METADATA YET')
		pass

	cursor_sql = "SET SEARCH_PATH TO %s" % Base.metadata.schema
	cursor_obj = dbapi_conn.cursor()
	cursor_obj.execute(cursor_sql)

try:
	engine = create_engine(
		url=engine_url,
		pool_size=10,
		max_overflow=20,
		pool_recycle=10
	)

	Base = declarative_base()
	session_factory = sessionmaker(bind=engine)

except Exception as e:
	print('exauted? ', e)
finally:
	print('done?')
