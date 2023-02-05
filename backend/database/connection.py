import os
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

class CustomDatabase:

    def __init__(cls, app:FastAPI = None, **kds):
        cls._engine = None
        cls._session = None
        if app:
            cls.init_app(app, **kds)

    @classmethod
    def init_app(cls, app:FastAPI, **kds):

        # init engine
        cls._engine = create_engine(
            kds.get("DB_URL"),
            echo=kds.get("ECHO", True),
            pool_recycle=kds.get("POOL_RECYCLE", 900),
            pool_pre_ping=True,
        )

        # init session
        cls._session = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=cls._engine
        )

        @app.on_event("startup")
        def startup():
            cls._engine.connect()
            if (os.environ.get('API_ENV', 'dev') == 'dev'):
                metadata = MetaData()
                metadata.create_all(cls._engine)
            logging.info("DB connected...")

        @app.on_event("shutdown")
        def shutdown():
            cls._session.close_all()
            cls._engine.dispose()
            logging.info("DB disconnected...")

    @classmethod
    def get_session(cls):
        if cls._session is None:
            raise Exception("Session is not valid...")
        db_session = None
        try:
            db_session = cls._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def engine(cls):
        return cls._engine

    @property
    def session(self):
        return self.get_session

custom_database = CustomDatabase()

custom_base = declarative_base()