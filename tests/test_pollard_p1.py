import pytest
import random
from src.attacks.pollard_p1 import pollard_p1, pollard_p1_factorial, smooth_prime
from src.ntt import random_prime

def test_manual():
    assert pollard_p1_factorial(59713, 7, 2) == 211
    assert pollard_p1(59713, 7, 2) == 211

def test_error():
    with pytest.raises(AssertionError):
        pollard_p1_factorial(59713, 6, 2)

    with pytest.raises(AssertionError):
        pollard_p1(59713, 6, 2)

def test_20bit_primes():
    random.seed(42)
    for j in range(10):
        B = random.randint(25,40)
        p = smooth_prime(20, B)
        q = random_prime(20)
        while q == p:
            q = random_prime(20)
        n = p*q
        factor_1 = pollard_p1_factorial(n, B, 2)
        factor_2 = pollard_p1(n, B, 2)

        assert factor_1 in (p, q)
        assert factor_2 in (p, q)
        assert n % factor_1 == 0
        assert n % factor_2 == 0
        
        if j == 0:
            print("\n")
            print(f"One generated instance is n = {n} = {p} * {q} = p * q.")
            print(f"Pollard's factorial version successfully recovered {factor_1}")
            print(f"Pollard's prime power version successfully recovered {factor_2}")
    

def test_negative():
    random.seed(0)
    for _ in range(10):
        p, q = random_prime(20), random_prime(20)
        B = random.randint(25,40)
        while p == q:
            q = random_prime(20)
        n = p*q
        with pytest.raises(AssertionError):
            pollard_p1_factorial(n, B, 2)
        with pytest.raises(AssertionError):
            pollard_p1(n, B, 2)

