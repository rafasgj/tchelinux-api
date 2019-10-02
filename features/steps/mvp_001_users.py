"""Steps for MVP-001: Users."""

from behave import given, when, then
import json
from api import connect_db

from features.steps.common import (
    verify_response, add_authentication, user_register, user_login)


@given('no user is registered')
def _given_no_user_exist(context):
    db = connect_db()
    assert db.session.query(db.entity('User')).count() == 0


@given('an unregistered user name "{name}" and email "{email}"')
def _given_name_and_email(context, name, email):
    context.user = {"name": name, "email": email}


@given('the user password "{password}"')
def _given_password(context, password):
    context.password = password


@when('I register with')
def _when_create_user_account(context):
    row = context.table[0]
    context.user = {
        "name": row['name'],
        "email": row['email'],
    }
    context.password = row['password']
    request = '{{"name":"{name}", "email":"{email}", "password":"{password}"}}'
    request = request.format(**context.user, password=context.password)
    data = json.loads(request)
    context.response = context.client.post('/user', data=data,
                                           follow_redirects=True)
    verify_response(context.response, 201)


@given('there are registered users')
def _given_some_registered_users(context):
    request = '{{"name":"{name}", "email":"{email}", "password":"{password}"}}'
    for row in context.table:
        text = request.format(name=row['name'], email=row['email'],
                              password=row['password'])
        user_register(context, **(json.loads(text)))


@when('I login with email "{email}" and password "{password}"')
def _given_or_when_login(context, email, password):
    data = {"email": email, "password": password}
    context.response = context.client.post('/login', data=data,
                                           follow_redirects=True)


@then('an authentication code is generated')
def _given_or_then_authentication_code_is_generated(context):
    assert context.response is not None
    res = json.loads(context.response.data)
    context.authentication = res["access_token"]


@given('the user "{email}" has authenticated in the system')
def _given_user_is_authenticated(context, email):
    user_register(context, email=email, password=1234, role="user")
    res = user_login(context, email, 1234)
    context.authentication = res["access_token"]


@given('the user ends its session')
@when('the user ends its session')
def _given_or_when_end_user_session(context):
    headers = add_authentication(context)
    context.response = context.client.get('/logout', headers=headers)
