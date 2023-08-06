import os

import requests


def filter_env_vars(prefix):
    """
    Matches all environment variables with a certain prefix.
    Returns a dict with the key of the variable without the prefix.

    Example:
        env vars:
            - CI_API_KEY=key
            - CI_URL=https://httpbin.org
            - BASE_URL=https://example.com
        prefix:
            - CI_

        result:
            - {'API_KEY': "key", 'URL': "https://httpbin.org"}
    """
    return {
        k.lstrip(prefix): os.getenv(k)
        for k in dict(os.environ).keys()
        if k.startswith(prefix)
    }


def get_config_vars(base_url, headers, app_name):
    """ Returns a dict with the config vars from a Heroku app """
    url = f"{base_url}/apps/{app_name}/config-vars"

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    return {
        k: v for k, v in res.json().items() if k not in ["DATABASE_URL", "REDIS_URL"]
    }
