from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.env import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

DATABASE = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)

engine = create_engine(
    DATABASE,
    encoding='utf-8',
    # echo=True
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = SessionLocal.query_property()
Base.metadata.create_all(bind=engine)


# DBセッションの作成
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
