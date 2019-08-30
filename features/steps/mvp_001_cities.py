"""Implement steps related to the City objects behavior."""

from behave import given, when
from features.steps.common import verify_response, post_json_data


def __add_city_to_database(client, cityname, cname):
    request = {
        "name": cityname,
        "cname": cname
    }
    return client.post('/city', data=request, follow_redirects=True)


#
#
#

@given('a database with no cities')
def _given_empty_database(context):
    # TODO: this is clearly wrong, and based on unwritten assumptions.
    assert context.db


@when('I add the city "{cityname}" with cname "{cname}"')
def _when_adding_a_city(context, cityname, cname):
    context.response = __add_city_to_database(context.client, cityname, cname)
    verify_response(context.response, 201)


@when('I add a city with the JSON data')
def _when_adding_a_city_with_json(context):
    post_json_data(context.client, '/city', context.text)


@given('the city "{cityname}" with cname "{cname}" exists in the database')
def _given_database_has_city(context, cityname, cname):
    context.response = __add_city_to_database(context.client, cityname, cname)
    verify_response(context.response, 201)


@when('I want to list all cities in the database')
def _when_listing_cities(context):
    context.response = context.client.get('/cities')
    verify_response(context.response, 200)
