from microstate.conventions import MicroStateConventions
import requests

# Simple CRD storage tied to a write key


class MicroStateWriter(MicroStateConventions):

    def __init__(self, write_key, **kwargs):
        super().__init__(**kwargs)
        self.write_key = write_key
        self.method = 'state'

    def delete(self, k:int = 0):
        res = requests.delete(self.base_url + '/' + self.method + '/' + self.write_key, params={'k': k})
        if res.status_code == 200:
            return res.json()

    def get(self, k: int = 0):
        res = requests.get(self.base_url + '/' + self.method + '/' + self.write_key, data={'k': k})
        if res.status_code == 200:
            return self.from_redis_value(res.json())

    def set(self, value, k: int = 0):
        params = {'k': k, 'value': self.to_redis_value(value)}
        res = requests.put(self.base_url + '/' + self.method + '/' + self.write_key, params=params)
        if res.status_code == 200:
            return res.json()
