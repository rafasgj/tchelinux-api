"""Commom tests for all steps."""

import json
from functools import wraps

from behave import given, then


def login_admin(callable):
    """Force execution of a step with admin priviledges."""
    @wraps(callable)
    def decorator(context, *args, **kwargs):
        # login
        step = 'Given the user has administrator priviledges'
        context.execute_steps(step)
        # execute
        result = callable(context, *args, **kwargs)
        # logout
        context.execute_steps("given the user ends its session")
        # return result
        return result
    return decorator


def verify_response(response, status_code):
    """Verify if response has the given status_code."""
    assert response is not None
    # print("CODES (observed/expected)", response.status_code, status_code)
    # print("RESPONSE", response.data)
    assert response.status_code == status_code


def post_json_data(context, endpoint):
    """Make a POST using JSON data to an endpoint."""
    txt = context.request if hasattr(context, "request") else context.text
    data = txt if type(txt) in (dict, list) else json.loads(txt)
    headers = add_authentication(context)
    response = context.client.post(endpoint, json=data, headers=headers,
                                   follow_redirects=True)
    return response


def add_authentication(context):
    """Add context authentication token."""
    if hasattr(context, 'authentication'):
        return {"Authorization": "Bearer {}".format(context.authentication)}
    else:
        return {}


def user_register(context, **kwargs):
    """Register user passed as JSON text."""
    user = """{{"name":"{name}", "email":"{email}",
               "password":"{password}", "role": "{role}"}}"""
    if "name" not in kwargs:
        kwargs['name'] = "Someone"
    if "email" not in kwargs:
        kwargs['email'] = "someone@local"
    if "password" not in kwargs:
        kwargs['password'] = "12345"
    if "role" not in kwargs:
        kwargs['role'] = "user"
    data = json.loads(user.format(**kwargs))
    response = context.client.post('/user', data=data, follow_redirects=True)
    return response


def user_login(context, email, password):
    """Perform user login."""
    data = {"email": email, "password": password}
    ans = context.client.post('/login', data=data, follow_redirects=True)
    verify_response(ans, 200)
    return ans.json


def user_logout(context):
    """Perform logout of the current user."""
    headers = add_authentication(context)
    response = context.client.get('/logout', headers=headers)
    verify_response(response, 200)


@given('the user has administrator priviledges')
def _given_admin_is_authenticated(context):
    res = user_login(context, "admin@tchelinux.org", 123456)
    context.authentication = res["access_token"]


@then('the resulting JSON is')
def then_resulting_JSON_is(context):
    """Compare a response JSON to a given one an context text."""
    observed = context.response.get_json(force=True)
    # 'id' are auto-generated, and we don't care about them.
    if type(observed) == dict:
        del observed['id']
    elif type(observed) == list:
        for o in observed:
            if 'id' in o:
                del o['id']
    expected = json.loads(context.text)
    assert expected == observed


@then('there is {count:d} item in the table {table}')
def _then_there_are_N_cities_in_database(context, table, count):
    from api import connect_db
    db = connect_db()
    Entity = db.entity(table)
    assert db.session.query(Entity).count() == count


@then('the operation succeeds')
def _then_authentication_succeeds(context):
    verify_response(context.response, 200)


@then('the operation exits with code {http_code:d}')
def _then_operation_exits_with_code(context, http_code):
    verify_response(context.response, http_code)
