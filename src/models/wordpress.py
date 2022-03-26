from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from asc.core.database.model import Model


class Post(Model):
    __tablename__ = 'wp_posts'

    ID = Column(Integer, primary_key=True)
    post_name = Column(VARCHAR)
    post_title = Column(VARCHAR)
    post_status = Column(VARCHAR)
    post_content = Column(Text)
    post_date_gmt = Column(DATETIME)
