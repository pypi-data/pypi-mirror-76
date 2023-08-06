from microconventions import MicroConventions
from microconventions.value_conventions import ValueConventions
import json


class MicroStateConventions(MicroConventions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def to_redis_value(value):
        """ Used by MicroStateWriter prior to storage in redis database """
        # This may change if we move to using JSON redis module
        if ValueConventions.is_valid_value(value):
            return value
        elif isinstance(value, (list,dict,tuple)):
            if ValueConventions.has_nan(value):
                raise Exception('Values with NaN cannot be stored, sorry')
            else:
                try:
                    return json.dumps(value)
                except Exception as e:
                    raise Exception('Value cannot be JSON dumped so cannot be stored '+str(e) )

    @staticmethod
    def from_redis_value(value):
        """ Used by MicroStateWriter to infer a Python type """
        # Note: will not try to convert string back to int or float.
        # If you wish to preserve type then make it dict, tuple or list
        try:
            native = json.loads(value)
            if isinstance(native, (dict,list,tuple)):
                return native
            else:
                return value
        except Exception as e:
            return value
