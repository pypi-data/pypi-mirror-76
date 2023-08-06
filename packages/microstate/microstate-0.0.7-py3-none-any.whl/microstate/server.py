import fakeredis
import redis
import sys
import json

from microstate.server_conventions import StateServerConventions, STATE_SERVER_CONVENTIONS_ARGS, FAKE_REDIS_ARGS, PY_REDIS_ARGS

# Implements a tiny bit of management over pyredis to effect community storage


class MicroStateServer(StateServerConventions):

    def __init__(self, **kwargs):
        conventions_kwargs = dict([(k, v) for k, v in kwargs.items() if k in STATE_SERVER_CONVENTIONS_ARGS])
        super().__init__(**conventions_kwargs)

        # Initialize Rediz instance. Expects host, password, port   ... or default to fakeredis
        for k in conventions_kwargs.keys():
            kwargs.pop(k)
        self.redis_client = self.make_redis_client(**kwargs)

    @staticmethod
    def make_redis_client(**kwargs):
        # TODO: Move to microconventions or some redis utility package since this is used by rediz and also microstate
        kwargs["decode_responses"] = True  # Strong Rediz convention
        is_real = "host" in kwargs  # May want to be explicit here
        KWARGS = PY_REDIS_ARGS if is_real else FAKE_REDIS_ARGS
        redis_kwargs = dict()
        for k in KWARGS:
            if k in kwargs:
                redis_kwargs[k] = kwargs[k]
        if is_real:
            return redis.StrictRedis(**redis_kwargs)
        else:
            return fakeredis.FakeStrictRedis(**redis_kwargs)

    def get(self, write_key: str, k: int):
        location = self.state_location(write_key=write_key, k=k)
        return self.redis_client.get(name=location)

    def delete(self, write_key, k):
        location = self.state_location(write_key=write_key, k=k)
        execut = self.redis_client.delete(location)
        return {'operation': 'delete_state', 'result': execut}

    def set(self, write_key, k, value):
        max_bytes = self.state_max_size(write_key=write_key,k=k)
        if max_bytes:
            value_bytes = sys.getsizeof(value)
            if value_bytes <= max_bytes:
                data = self.to_redis_value(value=value)
                if data:
                    location = self.state_location(write_key=write_key, k=k)
                    ttl = self.state_ttl(write_key=write_key)
                    execut = self.redis_client.set(name=location, value=data, ex=ttl)
                    return {'operation': 'set_state', 'success': execut, 'max_bytes': max_bytes}
                else:
                    return {'operation': 'set_state', 'success': 1,
                            'message': 'value not a recognized type str,int,float, dict',
                            'max_bytes': max_bytes}
            else:
                return {'operation': 'set_state', 'success': 0, 'message': 'value too large', 'max_bytes': max_bytes}
        else:
            return {'operation': 'set_state', 'success': 0, 'message': 'invalid write key', 'max_bytes': max_bytes}


MicroStateServer.put = MicroStateServer.set