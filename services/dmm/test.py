from dmm_client import DMM_client

dmm_client = DMM_client()
res = dmm_client.genre_search()
print(res.json()['result']['genre'][0])
