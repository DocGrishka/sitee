import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Manufacture(SqlAlchemyBase):
    __tablename__ = 'manufactures'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    Company = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Town = sqlalchemy.Column(sqlalchemy.String, nullable=True)



