from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from asc.core.database.model import Model


class Post(Model):
    __tablename__ = 'wp_posts'

    id = Column(Integer, primary_key=True, name='ID')
    name = Column(VARCHAR, name='post_name')
    title = Column(VARCHAR, name='post_title')
    status = Column(VARCHAR, name='post_status')
    content = Column(Text, name='post_content')
    date = Column(DATETIME, name='post_date_gmt')
