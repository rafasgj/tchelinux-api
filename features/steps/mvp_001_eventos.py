"""Steps for MVP 001: Eventos."""

from behave import given, when, then
import json
from features.steps.common import verify_response, post_json_data
from datetime import datetime, timedelta


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
    context.response = post_json_data(context, '/event', request)
    verify_response(context.response, 201)


@given('there is an event for "{institution}", {days:d} days from now')
def _given_an_event(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() + timedelta(days=days)
    context.request = request.format(institution=institution, date=date)
    verify_response(post_json_data(context, '/event'), 201)


@given(u'there is an event that occurred {days:d} days ago in "{institution}"')
def _given_an_event_that_occured(context, institution, days):
    request = """{{"institution": "{institution}", "date": "{date}"}}"""
    date = datetime.today() - timedelta(days=days)
    context.request = request.format(institution=institution, date=date)
    verify_response(post_json_data(context, '/event'), 201)


@when('I ask for future events')
def _when_retrieving_events(context):
    context.response = context.client.get('/events')
    verify_response(context.response, 200)


@then('with a date {days:d} days in the future, the resulting JSON is')
def _then_json_added_with_date_is(context, days):
    observed = context.response.get_json(force=True)
    date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")
    print("CONTEXT", context.text)
    expected = json.loads(context.text)
    if type(expected) == list:
        expected[0]['date'] = date
    else:
        expected['date'] = date
    # print("EXPECTED", expected)
    # print("OBSERVED", observed)
    assert expected == observed


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


@then('the answer has {count:d} events due in [{days}] days with')
def _then_there_are_some_events(context, count, days):
    days = [int(d.strip()) for d in days.split(",")]
    observed = context.response.json
    assert len(observed) == count
    for i, expected in enumerate(json.loads(context.text)):
        date = datetime.today() + timedelta(days=days[i])
        expected['date'] = date.strftime("%Y-%m-%d")
        print("EXPECTED", expected)
        print("OBSERVED", observed[i])
        assert expected == observed[i]
