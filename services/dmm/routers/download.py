import collections
from typing import Container, Optional
from pandas.io.json import json_normalize
from dmm_client import DMMClient
from fastapi import APIRouter, Response, status
from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get('/actresses')
async def all_actresses_convert_to_csv(total_count: int = 500, sort='id', hits: int = 100):

    client = DMMClient()
    next_offset = 1
    all_data = []
    next_offset = 1

    # およそ total_count 個 になるまでデータ追加
    while len(all_data) <= total_count:
        response = client.all_actress_convert_to_csv(
            hits=hits, offset=next_offset, sort=sort)
        data = response.json()['result']['actress']
        all_data += data
        next_offset += hits

    # total_count 個になるまでデータ削除
    while len(all_data) > total_count:
        all_data.pop(-1)

    # ブラウザにダウンロードさせる
    filename = 'avzeus-actresses'
    df = json_normalize(all_data)

    return Response(content=df.to_csv(encoding='utf-8'), headers={'Content-Disposition': f'attachment; filename={filename}.csv', 'Content-Type': 'text/csv'})


@router.get('/actresses-by-rank')
async def actresses_by_rank(explore_total_count: int = 500, total_count: int = 10, site: str = 'FANZA', service: str = 'digital', floor: str = 'videoa', sort='date', hits: int = 100):
    """
    女優情報を total_count 人分 sort 順に csv ファイルに変換する

    - **total_count**: [出力したい女優の人数] default 1000
    - **site**: [サイト] 一般（DMM.com）かアダルト（FANZA）か
    - **service** [サービス] フロアAPIから取得できるサービスコードを指定
    - **floor** [フロア] フロアAPIから取得できるフロアコードを指定
    - **sort**: [ソート順] name, -name, bust, -bust, waist, -waist, hip, -hip, height, -height, birthday, -birthday, id, -id
    - **hits**: [取得件数] 初期値：20　最大：100
    """

    client = DMMClient()
    next_offset = 1
    all_data = []

    # およそ explore_total_count 個 になるまでデータ削除
    while len(all_data) <= explore_total_count:
        response = client.item_list(
            site=site, service=service, floor=floor, hits=hits, sort=sort, offset=next_offset)
        items = response.json()['result']['items']
        for item in items:
            # data が存在しない時エラーを起こす
            try:
                data = item['iteminfo']['actress']
            except:
                continue
            all_data += data
        next_offset += hits
        logger.debug(
            'progress... number of all_data: {}'.format(len(all_data)))

    # explore_total_count 個になるまでデータ削除
    while len(all_data) > explore_total_count:
        all_data.pop(-1)

    actresses_ids = []
    for actress in all_data:
        actresses_ids.append(actress['id'])

    # 各要素の数を数え、出現回数の多い順にIDを並べる
    # sorted_tuples は、 [(actress_id,出現回数),...] のタプルのリスト型となる
    c = collections.Counter(actresses_ids)
    sorted_tuples = c.most_common(total_count)

    sorted_actresses = []

    # ソートしたIDから名前を特定
    for tuple in sorted_tuples:
        id = tuple[0]
        number_of_appearances = tuple[1]
        response = client.actress_search(actress_id=id)
        # これがないとエラーで動かないときがある
        try:
            name = response.json()['result']['actress'][0]['name']
        except:
            continue
        sorted_actresses.append(
            {'id': id, 'name': name, 'number_of_appearances': number_of_appearances})

    # ブラウザにダウンロードさせる
    filename = 'avzeus-actresses-by-rank'
    df = json_normalize(sorted_actresses)

    return Response(content=df.to_csv(encoding='utf-8'), headers={'Content-Disposition': f'attachment; filename={filename}.csv', 'Content-Type': 'text/csv'})


@router.get('/genres-by-floor')
async def genres_by_floor(floor_id: int = 48):
    """
    特定の floorID 内のジャンル情報を csv ファイルに変換する

    - **floor_id**: [フロアID]
    """
    client = DMMClient()
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

    # ブラウザにダウンロードさせる
    filename = 'avzeus-genres-by-floor'
    df = json_normalize(all_data)

    return Response(content=df.to_csv(encoding='utf-8'), headers={'Content-Disposition': f'attachment; filename={filename}.csv', 'Content-Type': 'text/csv'})


@router.get('/items')
async def items(site: str = 'FANZA', total_count: int = 10000, hits: Optional[int] = 100, sort: Optional[str] = 'rank'):
    client = DMMClient()
    all_data = []
    total_count = total_count
    next_offset = 1

    # およそ total_count 個 になるまでデータ追加
    while len(all_data) <= total_count:
        response = client.item_list(
            site=site, hits=hits, offset=next_offset, sort=sort)

        for item in response.json()['result']['items']:
            try:
                content_id = item['content_id']
                title = item['title']

                genres = item['iteminfo']['genre']
                genre_ids = []
                for genre in genres:
                    genre_ids.append(genre['id'])

                # VR専用 は外す
                if 6793 in genre_ids:
                    continue

                actresses = item['iteminfo']['actress']
                actress_ids = []
                for actress in actresses:
                    actress_ids.append(actress['id'])

                data = {'content_id': content_id,
                        'title': title, 'genre': genre_ids, 'actress': actress_ids}

                all_data.append(data)
            except:
                continue

        next_offset += hits

    # total_count 個になるまでデータ削除
    while len(all_data) > total_count:
        all_data.pop(-1)

    # ブラウザにダウンロードさせる
    filename = 'avzeus-items'
    df = json_normalize(all_data)

    return Response(content=df.to_csv(encoding='utf-8'), headers={'Content-Disposition': f'attachment; filename={filename}.csv', 'Content-Type': 'text/csv'})
