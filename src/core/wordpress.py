import re

from asc.core import session_factory

from models.wordpress import Post


def get_post(*query):
    session = session_factory()

    if not query:
        query = Post

    return session \
        .query(query) \
        .filter(
            Post.status=='publish',
            Post.type=='post'
        ) \
        .order_by(Post.date.desc())

def get_post_content(content:str):
    return re.sub(
        pattern='\<\!\-{2}\ \/?wp\:(\w*)\ \-{2}\>',
        repl='',
        string=content
    )
