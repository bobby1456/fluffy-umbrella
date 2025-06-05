from lifespan import lifespan
from fastapi import FastAPI
from api import router


app = FastAPI(lifespan=lifespan)
app.include_router(router, tags=["rooms"])