"""Commom tests for all steps."""

from behave import then
import json

from api import connect_db


def verify_response(response, status_code):
    """Verify if response has the given status_code."""
    assert response is not None
    assert response.status_code == status_code


def post_json_data(client, endpoint, text_data):
    """Make a POST using JSON data to an endpoint."""
    data = json.loads(text_data)
    response = client.post(endpoint, json=data, follow_redirects=True)
    verify_response(response, 201)
    return response


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
    db = connect_db()
    Entity = db.entity(table)
    assert db.session.query(Entity).count() == count


@then('the operation succeeds')
def _then_authentication_succeeds(context):
    verify_response(context.response, 200)


@then(u'the operation fails with code {http_code:d}')
def _then_operation_fails_with_code(context, http_code):
    verify_response(context.response, http_code)
