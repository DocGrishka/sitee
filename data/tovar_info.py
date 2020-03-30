import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    Count = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Price = sqlalchemy.Column(sqlalchemy.String)
    Manufacture = sqlalchemy.Column(sqlalchemy.Integer)


