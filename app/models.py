from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from .database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    caught = Column(Boolean, nullable=False)
    party = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
