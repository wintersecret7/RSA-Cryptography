import math 
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ntt import egcd, is_probable_prime, isqrt

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, isqrt(n) + 1):
            if n%i == 0:
                return False
        return True

# Choose 1 < a < n, B > 1
def pollard_p1_factorial(n: int, B: int, a: int = 2) -> int:
    g = egcd(a,n)[0]
    if 1 < g < n:
        return g
    else:
        x = a
        for k in range(1, B+1):
            x = pow(x, k, n)
            g = egcd(x-1,n)[0]
            if 1 < g < n:
                return g
            elif g == n:
                raise AssertionError("The gcd equals n; both p-1 and q-1 divide M")
        raise AssertionError("B too small")

# prime power version, choose 1 < a < n, B > 1
def pollard_p1(n: int, B: int, a: int = 2) -> int:
    g = egcd(a,n)[0]
    if 1 < g < n:
        return g
    else:
        x = a
        g = egcd(x-1,n)[0]
        if 1 < g < n:
            return g
        else:
            for p in range(2, B+1):
                if is_prime(p):
                    res = p
                    while res*p <= B:
                        res = res*p
                    x = pow(x, res, n)
                    g = egcd(x-1,n)[0]
                    if 1 < g < n:
                        return g
                    elif g == n:
                        raise AssertionError("The gcd equals n; both p-1 and q-1 divide M")
            raise AssertionError("B too small")

# sample a prime p where p-1 is B-powersmooth
def smooth_prime(bits: int, B: int) -> int:
    prime_powers = []
    for p in range (2, B+1):
        if is_prime(p):
            res = p
            while res*p <= B:
                res = res*p
            prime_powers.append(res)
    product = math.prod(prime_powers)
    high, low = 2**(bits) - 1, 2**(bits - 1) + 1
    assert product + 1 >= low, "B is too small"

    for _ in range(10000):
        sample = 1
        while sample + 1< low:
            k = random.choice(prime_powers)
            if sample % k != 0:
                sample = sample*k
        if sample + 1 <= high and is_probable_prime(sample + 1):
            return sample + 1
    
    raise AssertionError("no prime p of this bit length with p-1 B-powersmooth was found; increase B or decrease bits")