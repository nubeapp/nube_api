from .database import Base
from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class TmpCode(Base):
    __tablename__ = "tmpcodes"

    email = Column(String, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False)
    username = Column(String, nullable=False,
                      unique=True)
    name = Column(String, nullable=False)
    firstSurname = Column(String, nullable=True)
    secondSurname = Column(String, nullable=True)
    country = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
