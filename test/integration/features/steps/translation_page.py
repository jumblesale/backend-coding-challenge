from behave import *
from hamcrest import assert_that, equal_to

from unbabel.config import test_config


@given("I have a test application")
def step_impl(context):
    context.app = app = test_config()
    context.client = app.test_client()


@when('I visit "{path}"')
def step_impl(context, path: str):
    context.response = context.client.get(path)


@then('I get http status "{status}"')
def step_impl(context, status):
    response = context.response
    assert_that(response.status_code, equal_to(int(status)))


@step('I have data with "{key}" set to "{value}"')
def step_impl(context, key, value):
    if not hasattr(context, 'data'):
        context.data = {}
    context.data[key] = value


@when('I "post" that data to "{path}"')
def step_impl(context, path):
    context.response = context.client.post(path, data=context.data)
