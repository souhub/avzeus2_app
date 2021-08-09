from typing import Optional
import utils.env as env
import requests


class DMMClient():
    def __init__(self) -> None:
        self.api_key = env.DMM_API_KEY
        self.affiriate_key = env.DMM_AFFIRIATE_KEY
        self.version = env.DMM_API_VERSION

    def _get_base_path(self, api_name: str) -> str:
        return 'https://api.dmm.com/affiliate/{}/{}?api_id={}&affiliate_id={}'.format(
            self.version, api_name, self.api_key, self.affiriate_key)

    def floor_list(self, output: str) -> requests.Response:
        params = {'output': output}
        request_url = self._get_base_path('FloorList')
        response = requests.get(request_url, params=params)
        return response

    def genre_search(self, floor_id: int, initial: str, hits: int, offset: int, output: str) -> requests.Response:
        params = {'floor_id': floor_id, 'initial': initial,
                  'hits': hits, 'offset': offset, 'output': output}
        request_url = self._get_base_path('GenreSearch')
        response = requests.get(request_url, params=params)
        return response

    def all_genres_convert_to_csv(self, floor_id: int, hits: int, offset: int) -> requests.Response:
        params = {'floor_id': floor_id, 'hits': hits, 'offset': offset}
        request_url = self._get_base_path('GenreSearch')
        response = requests.get(request_url, params=params)
        return response

    def actress_search(self, initial: Optional[str] = None, actress_id: Optional[int] = None, keyword: Optional[str] = None, gte_bust: Optional[str] = None, lte_bust: Optional[str] = None, gte_waist: Optional[str] = None, lte_waist: Optional[str] = None,	gte_hip: Optional[str] = None,
                       lte_hip: Optional[str] = None,	gte_height: Optional[str] = None, lte_height: Optional[str] = None, gte_birshday: Optional[str] = None, lte_birthday: Optional[str] = None, hits: Optional[int] = None, offset: Optional[int] = None, sort: Optional[str] = None) -> requests.Response:
        params = {'initial': initial, 'actress_id': actress_id, 'keyword': keyword, 'gte_bust': gte_bust, 'lte_bust': lte_bust, 'gte_waist': gte_waist, 'lte_waist': lte_waist, 'gte_hip': gte_hip,
                  'lte_hip': lte_hip, 'gte_height': gte_height, 'lte_height': lte_height, 'gte_birshday': gte_birshday, 'lte_birthday': lte_birthday, 'hits': hits, 'offset': offset, 'sort': sort}
        request_url = self._get_base_path('ActressSearch')
        response = requests.get(request_url, params=params)
        return response

    def all_actress_convert_to_csv(self, hits: Optional[int] = None, offset: Optional[int] = None, sort: Optional[str] = None) -> requests.Response:
        params = {'hits': hits, 'offset': offset, 'sort': sort}
        request_url = self._get_base_path('ActressSearch')
        response = requests.get(request_url, params=params)
        return response

    def item_list(self, site: str, service: Optional[str] = None, floor: Optional[str] = None, hits: Optional[int] = None, offset: Optional[int] = None, sort: Optional[str] = None, keyword: Optional[str] = None, cid: Optional[str] = None, article: Optional[str] = None, gte_date: Optional[str] = None, lte_date: Optional[str] = None, mono_stock: Optional[str] = None, output: Optional[str] = None):
        params = {'site': site, 'service': service, 'floor': floor, 'hits': hits, 'offset': offset, 'sort': sort,
                  'keyword': keyword, 'cid': cid, 'article': article, 'gte_date': gte_date, 'lte_date': lte_date, 'mono_stock': mono_stock, 'output': output}
        request_url = self._get_base_path('ItemList')
        response = requests.get(request_url, params=params)
        return response
