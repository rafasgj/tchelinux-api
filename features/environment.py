"""Set up testing environment."""

import os
import tempfile

from api import api

from behave import fixture, use_fixture


@fixture
def api_client(context, *args, **kwargs):
    """Create an API testing client."""
    context.db, api.config['DATABASE'] = tempfile.mkstemp(suffix=".sqlite")
    api.testing = True
    context.client = api.test_client()
    yield context.client
    # -- CLEANUP:
    os.close(context.db)
    os.unlink(format(api.config['DATABASE']))


def before_scenario(context, scenario):
    """Prepare context for testing scenario."""
    use_fixture(api_client, context)


def before_feature(context, feature):
    """Prepare context for testing feature."""
    pass
