"""Implement steps related with Institution objects behavior."""

from behave import given, when, then
from features.steps.common import (
    verify_response, post_json_data, add_authentication, login_admin)
import json


def __add_institution(context):
    institution = json.loads(context.text)
    headers = add_authentication(context)
    return context.client.post('/institution', data=institution,
                               headers=headers, follow_redirects=True)


@given('no institution exists')
def _given_no_institution_exits(context):
    # TODO: this is clearly wrong, and based on unwritten assumptions.
    assert context.db


@when('I add the institution from JSON data')
def _when_adding_an_institution_from_json(context):
    context.response = post_json_data(context, '/institution')


@when('I add the institution')
def _when_add_institution(context):
    context.response = __add_institution(context)
    verify_response(context.response, 201)


@then('there is {count:d} institution(s) in the database')
def _then_there_is_N_institutions(context, count):
    # TODO: actually implement it.
    pass


@given('an institution exists in the database')
@login_admin
def _given_an_institution(context):
    verify_response(__add_institution(context), 201)


@when('I want to list all institutions in the city "{city}"')
def _when_list_institutions_in_city(context, city):
    context.response = context.client.get('/institution/{}'.format(city))
    verify_response(context.response, 200)
