from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models import Model


class Post(Model):
    __tablename__ = 'wp_posts'

    id = Column(Integer, primary_key=True, name='ID')
    type = Column(VARCHAR, name='post_type')
    name = Column(VARCHAR, name='post_name')
    guid = Column(VARCHAR, name='guid')
    title = Column(VARCHAR, name='post_title')
    status = Column(VARCHAR, name='post_status')
    content = Column(Text, name='post_content')
    date = Column(DATETIME, name='post_date_gmt')

    attachments = relationship('PostMeta',
                              lazy='joined',
                              primaryjoin="and_("
                                          "PostMeta.id_post=="
                                          "Post.id,"
                                          "PostMeta.key=="
                                          "'_wp_attached_file')"
                              )
    ###metas = relationship('PostMeta', lazy='joined', back_populates='post')

    def as_dict(self):
        dict = vars(self)
        del dict['_sa_instance_state']
        return dict


class PostMeta(Model):
    __tablename__ = 'wp_postmeta'

    id = Column(Integer, primary_key=True, name='meta_id')
    id_post = Column(Integer,
                     ForeignKey(Post.id),
                     primary_key=True,
                     name='post_id'
    )
    key = Column(VARCHAR, name='meta_key')
    value = Column(VARCHAR, name='meta_value')

    #post = relationship(Post, lazy='joined')
    """
    EXECUTA QUERY, PORÉM NÃO RETORNA ATTACHMENT. LENTO!
    attachment = relationship(Post, primaryjoin="and_(PostMeta.value=="
                                                "Post.id,"
                                                "PostMeta.key=="
                                                "'_wp_attached_file')",
                              foreign_keys=[Post.id]

    )
    """



    def as_dict(self):
        dict = vars(self)
        del dict['_sa_instance_state']
        return dict
