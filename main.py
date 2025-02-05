from fastapi import FastAPI

from user_endpoints.router import router as user_router
from admin_endpoints.router import router as admin_router
from transact_endpoints.router import router as tr_router
from auth_endpoints.router import router as th_router

app = FastAPI()

app.include_router(th_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(tr_router)

@app.get('/')
async def home_page():
    return {'page': 'home'}


