import pytest

from trythatagain import retry, CaughtException, retry_exp_backoff
from trythatagain import waiters


def test_exp_backoff(mocker):
    mocker.patch('trythatagain.waiters.time')

    assert waiters.exp_backoff(2, 1) is 4
    waiters.time.sleep.assert_called_with(4)

    mocker.resetall()

    assert waiters.exp_backoff(3, 1) is 9
    waiters.time.sleep.assert_called_with(9)

    mocker.resetall()

    assert waiters.exp_backoff(2, .1) == .4
    waiters.time.sleep.assert_called_with(.4)


def test_linear_backoff(mocker):
    mocker.patch('trythatagain.waiters.time')
    assert waiters.linear_backoff(2, 1) is 3
    waiters.time.sleep.assert_called_with(3)

    mocker.resetall()

    assert waiters.linear_backoff(2, .1) == pytest.approx(.3)
    waiters.time.sleep.assert_called_with(pytest.approx(.3))


def test_retry():
    @retry
    def func():
        return 'foo'

    assert func() == 'foo'

    class TestClass(object):
        @retry
        def foo(self):
            return 'foo'

    c = TestClass()
    assert c.foo() == 'foo'


def test_retry_calling_func_some_errors():
    local = {'calls': 0}

    @retry
    def func():
        local['calls'] += 1
        if local['calls'] > 2:
            return 'foo'
        raise Exception('some problem')

    assert func() == 'foo'


def test_retry_calling_func_error():
    class CustomException(Exception):
        pass

    @retry
    def func():
        raise CustomException('Oops')

    with pytest.raises(CaughtException) as excinfo:
        func()

    assert isinstance(excinfo.value.caught, CustomException)


def test_retry_raise_for():
    @retry(raise_for=ValueError)
    def func():
        raise ValueError

    with pytest.raises(ValueError):
        func()


def test_retry_raise_for_bad_exception():
    @retry(raise_for='')
    def func():
        raise ValueError

    with pytest.raises(TypeError):
        func()


def test_retry_retries_correct_amount():
    local = {'count': 0}

    def waiter(i, unit):
        local['count'] += 1

    @retry(wait_func=waiter)
    def func():
        raise Exception

    with pytest.raises(CaughtException):
        func()

    assert local['count'] is 3


def test_retry_retries_custom_amount():
    local = {'count': 0}

    def waiter(*args):
        local['count'] += 1

    @retry(retries=5, wait_func=waiter)
    def func():
        raise Exception

    with pytest.raises(CaughtException):
        func()

    assert local['count'] is 5


def test_retry_retries_forever():
    local = {'count': 0}

    class StopRetrying(Exception):
        pass

    def waiter(*args):
        local['count'] += 1
        if local['count'] > 10:
            raise StopRetrying()

    @retry(retries=0, wait_func=waiter)
    def func():
        raise Exception

    with pytest.raises(StopRetrying):
        func()

    assert local['count'] is 11


def test_retry_wait_func(mocker):
    mock = mocker.Mock()

    @retry(retries=3, wait_func=mock)
    def func():
        raise ValueError

    with pytest.raises(CaughtException):
        func()

    assert mock.call_count is 3


def test_retry_exp_backoff(mocker):
    mocker.patch('trythatagain.waiters.time')

    @retry_exp_backoff
    def func():
        raise Exception

    with pytest.raises(CaughtException):
        func()

    assert waiters.time.sleep.call_count is 3


def test_retry_linear_backoff(mocker):
    mocker.patch('trythatagain.waiters.time')

    @retry_exp_backoff
    def func():
        raise Exception

    with pytest.raises(CaughtException):
        func()

    assert waiters.time.sleep.call_count is 3
