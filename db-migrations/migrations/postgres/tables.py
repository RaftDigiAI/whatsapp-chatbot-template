from typing import Type

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression


Base: Type = declarative_base()


class User(Base):
    """
    Users table
    """

    __table_args__ = {"schema": "webhook"}
    __tablename__ = "user"

    user_id = Column(INTEGER, primary_key=True)
    user_name = Column(String(256), nullable=True)
    phone_number = Column(String(64), nullable=False)
    phone_number_id = Column(String(128), nullable=False)


class Session(Base):
    """
    Sessions table
    """

    __table_args__ = {"schema": "webhook"}
    __tablename__ = "session"

    session_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey(User.user_id))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_archived = Column(Boolean, default=False, server_default=expression.false())
    communication_channel = Column(String(32))


class Message(Base):
    """
    Sessions table
    """

    __table_args__ = {"schema": "webhook"}
    __tablename__ = "message"

    message_id = Column(INTEGER, primary_key=True)
    session_id = Column(INTEGER, ForeignKey(Session.session_id), nullable=False)
    received_timestamp = Column(DateTime, nullable=False)
    replied_timestamp = Column(DateTime)
    user_message = Column(String(4096))
    bot_message = Column(String(4096))
    wa_message_id = Column(String(256))
    concatenated_message_id = Column(INTEGER)


class MessageStatus(Base):
    """
    Message status table
    """

    __table_args__ = {"schema": "webhook"}
    __tablename__ = "message_status"

    status_id = Column(INTEGER, primary_key=True)
    message_id = Column(INTEGER, ForeignKey(Message.message_id), nullable=False)
    status = Column(String(4096))
    timestamp = Column(DateTime)


class GptResponse(Base):
    """
    Sessions table
    """

    __table_args__ = {"schema": "webhook"}
    __tablename__ = "gpt_response"

    response_id = Column(INTEGER, primary_key=True)
    message_id = Column(INTEGER, ForeignKey(Message.message_id), nullable=False)
    prompt = Column(TEXT)


class MessageProcessing(Base):
    """
    Message processing table
    """

    __table_args__ = {"schema": "webhook"}
    __tablename__ = "message_processing"

    message_processing_id = Column(INTEGER, primary_key=True)
    session_id = Column(INTEGER, ForeignKey(Session.session_id), nullable=False)
    message_id = Column(INTEGER, ForeignKey(Message.message_id), nullable=False)
