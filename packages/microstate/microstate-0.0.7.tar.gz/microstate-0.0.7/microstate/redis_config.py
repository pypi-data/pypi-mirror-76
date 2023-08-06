import os
from sys import platform
from getjson import getjson


# Retrieve credentials for database where state is stored

try:
    from microstate.redis_env_private import NOTHING_MUCH
except ImportError:
    # Environment variables need to be set some other way, for example as github secrets
    pass

state_config_url = os.getenv('REDIS_CONFIG_URL')
if state_config_url is None:
    raise Exception('Cannot get environment variable REDIS_CONFIG_URL')

state_config_failover_url = os.getenv('REDIS_CONFIG_FAILOVER_URL')
if state_config_url is None:
    raise Exception('Cannot get environment variable REDIS_CONFIG_FAILOVER_URL')

REDIS_CONFIG = getjson(url=state_config_url, failover_url=state_config_failover_url)

state_test_config_url = os.getenv('REDIS_TEST_CONFIG_URL')
if state_config_url is None:
    raise Exception('Cannot get environment variable REDIS_TEST_CONFIG_URL')

state_test_config_failover_url = os.getenv('REDIS_TEST_CONFIG_FAILOVER_URL')
if state_config_url is None:
    raise Exception('Cannot get environment variable REDIS_TEST_CONFIG_FAILOVER_URL')

REDIS_TEST_CONFIG = getjson(url=state_test_config_url, failover_url=state_config_failover_url)

if REDIS_CONFIG is None:
    raise Exception('Could not get configuration')

if platform == 'darwin':
    REDIS_CONFIG['local'] = True
