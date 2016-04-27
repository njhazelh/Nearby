from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    """
    User Database class
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)


class Session(Base):

    """
    Session Database Class
    """
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_hash = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires = Column(DateTime, nullable=False)


class Device(Base):

    """
    Device Database Class
    """
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True)
    mac = Column(String, index=True, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class Observation(Base):

    """
    Observations Database Class
    """
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
