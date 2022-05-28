from copy import deepcopy
from sqlalchemy import inspect

from core import Base

metadata = Base.metadata


class Model(Base):
    """ Classe base responsável por representar um
    modelo de dados abstrato. """

    __abstract__ = True
    __table_args__ = {
        'schema': metadata.schema
    }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def schema(cls, schema):
        if isinstance(cls.__table_args__, dict):
            cls.__table_args__.update({'schema': schema})
        else:
            cls.__table_args__ += ({'schema': schema},)
        return cls

    def update_db(self, keep=False, **fields):
        """ método responsável por realizar atribuição da
        classe com os campos obtidos em um dicionario. """

        if keep:
            mapper = inspect(self)
            primary_keys = [key.name for key in
                            inspect(self.__class__).primary_key]
            dict_object = self.as_dict()
            disjunction = set([a.key for a in mapper.attrs]) \
                          - set(list(fields.keys()))
            cleanup = {k: None for k in disjunction
                       if k not in primary_keys}
            dict_object.update(fields)
            dict_object.update(cleanup)
            fields = deepcopy(dict_object)

        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return f"<{type(self).__name__}>"

# end-of-file