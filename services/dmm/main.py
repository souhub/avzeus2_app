from fastapi import FastAPI, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from middlewares import http_log
from routers.actress import router as actress_router
from routers.floor import router as floor_router
from routers.genre import router as genre_router
from routers.item import router as item_router
from routers.download import router as download_router


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
    item_router,
    prefix='/item',
    tags=['item']
)

router.include_router(
    download_router,
    prefix='/download',
    tags=['download']
)


@router.get('/health')
async def health_check():
    return 'A page for health check.'

# if env.APP_ENV == 'development':
#     app = FastAPI()
# else:
#     app = FastAPI(docs_url=None,
#                   redoc_url=None,
#                   openapi_url=None)
app = FastAPI()

app.include_router(
    router,
    prefix='/v1'
)

app.add_middleware(BaseHTTPMiddleware, dispatch=http_log)

origins = [
    'http://localhost:3000',
    'https://www.avzeus.net'
    # 'http://172.22.0.1:3000'
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )
