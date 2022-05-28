from flask import jsonify
from flask import request

from core.wordpress import get_post, Post
from routes import app
from message import NOT_FOUND_POST
from models.wordpress import PostMeta

@app.route('/posts', methods=['GET'])
def GET_post_last():
    content = []

    posts = get_post()
    query_search = request.args.get('search')

    if query_search:
        posts = posts.filter(
            Post.title.ilike(f'%{query_search.strip()}%')
        )

    posts = posts.limit(10).all()

    if not posts:
        return {
            'message': NOT_FOUND_POST
        }, 404

    for post in posts:

        """
        post_image = session.query(PostMeta.value).where(
            Post.id==post.id,
            PostMeta.key=='_wp_attached_file',
        ).first()

        """
        post = post.as_dict()
        attachments = post.pop('attachments')
        post_data = {
            **post,
            'attachments': [],
            'meta': []
        }

        for attach in attachments:
            post_data.append('attachments')

        #for meta in metas:
        #    print(meta.attachment)
        #    post_data['meta'].append(meta.as_dict())

        print(post_data)
        content.append(post_data)


    return jsonify(content), 200

@app.route('/post/<slug>', methods=['GET'])
def GET_post_slug(slug:str):
    content = {}

    post = get_post() \
        .filter(Post.name==slug.strip().lower()) \
        .first()

    if not post:
        return {
            'message': NOT_FOUND_POST
        }, 404

    postagem = {
        'id':post.id,
        'slug':post.name,
        'title':post.title,
        'image':post.attachments.value if post.attachments else False,
        'content':post.content
    }

    return postagem, 200