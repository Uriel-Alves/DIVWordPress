import multiprocessing
import os

from dotenv import load_dotenv

load_dotenv()

workers = multiprocessing.cpu_count() * 2 + 1
threads = (workers - 1) * 8

debug = False
daemon = False
preload_app = True

wsgi_app = 'wsgi:app'

bind = [f"{os.environ.get('WSGI_HOST', '127.0.0.1')}:"
        f"{os.environ.get('WSGI_PORT', 5001)}"]

if os.environ.get('GUNICORN_DAEMON','false').lower() == 'true':
    daemon = True
    
if os.environ.get('WSGI_DEBUG','true').lower() == 'true':
    debug = True
    reload = True
    loglevel = 'debug'

print('DAEMON',daemon)
print('DEBUG',debug)
print('WORKES',workers)
print('THREADS',threads)