from typing import Optional
import schemas
from dmm_client import DMM_client
from fastapi import APIRouter
from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get('/list', response_model=schemas.FloorResult)
async def floor_list(output: Optional[str] = 'json'):
    """
    Get floors with all the information

    - **output**: [出力形式] json/xml
    """
    client = DMM_client()
    response = client.floor_list(output)
    return response.json()['result']
