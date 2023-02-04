from dataclasses import asdict
import uvicorn
from os import environ
from fastapi import FastAPI
from config.configuration import get_configuration
from database.connection import custom_database, custom_base
from sqlalchemy.ext.declarative import declarative_base
from routes.auth.auth_route import auth_router

custom_config = asdict(get_configuration())

def create_app():
    app = FastAPI()
    # TODO - initialize app
    custom_database.init_app(app=app, **custom_config)
    app.include_router(auth_router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=custom_config.get("PORT", 8000), 
        reload=custom_config.get("RELOAD", True)
    )