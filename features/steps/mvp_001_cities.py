"""Implement steps related to the City objects behavior."""

from behave import given, when
from features.steps.common import (
    verify_response, post_json_data, add_authentication, login_admin)


def __add_city_to_database(context, cityname, cname):
    request = {
        "name": cityname,
        "cname": cname
    }
    headers = add_authentication(context)
    return context.client.post('/city', data=request, headers=headers,
                               follow_redirects=True)


@given('a database with no cities')
def _given_empty_database(context):
    # TODO: this is clearly wrong, and based on unwritten assumptions.
    assert context.db


@when('I add the city "{cityname}" with cname "{cname}"')
def _when_adding_a_city(context, cityname, cname):
    context.response = __add_city_to_database(context, cityname, cname)


@when('I add a city with the JSON data')
def _when_adding_a_city_with_json(context):
    context.response = post_json_data(context, '/city')


@given('the city "{cityname}" with cname "{cname}" exists in the database')
@login_admin
def _given_database_has_city(context, cityname, cname):
    response = __add_city_to_database(context, cityname, cname)
    verify_response(response, 201)
    context.execute_steps('when the user ends its session')


@when('I want to list all cities in the database')
def _when_listing_cities(context):
    context.response = context.client.get('/cities')
    verify_response(context.response, 200)
