from microstate.conventions import MicroStateConventions

STATE_SERVER_CONVENTIONS_ARGS = ('obscurity', 'max_bytes')

try:
    from microconventions.redis_conventions import PY_REDIS_ARGS, FAKE_REDIS_ARGS
except ImportError:
    print('Falling back to hardwired redis args. You should probably upgrade to microconventions>0.1.0')
    PY_REDIS_ARGS = (
        'host', 'port', 'db', 'username', 'password', 'socket_timeout', 'socket_keepalive', 'socket_keepalive_options',
        'connection_pool', 'unix_socket_path', 'encoding', 'encoding_errors', 'charset', 'errors',
        'decode_responses', 'retry_on_timeout', 'ssl', 'ssl_keyfile', 'ssl_certfile', 'ssl_cert_reqs', 'ssl_ca_certs',
        'ssl_check_hostname', 'max_connections', 'single_connection_client', 'health_check_interval', 'client_name')
    FAKE_REDIS_ARGS = ('decode_responses',)


class StateServerConventions(MicroStateConventions):

    def __init__(self, obscurity=None, max_bytes=400, max_locations=200, **kwargs):
        super().__init__(**kwargs)
        self._obscurity = (obscurity or "obscure") + self.SEP
        self.MAX_BYTES = max_bytes
        self.MAX_LOCATIONS = max_locations

    def state_location(self, write_key:str, k:int) -> str:
        return self._obscurity + write_key + self.SEP + str( int(k) % self.MAX_LOCATIONS )

    def state_ttl(self, write_key:str) ->int:
        """ State will survive a long weekend if write_key has difficulty at least 11 """
        difficulty = self.key_difficulty(write_key)
        if difficulty >= 11:
            return 60 * 60 * 72
        else:
            return 60 * 70

    def state_max_size(self, write_key:str, k:int) -> int:
        """ To accommodate two styles of use, the first virtual memory
            location is allowed to be as large as the others' combined.

               k: logical location is integer in the set {0,..,self.MAX_LOCATIONS}

        """
        difficulty = self.key_difficulty(write_key)
        if difficulty is None:
            return 0
        elif difficulty >= 11:
            return self.MAX_BYTES if k>0 else self.MAX_LOCATIONS*self.MAX_BYTES
        else:
            return int( self.MAX_BYTES / 100. ) if k>0 else self.MAX_LOCATIONS*self.MAX_BYTES