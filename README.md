# Unbabel technical assessment

## Running

This solution uses [pipenv](https://pipenv.readthedocs.io/en/latest/).
To start, run `pipenv install`. To get a shell, run `pipenv shell`.
To launch the application on `localhost:8888`, run `python app.py`.

A running postgres instance is required. A postgres container can be brought
up with `docker-compose up` and will run on port `5555` with username and
password set to `docker`. The database used is called `postgres`. Tables
are dropped and created when the app comes up - in production, this would
be handled with migrations.

The app can be run in `test` mode, in which case a stub `Unbabel` adapter
is used and no calls are made to the API. Or a `dev` config can be used
which will use the API's sandbox. Switch between these with the `ENVIRONMENT`
environment variable. `test` is used by default.

In `dev` mode, the app also requires a `USERNAME` and `API_KEY` environment variable,
containing the sandbox username and api key respectively.

Example use (from inside a pipenv shell):

```bash
ENVIRONMENT=dev USERNAME=jumblesale API_KEY=xyz543 python app.py
```

## Testing

Unit tests are available using `pytest`. To run them, run `make test-local`.

This solution uses `mypy` for static type checking. Run mypy with `make mypy`.

Integration use `behave`. Run integration tests with `make test-integration`.

## What could have been done better?

I'm not used to writing so many unit tests - I find that I often get more value
out of integration tests. However I did not have access to the sandbox when
writing this solution so have based it off the documentation and therefore
have thoroughly tested the API adapter in isolation. The level of unit tests
combined with mypy coverage makes me feel reasonably confident in what I've written.

It's been a long time since I've written a service which provides html - I'm much
more used to providing json. I was not sure how to test the `GET` and `POST` endpoints
beyond asserting that I got `200` responses from them.

The html page itself is very ugly. I'm more used to building RESTful APIs which get consumed
by a JavaScript framework but felt this was outside of the scope of the specification.
Hopefully what is there is enough to be functional.

If I had access to the API I would have written integration tests which go from the controller
to the running API.

I could have used the Unbabel Python SDK to make the solution dramatically more simple.
However not having access to the API meant this was not possible. I feel like the adapter
is quite nice so I don't think this has been too bad of a decision.

I like how decoupled everything is. The config serves as a way to wire up a bunch of modules
which have no knowledge of one another. Using `mypy`'s `Protocol`s is a nice way to describe
the interface to the adapter.  It should be easy to switch out the implementation if we ever
needed to.

I've detailed other assumptions I've made as I was going in `ASSUMPTIONS.md`.
