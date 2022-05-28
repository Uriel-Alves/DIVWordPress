from core import session_factory

from core.wordpress import get_post, get_post_content
from models.wordpress import Post


if __name__ == '__main__':

    session = session_factory()
    post = get_post(Post).where(
        Post.name=='bordado-de-caico-esta-na-vitrine-das-lojas-riachuelo-da-avenida-paulista'
    ).first()
    print(get_post_content(post.content))
    print(post.post_meta)