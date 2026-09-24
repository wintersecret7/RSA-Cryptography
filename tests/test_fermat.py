import random
from src.ntt import is_probable_prime, random_prime
from src.attacks.fermat import fermat_factor, recover_rsa_from_factors
from src.rsa import keygen, encrypt, decrypt

# For 40 bit primes, the number of iterations ≈ (q − p)^2 / (8√n) <<< (q - p)^2 / (8 * 10^12)
# So, choosing the gap of 2 * 10^8 gives just below 5000 iterations for 40 bit integers.
# With a similar reasoning, we choose the gap of 2 * 10^14 for 80 bit integers.
def generate_keys(bits: int) -> tuple[int, int]:
    if bits == 40:
        p, q = 0, 0
        gap = 2*(10**8)
        while q == 0:
            p = random_prime(40)
            i = 2
            while i <= gap and q == 0:
                if is_probable_prime(p+i):
                    q = p + i
                i += 2
        return(p, q)
    if bits == 80:
        p, q = 0, 0
        gap = 2*(10**14)
        while q == 0:
            p = random_prime(80)
            i = 2
            while i <= gap and q == 0:
                if is_probable_prime(p+i):
                    q = p + i
                i += 2
        return(p, q)

def test_handkey():
    assert(fermat_factor(1022117, 20) == (1009, 1013))

def test_40bit():
    for _ in range(10):
        p_40, q_40 = generate_keys(40)
        dictt = keygen(p_40, q_40)
        n, e, d = dictt["n"], dictt["e"], dictt["d"]
        assert(fermat_factor(n, 5000) == (p_40, q_40))
        assert(recover_rsa_from_factors(p_40, q_40, e) == d)
        m = random.randint(0, n-1)
        c = encrypt(m, n, e)
        assert(decrypt(c, n, d) == m)

def test_80bit():
    for _ in range(10):
        p_80, q_80 = generate_keys(80)
        dictt = keygen(p_80, q_80)
        n, e, d = dictt["n"], dictt["e"], dictt["d"]
        assert(fermat_factor(n, 5000) == (p_80, q_80))
        assert(recover_rsa_from_factors(p_80, q_80, e) == d)
        m = random.randint(0, n-1)
        c = encrypt(m, n, e)
        assert(decrypt(c, n, d) == m)

def test_40bit_huge_gaps():
    for _ in range(10):
        p, q = 0, 0
        while p == 0:
            p = random_prime(40); q = random_prime(40)
            if abs(p-q) < 10**9:
                p = 0
                q = 0
        n = p*q
        assert(fermat_factor(n, 5000) is None)