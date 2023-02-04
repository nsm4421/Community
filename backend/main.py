from typing import Optional

import uvicorn
from fastapi import FastAPI
from config.configuration import get_configuration

c = get_configuration()

def create_app():
    app = FastAPI()
    # TODO - initialize app
    return app

app = create_app()

@app.route("/")
def index():
    return "Hi"

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=c.PORT, 
        reload=c.RELOAD
    )