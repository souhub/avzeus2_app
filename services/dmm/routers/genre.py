from typing import Optional
import schemas
from dmm_client import DMMClient
from fastapi import APIRouter

from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get('/search', response_model=schemas.GenreResult)
async def genre_search(floor_id: Optional[int] = 43, initial: Optional[str] = None, hits: Optional[int] = None, offset: Optional[int] = None, output: Optional[str] = 'json'):
    """
    Get genres with all the information

    - **floor_id**: [フロアID] フロア検索APIから取得可能なフロアID
    - **initial**: [頭文字5] 50音をUTF-8で指定
    - **hits**: [取得件数] 初期値：100　最大：500
    - **offset**: [検索開始位置]  初期値 1
    - **output**: [出力形式]　json/xml
    """
    client = DMMClient()
    response = client.genre_search(floor_id, initial, hits, offset, output)
    return response.json()['result']
