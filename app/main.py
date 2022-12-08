from fastapi import FastAPI
from core.config import settings
from endpoints.api import api_router   
from starlette.middleware.cors import CORSMiddleware

# postgresql://postgres:changethis@db/app
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

DEBUG = True
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    if not DEBUG :
        app.add_middleware(
            CORSMiddleware,  
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else :
        app.add_middleware(
            CORSMiddleware,
            allow_origins='*',
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

@app.get("/")
async def root():
    return {"message": "Hello World"}
app.include_router(api_router, prefix=settings.API_STR)

