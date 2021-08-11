from typing import List, Optional
import schemas
from dmm_client import DMMClient
from fastapi import APIRouter

from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get('/list', response_model=List[schemas.Item])
async def items(site: str = 'FANZA', service: Optional[str] = None, floor: Optional[str] = None, hits: Optional[int] = None, offset: Optional[int] = None, sort: Optional[str] = None, keyword: Optional[str] = None, cid: Optional[str] = None, article: Optional[str] = None, gte_date: Optional[str] = None, lte_date: Optional[str] = None, mono_stock: Optional[str] = None, output: Optional[str] = 'json') -> schemas.ItemResult:
    client = DMMClient()
    response = client.item_list(site, service, floor, hits, offset, sort,
                                keyword, cid, article, gte_date, lte_date, mono_stock, output)
    return response.json()['result']['items']
