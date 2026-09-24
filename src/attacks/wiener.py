import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ntt import egcd, modinv, is_perfect_square, continued_fraction, convergents

# assumes 1 < e < φ(n)
# returns d_φ = modinv(e, φ(n))
def wiener_attack(n: int, e: int) -> int | None:
    g = egcd(n,e)[0]
    n1 = n // g
    e1 = e // g 
    conv = convergents(continued_fraction(e1, n1))
    # we have e1 < n1 from precondition, so the first pair of conv is (0, 1) - we want to omit it
    for (k, d_i) in conv[1:]:
        if (e*d_i - 1) % k == 0:
            phi = (e*d_i - 1) // k
            prime_sum = n - phi + 1
            if prime_sum > 0:
                v = prime_sum**2 - 4*n
                if v >= 0 and is_perfect_square(v) is not None and prime_sum != n+1:
                    return modinv(e, phi)
    return None

# create a key that matches this lab's rsa system of inverting modulo λ(n), and with small d
def generate_small_d_lambda_key(p: int, q: int, d_lam: int) -> int | None:
    lam = (p-1)*(q-1) // egcd(p-1, q-1)[0]
    if egcd(d_lam, lam)[0] == 1:
        return modinv(d_lam, lam)
    else:
        return None

if __name__ == "__main__":
    print(wiener_attack(200309, 39881))
