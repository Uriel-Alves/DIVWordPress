from os import environ

from routes import app

if __name__ == "__main__":
    app.run(
        host=environ.get('WSGI_HOST', '127.0.0.1'),
        port=environ.get('WSGI_PORT', 5001),
        debug=environ.get('WSGI_DEBUG', True),
    )
