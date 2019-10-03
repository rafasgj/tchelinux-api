"""Set up testing environment."""

import json
import os
import tempfile

from behave import fixture, use_fixture


@fixture
def api_client(context, *args, **kwargs):
    """Create an API testing client."""
    from api import api
    context.db, api.config['DATABASE'] = tempfile.mkstemp(suffix=".sqlite")
    api.testing = True
    context.client = api.test_client()
    yield context.client
    # -- CLEANUP:
    os.close(context.db)
    os.unlink(format(api.config['DATABASE']))


@fixture
def api_config(context, *args, **kwargs):
    """Create an API configuration file."""
    config = {
        "JWT_SECRET_KEY": "super-secret",
        "JWT_BLACKLIST_ENABLED": True,
        "JWT_BLACKLIST_TOKEN_CHECKS": ["access", "refresh"],
        "DBUSERNAME": "somebody",
        "DBPASSWD": "asecret",
        "DATABASE": "tchelinuxcms",
        "admin": {
            "admin@tchelinux.org": "123456",
        }
    }
    print("JSON\n", json.dumps(config, indent=4))
    with open('apiconfig.json', 'w', encoding='utf-8') as cfg:
        json.dump(config, cfg, ensure_ascii=False, indent=4)
    yield context
    os.unlink('apiconfig.json')


def before_scenario(context, scenario):
    """Prepare context for testing scenario."""
    use_fixture(api_config, context)
    use_fixture(api_client, context)


def before_feature(context, feature):
    """Prepare context for testing feature."""
    pass
