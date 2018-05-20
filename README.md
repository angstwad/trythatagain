# trythatagain

This provides decorators for super simple function/method call retries when an exception is raised.

## Installation

```bash
pip install trythatagain
```

## Examples

Here's a simple use case: querying the AWS API, knowing you might hit API limits.

```python
from trythatagain import retry

@retry
def find_ebs_volumes(unattached=True, no_snapshots=True):
    ...

try:
    find_ebs_volumes()
except CaughtException as e:
    print('Failed to list EBS volumes')
    print(e.caught_exception)
```

This will retry calling `func` three times.  If was not successful in calling the function without an exception, it will re-raise the exception as `CaughtException`, with the original exception available at the attribute `caught_exception`.

Retry as many times as times as necessary:

```python
from trythatagain import retry

@retry(retries=5)
def try_five_times():
    raise Exception('This always fails')

@retry(retries=0)
def retry_forever():
    raise Exception('Terrible waste of CPU cycles')
```

Raise immediately on specific exceptions:

```python
@retry(raise_for=ValueError)
def update_cache():
    ...
```

Suppress re-raising exceptions:

```python
@retry(reraise=False)
def reload_user_data():
    ...
```

There's also exponential and linear backoff retries things like cooling down after hitting API limits.  In fact, AWS recommends exponential backoff to deal with API limits.

```python
# waits 1 second, then 4, then 9, etc.
@retry_exp_backoff(unit=MILLISECONDS)
def update_instance_tags():
    ...

@retry_linear_backoff(unit=SECONDS)
def scrape_url():
    ...
```

Custom wait functions are also possible:

```python
def fixed(i, unit):
    time.sleep(5 * unit)

@retry(wait_func=fixed, unit=MILLISECONDS)
def func():
    ...
```
