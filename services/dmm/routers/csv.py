from typing import Optional
from pandas.io.json import json_normalize
from dmm_client import DMM_client
from fastapi import APIRouter
from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get('/actresses')
async def all_actresses_convert_to_csv(total_count: Optional[int] = 1000):
    client = DMM_client()
    all_data = []
    count = 0
    # total_count = client.all_actress_convert_to_csv(
    #     hits=0, offset=1, sort='id').json()['result']['total_count']
    next_offset = 1

    while count < int(total_count):
        response = client.all_actress_convert_to_csv(
            hits=100, offset=next_offset, sort='id')
        data = response.json()['result']['actress']
        all_data += data
        next_offset += 100
        count += len(data)
        print('count: ', count)

    data_json = json_normalize(all_data)
    data_json.to_csv('./actress.csv', encoding='utf-8')
    print(data_json)
    return data


@router.get('/all-genres')
async def all_genres_convert_to_csv(floor_id: int):
    client = DMM_client()
    all_data = []
    total_count = client.all_genres_convert_to_csv(
        floor_id=floor_id, hits=1, offset=1).json()['result']['total_count']
    count = 0
    next_offset = 1

    while count < int(total_count):
        response = client.all_genres_convert_to_csv(
            floor_id=floor_id, hits=100, offset=next_offset)
        data = response.json()['result']['genre']
        all_data += data
        next_offset += 100
        count += len(data)

    data_json = json_normalize(all_data)
    data_json.to_csv('./genres_{}.csv'.format(floor_id), encoding='utf-8')
    return data
