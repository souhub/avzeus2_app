from typing import Optional, List
import schemas
from dmm_client import DMMClient
from fastapi import APIRouter
from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get('/search', response_model=List[schemas.Actress])
async def actress_search(initial: Optional[str] = None, actress_id: Optional[int] = None, keyword: Optional[str] = None, gte_bust: Optional[str] = None, lte_bust: Optional[str] = None, gte_waist: Optional[str] = None, lte_waist: Optional[str] = None,	gte_hip: Optional[str] = None,
                         lte_hip: Optional[str] = None,	gte_height: Optional[str] = None, lte_height: Optional[str] = None, gte_birshday: Optional[str] = None, lte_birthday: Optional[str] = None, hits: Optional[int] = None, offset: Optional[int] = None, sort: Optional[str] = None):
    """
    女優情報を取得する

    - **initial**: [頭文字5] 50音をUTF-8で指定
    - **actress_id** [女優ID]
    - **keyword** [キーワード] UTF-8で指定
    - **gte_bust** [バスト] gte_bust=90ならバスト90cm以上
    - **lte_bust** [バスト] lte_bust=90ならバスト90cm以下
    - **gte_waist** [ウエスト] gte_waist=90ならウエスト90cm以上
    - **lte_waist** [ウエスト] lte_waist=90ならウエスト90cm以下
    - **gte_hip** [ヒップ] gte_hip=90ならヒップ90cm以上
    - **lte_hip** [ヒップ] lte_hip=90ならヒップ90cm以下
    - **gte_height** [身長] gte_height=90なら身長90cm以上
    - **lte_height** [身長] lte_height=90なら身長90cm以下
    - **gte_birthday** [誕生日] gte_birthday=1990-01-01なら1990年1月1日以降生まれ
    - **lte_birthday** [誕生日] lte_birthday=1990-01-01なら1990年1月1日以前生まれ
    - **hits**: [取得件数] 初期値：20　最大：100
    - **offset**: [検索開始位置]  初期値 1
    - **sort**: [ソート順] name, -name, bust, -bust, waist, -waist, hip, -hip, height, -height, birthday, -birthday, id, -id
    - **output**: [出力形式]　json/xml
    """

    client = DMMClient()
    response = client.actress_search(initial, actress_id, keyword, gte_bust, lte_bust, gte_waist, lte_waist,
                                     gte_hip, lte_hip, gte_height, lte_height, gte_birshday, lte_birthday, hits, offset, sort)
    return response.json()['result']['actress']
