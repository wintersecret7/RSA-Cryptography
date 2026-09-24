import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ntt import egcd, modinv, isqrt, is_perfect_square

# - `n` odd, composite of the form `pq` where p,q are odd primes.
# - Returns `(p, q)` with `p ≤ q` and `p*q == n`.
def fermat_factor(n: int, max_steps: int | None = None) -> tuple[int, int] | None:
    if max_steps is None:
        a0 = isqrt(n); a = 0 
        if a0**2 == n: # initialize a = ceil(√n)
            a = a0
        else:
            a = a0 + 1
        while is_perfect_square(a**2 - n) is None:
            a += 1
        b = isqrt(a**2 - n)
        return (a-b, a+b)
    else:
        count = 0 
        a0 = isqrt(n); a = 0 
        if a0**2 == n: # initialize a = ceil(√n)
            a = a0
        else:
            a = a0 + 1
        while is_perfect_square(a**2 - n) is None and count < max_steps:
            a += 1
            count += 1
        b = is_perfect_square(a**2 - n)
        if b is None:
            return None
        else:
            return (a-b, a+b)

# Returns `d` by inverting `e` modulo `λ(pq)`
def recover_rsa_from_factors(p: int, q: int, e: int) -> int | None:
    g = egcd(p-1, q-1)[0]
    lam = (p-1)*(q-1) // g
    return modinv(e, lam)

