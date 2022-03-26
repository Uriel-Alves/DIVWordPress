from asc.core import session_factory

from src.models.wordpress import Post


if __name__ == '__main__':

    session = session_factory()
    post = session.query(Post).first()
    print(post)