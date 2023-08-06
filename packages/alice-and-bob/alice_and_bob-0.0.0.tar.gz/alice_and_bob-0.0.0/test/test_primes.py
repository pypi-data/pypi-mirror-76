from alice_and_bob.primes import Prime

def test_known_prime():
    prime = Prime(3)
    assert isinstance(prime, int)
    assert prime == 3


def test_raises_value_error_when_not_prime():
    try:
        not_prime = Prime(4)
        assert not_prime == 4
    except ValueError:
        pass
    else:
        raise AssertionError('ValueError not raise for non-prime')


def test_large_non_prime():
    try:
        big_even = Prime.primes[-1] + 1
        non_prime = Prime(big_even)
        assert non_prime % 2 == 0
    except ValueError:
        pass
    else:
        raise AssertionError('Expected ValueError to be raised for large even number')


def test_large_prime():
    primes = Prime.primes.copy()  # backup primes data

    Prime.primes = [2, 3, 5]
    prime = Prime(7)
    assert prime == Prime.primes[-1] == 7

    Prime.primes = primes  # restore original data


def test_non_integer():
    try:
        Prime(3.1)
    except TypeError:
        pass
    else:
        raise AssertionError('Expected TypeError to be raised when passing float value')
