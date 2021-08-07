from sqlalchemy import Column, String
from database.database import Base


class Channel(Base):
    __tablename__ = 'channel'

    id = Column('id', String, primary_key=True)
    title = Column('title', String)
    thumbnail = Column('thumbnail', String)
