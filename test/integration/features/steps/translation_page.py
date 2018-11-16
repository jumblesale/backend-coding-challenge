from behave import *
from hamcrest import assert_that, equal_to, has_item

from unbabel.config import test_config, create_storage_adapter, dev_config
from unbabel.types import SupportsStoringUids


@given("I have a test application")
def step_impl(context):
    context.app = app = test_config()
    context.client = app.test_client()


@given("I have a dev application")
def step_impl(context):
    context.app = app = dev_config()
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


@given("I have a storage adapter")
def step_impl(context):
    context.app = app = test_config()
    context.storage_adapter = create_storage_adapter(app)


@given('I create a new translation with uid "{uid}"')
def step_impl(context, uid):
    storage_adapter: SupportsStoringUids = context.storage_adapter
    with context.app.app_context():
        storage_adapter.store_uid(uid)


@when("I retrieve all saved translations")
def step_impl(context):
    storage_adapter: SupportsStoringUids = context.storage_adapter
    with context.app.app_context():
        context.uids = storage_adapter.retrieve_all_uids()


@then('I get uid "{uid}"')
def step_impl(context, uid):
    assert_that(context.uids, has_item(uid))


@when("I request a new translation")
def step_impl(context):
    text = 'Sphinx of black quartz, judge my vow'
    context.client.post('/', data={'text': text})


@then("I can see that translation")
def step_impl(context):
    response = context.client.get('/')
    one = 1
