import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ntt import egcd, modinv

def lambda_n(p: int, q: int) -> int:
    return (p-1)*(q-1) // egcd(p-1,q-1)[0]

# p and q provided must be primes
def keygen(p: int, q:int, e: int | None = None) -> dict:
    assert p != q, "p must not equal to q"
    n = p*q; assert n%2 == 1, "both p and q must be odd"
    l = lambda_n(p, q)
    if e is None:
        e_rep = 3
        while egcd(e_rep, l)[0] != 1: # search a replacement of e from 3,5,7,...
            e_rep += 2
        d = modinv(e_rep, l)
        return {
            "n": n,
            "e": e_rep,
            "d": d,
            "p": p,
            "q": q,
            "lam": l
        }
    else: 
        assert egcd(e, l)[0] == 1, "e must be coprime to lambda_n"
        d = modinv(e, l)
        return {
            "n": n,
            "e": e,
            "d": d,
            "p": p,
            "q": q,
            "lam": l
        }
    
def encrypt(m: int, n: int, e: int) -> int:
    assert (0 <= m and m < n)
    return pow(m, e, n)

def decrypt(c: int, n: int, d: int) -> int:
    assert (0 <= c and c < n)
    return pow(c, d, n)

def decrypt_crt(c: int, p: int, q: int, d: int) -> int:
    assert p != q
    assert (0 <= c and c < p*q)
    a = pow(c%p, d % (p-1), p)
    b = pow(c%q, d % (q-1), q)
    t = (modinv(p, q)*(b-a)) % q
    return (p*t + a) % (p*q)

if __name__ == "__main__":
    pass