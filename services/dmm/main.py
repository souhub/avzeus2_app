from fastapi import FastAPI, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware
from middlewares import http_log
import utils.env as env
from routers.actress import router as actress_router
from routers.floor import router as floor_router
from routers.genre import router as genre_router
from routers.csv import router as csv_router

router = APIRouter()

router.include_router(
    actress_router,
    prefix='/actress',
    tags=['actress']
)

router.include_router(
    floor_router,
    prefix='/floor',
    tags=['floor']
)

router.include_router(
    genre_router,
    prefix='/genre',
    tags=['genre']
)

router.include_router(
    csv_router,
    prefix='/csv',
    tags=['csv']
)


@router.get('/health')
async def health_check():
    return 'A page for health check.'

if env.APP_ENV == 'development':
    app = FastAPI()
else:
    app = FastAPI(docs_url=None,
                  redoc_url=None,
                  openapi_url=None)

app.include_router(
    router,
    prefix='/v1'
)

app.add_middleware(BaseHTTPMiddleware, dispatch=http_log)
