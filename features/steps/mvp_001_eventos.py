"""Steps for MVP 001: Eventos."""

from behave import given, when, then
import json
from features.steps.common import (
    verify_response, post_json_data, add_authentication, login_admin)
from datetime import datetime, timedelta


def _compare_event_in_days(expected, observed, days):
    date = datetime.today() + timedelta(days=days)
    expected['date'] = date.strftime("%Y-%m-%d")
    assert expected == observed


@when('I create an event for "{institution}", {days:d} days from now')
def _when_adding_an_event(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    data = json.loads(request.format(institution=institution, date=date))
    headers = add_authentication(context)
    context.response = context.client.post('/event', data=data,
                                           headers=headers,
                                           follow_redirects=True)


@when('I use JSON to add an event for "{institution}", {days:d} days from now')
def _when_adding_an_event_with_JSON(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    request = request.format(institution=institution, date=date)
    context.response = post_json_data(context, '/event', request)


@given('there is an event for "{institution}", {days:d} days from now')
@login_admin
def _given_an_event(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    context.date = date
    context.request = request.format(institution=institution, date=date)
    verify_response(post_json_data(context, '/event'), 201)


@given('there is an event that occurred {days:d} days ago in "{institution}"')
@login_admin
def _given_an_event_that_occured(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() - timedelta(days=days)
    context.date = date
    context.request = request.format(institution=institution, date=date)
    verify_response(post_json_data(context, '/event'), 201)


@when('I ask for future events')
def _when_retrieving_events(context):
    context.response = context.client.get('/events')
    verify_response(context.response, 200)


@then('with a date {days:d} days in the future, the resulting JSON is')
def _then_json_added_with_date_is(context, days):
    observed = context.response.get_json(force=True)
    expected = json.loads(context.text)
    if type(expected) == list:
        assert len(expected) == len(observed)
        for i in range(len(expected)):
            _compare_event_in_days(expected[i], observed[i], days)
    else:
        _compare_event_in_days(expected, observed, days)


@when('I ask for the next event')
def _when_get_next_event(context):
    context.response = context.client.get('/event')
    verify_response(context.response, 200)


@when('I ask for the next event in the city "{city}"')
def _when_get_next_event_in_city(context, city):
    context.response = context.client.get('/event/{}'.format(city))
    verify_response(context.response, 200)


@when('I ask for the next event {dist:d} km closer to {lat:g},{lon:g}')
def step_impl(context, dist, lat, lon):
    request = '/event/{}/{}/{}'.format(lat, lon, dist)
    context.response = context.client.get(request)
    verify_response(context.response, 200)


@when('I configure the event rooms to')
def _when_configure_rooms(context):
    event_date = context.date.strftime("%Y-%m-%d")
    context.request = [{"number": r['number'], "topic": r['topic']}
                       for r in context.table]
    endpoint = "/event/{date}/rooms".format(date=event_date)
    verify_response(post_json_data(context, endpoint), 201)


@then('the answer has {count:d} events due in [{days}] days with')
def _then_there_are_some_events(context, count, days):
    days = [int(d.strip()) for d in days.split(",")]
    observed = context.response.json
    assert len(observed) == count
    for i, expected in enumerate(json.loads(context.text)):
        _compare_event_in_days(expected, observed[i], days[i])


@then('there is an event for "{institution}" that will occur in {days:d} days')
def _then_event_in_institution_in_days(context, institution, days):
    response = context.client.get('/events')
    verify_response(response, 200)
    observed = response.json
    assert len(observed) == 1
    _compare_event_in_days(json.loads(context.text), observed[0], days)
