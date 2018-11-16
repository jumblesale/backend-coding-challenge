## Assumptions

* I'm developing this without access to the unbabel API sandbox, so using the
  [Python SDK](https://github.com/Unbabel/unbabel-py) has not been an option.
* I made the assumption that the `translate` endpoint would return immediately. This
  was incorrect. The specification asks for a page which loads in < 1 second, which
  this solution does not achieve. If I had realised that the http call was long-running,
  I would have made sure to account for this from the beginning and made the call asynchronous.
  Unfortunately at this point, this would require rewriting most of the application to
  account for this. I would be very happy to discuss what an alternative solution would look
  like.
* The [docs](https://developers.unbabel.com/docs/) don't seem to list models for the return
  types which means my status map may not be exhaustive - I might have missed these listed somewhere?
  I've used an unknown status as the default.
* The get all endpoint paginates with 20 items per page, which I assume will be enough.
  If not, it would be easy to extend the solution to get all results across all pages.
* From the spec: `The list should be dynamically ordered by the size of the translated messages`. I've
  assumed this is longest to shortest.
* Performance is not the most important thing. It would be easy to parallelise the calls to the single
  get endpoint, but this would make the code more complex than the serial solution.
* We don't need migrations, and for testing, dropping and recreating the database
  is good enough for now.
