"""Steps for MVP 001: Eventos."""

from behave import given, when, then
import json
from features.steps.common import verify_response, post_json_data
# from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
# from flask import request, jsonify


@when('I create an event for "{institution}", {days:d} days from now')
def _when_adding_an_event(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    data = json.loads(request.format(institution=institution, date=date))
    context.response = context.client.post('/event', data=data,
                                           follow_redirects=True)
    verify_response(context.response, 201)


@when('I use JSON to add an event for "{institution}", {days:d} days from now')
def _when_adding_an_event_with_JSON(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    request = request.format(institution=institution, date=date)
    context.response = post_json_data(context.client, '/event', request)
    verify_response(context.response, 201)


@given('there is an event for "{institution}", {days:d} days from now')
def _given_an_event(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    request = request.format(institution=institution, date=date)
    verify_response(post_json_data(context.client, '/event', request), 201)


@when('I ask for future events')
def _when_retrieving_events(context):
    context.response = context.client.get('/events')
    verify_response(context.response, 200)


@then(u'with a date {days:d} days in the future, the resulting JSON is')
def _then_json_added_with_date_is(context, days):
    observed = context.response.get_json(force=True)
    date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")
    expected = json.loads(context.text)
    expected[0]['date'] = date
    print("OBSERVED", observed)
    print("EXPECTED", expected)
    assert expected == observed
