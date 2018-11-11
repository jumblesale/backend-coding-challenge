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
