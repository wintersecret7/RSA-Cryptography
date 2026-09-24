from src.attacks.wiener import generate_small_d_lambda_key, wiener_attack
from src.rsa import keygen, encrypt, decrypt
from src.ntt import egcd, modinv, isqrt, is_probable_prime, random_prime
import random

def generate_primes(bits: int):
    p, q = 0, 0
    while q == 0:
        p = random_prime(bits)
        i = 2
        while i <= p-1 and q == 0:
            if is_probable_prime(p+i):
                q = p + i
            i += 2
    return (p, q)

def test_hand_pair():
    assert wiener_attack(200309, 39881) == 5
    assert wiener_attack(195571, 12965) is None # documented miss
    m, e, n, d_phi = 42, 39881, 200309, 5
    c = encrypt(m, n, e)
    assert decrypt(c, n ,d_phi) == m

# the keygen is generated in such a way that d_φ = modinv(e, φ(n)) is within the desired bound
# we generate d_φ first, then calculate the public key e
def test_random_30bit_primes(): 
    found = False
    p, q, n, d, phi = 0, 0, 0, 0, 0
    while not found:
        p, q = generate_primes(30)
        phi = (p-1) * (q-1)
        d = 3
        n = p*q
        upp_bd = isqrt(isqrt(n)) // 3
        while egcd(d, phi)[0] != 1:
            d += 2
        if d < upp_bd:
            found = True
    e = modinv(d, phi)

    ## Wiener's attack, given only n and e
    d_wiener_attack = wiener_attack(n, e)
    assert d_wiener_attack is not None
    for _ in range(20):
        m = random.randrange(0, n)
        c = encrypt(m, n, e)
        assert decrypt(c, n, d_wiener_attack) == m
    print("Wiener's Attack successfully recovered private key that decrypts 20 random messages")

# the keygen is generated such that d_φ is a few times larger than the desired bound
def test_d_phi_large():
    found = False
    p, q, n, lam, d_large, e = 0, 0, 0, 0, 0, 0
    while not found:
        p, q = generate_primes(30)
        n = p*q
        lam = (p-1)*(q-1) // egcd(p-1, q-1)[0]
        upp_bd = isqrt(isqrt(n)) // 3
        d_large = 2*((3 * upp_bd) // 2) + 1
        while egcd(d_large, lam)[0] != 1:
            d_large += 2
        e = generate_small_d_lambda_key(p, q, d_large)
        assert e is not None
        if d_large < 4 * upp_bd and (e*d_large - 1)%((p-1)*(q-1)) == 0:
            found = True
    
    ## Wiener's Attack
    d_wiener_attack = wiener_attack(n, e)
    if d_wiener_attack is None:
        print("Wiener's Attack recovered Nothing")
    else:
        for _ in range(20):
            m = random.randrange(0, n)
            c = encrypt(m, n, e)
            assert decrypt(c, n, d_wiener_attack) == m
        print("Wiener's Attack successfully recovered private key that decrypts 20 random messages")

def test_negative():
    found = False
    e = 65537
    while not found:
        p, q = random_prime(30), random_prime(30)
        lam = (p-1)*(q-1) // egcd(p-1, q-1)[0]
        if p != q and egcd(e, lam)[0] == 1:
            dictt = keygen(p, q, 65537)
            d, n = dictt["d"], dictt["n"]
            if d > 100*isqrt(isqrt(n)) // 3: ## normally, d = modinv(e, λ(n)) is already very large
                found = True
                assert wiener_attack(n, 65537) is None
                print("Wiener's Attack recovered nothing")