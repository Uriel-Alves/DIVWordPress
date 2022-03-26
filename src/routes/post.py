from flask import jsonify

from src.routes import app, session
from src.message import NOT_FOUND_POST
from src.models.wordpress import Post


query_post = (
    Post.ID.label('id'),
    Post.post_name.label('slug'),
    Post.post_title.label('title'),
    Post.post_date_gmt.label('date'),
    Post.post_content.label('content'),
)

def get_post(*query):
    return session \
        .query(*query_post, *query) \
        .filter(Post.post_status=='publish') \
        .order_by(Post.post_date_gmt.desc())

@app.route('/posts', methods=['GET'])
def GET_post_last():
    content = []

    posts = get_post().limit(10).all()

    if not posts:
        return {
            'message': NOT_FOUND_POST
        }, 404

    for post in posts:
        content.append(post._asdict())

    return jsonify(content), 200

@app.route('/post/<slug>', methods=['GET'])
def GET_post_slug(slug:str):
    content = {}

    post = get_post() \
        .filter(Post.post_name==slug.strip().lower()) \
        .first()

    if not post:
        return {
            'message': NOT_FOUND_POST
        }, 404

    return post._asdict(), 200