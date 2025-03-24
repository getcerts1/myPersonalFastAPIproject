import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Ensure project path is set
from fastapi import FastAPI
from db.database import engine, Base
from api.v1 import post_routes, user_routes, login, admin_routes


Base.metadata.create_all(bind=engine)

app = FastAPI()

#app.include_router(post_routes)
app.include_router(user_routes.router)
app.include_router(login.router)
app.include_router(admin_routes.router)


