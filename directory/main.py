from fastapi import Depends, FastAPI

from directory.dependencies import get_api_key
from directory.routers.routers import router as organization_router

app = FastAPI()

app.include_router(organization_router, dependencies=[Depends(get_api_key)])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Organization API"}
