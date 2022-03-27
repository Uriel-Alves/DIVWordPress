from flask import jsonify
from flask import request

from core.wordpress import get_post
from src.routes import app, session
from src.message import NOT_FOUND_POST
from src.models.wordpress import Post

@app.route('/posts', methods=['GET'])
def GET_post_last():
    content = []

    posts = get_post()
    query_search = request.args.get('search')

    if query_search:
        posts = posts.filter(
            Post.post_title.ilike(f'%{query_search.strip()}%')
        )

    posts = posts.limit(10).all()

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