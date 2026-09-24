import random

# Returns `(g, x, y)` with `g ≥ 0` and `a*x + b*y == g`.
# `g == 0` iff `a == b == 0`; in that case `(x, y)` can be `(0, 0)`.
def egcd(a: int, b: int) -> tuple[int, int, int]:
    # sign function
    def sign(x: int) -> int:
        if x>0:
            return 1
        if x<0:
            return -1
        else: 
            return 0
    
    # case bash
    if a == 0 and b == 0:
        return (0,0,0)
    elif a == 0:
        return(abs(b), 0, sign(b))
    elif b == 0:
        return(abs(a), sign(a), 0)
    elif a > 0 and b > 0:
        q, r = a//b, a%b
        g, x1, y1 = egcd(b, r)
        return(g, y1, x1 - q*y1)
    else:
        g, x1, y1 = egcd(abs(a), abs(b))
        return(g, sign(a)*x1, sign(b)*y1)


# `m > 1`.
# Returns `x` with `0 ≤ x < m` and `a*x ≡ 1 (mod m)` when the inverse exists.
# Returns None when `gcd(a, m) ≠ 1`.
def modinv(a: int, m: int) -> int | None:
    if m <= 1:
        raise ValueError(f"Input m must be greater than 1, you gave {m}")
    else:
        g, x, y = egcd(a,m)
        if g == 1:
            return x%m
        else:
            return None

# `n >= 0`
# Returns largest `s` such that s*s <= n, or equivalently, s^2 <= n < (s+1)^2
def isqrt(n: int) -> int:
    l = 0; r = n+1
    while r-l>1:
        m = (l + r) // 2
        if m*m <= n:
            l = m
        else:
            r = m
    return l

# `n >= 0`
# Returns b if `n = b^2`, otherwise returns None
def is_perfect_square(n: int) -> int | None:
    b = isqrt(n)
    if b*b == n:
        return b
    else:
        return None

# checks if an integer n is a prime
# gives a deterministic algorithm if n <= 40 bits
# otherwise, it only gives a probabilistic one
# rounds >= 1
def is_probable_prime(n: int, rounds: int = 8) -> bool:
    if rounds < 1:
        raise ValueError("rounds must be at least 1")
    if n < 2:
        return False
    if n%2 == 0:
        if n == 2:
            return True
        else:
            return False
    elif n == 1:
        return False
    else:
        n_bits = len(bin(n)) - 2
        d = n-1; s = 0
        while d%2 == 0:
            s += 1
            d = d // 2
        if n_bits <= 40: # deterministic algorithm for 40-bit integers
            bases = [2, 3, 5, 7, 11, 13, 17]
            for a in bases:
                if n == a:
                    return True
            for a in bases:
                if n%a == 0:
                    return False
                else:
                    v = pow(a, d, n)
                    modulos = []
                    for _ in range(s):
                        modulos.append(v)
                        v = v**2 % n
                    if all([modulos[0] != 1]+ [modulos[i] != n-1 for i in range(s)]):
                        return False
            return True
        else:
            count = 0
            coprimes = []
            while count < rounds:
                a = random.randint(2, n-2)
                if egcd(a, n)[0] != 1:
                    return False
                else:
                    if a not in coprimes: 
                        coprimes.append(a)
                        count += 1
            for a in coprimes:
                v = pow(a, d, n)
                modulos = []
                for _ in range(s):
                    modulos.append(v)
                    v = v**2 % n
                if all([modulos[0] != 1]+ [modulos[i] != n-1 for i in range(s)]):
                    return False
            return True

# generate a prime with this many bits
# same as is_probable_prime, deterministic for <= 40 bits and
# probabilistic otherwise
def random_prime(bits: int) -> int:
    assert bits > 0
    if bits == 1:
        return 2
    else:
        low = 2**(bits-2) + 1
        high = 2**(bits-1)
        while True:
            k = random.randint(low, high)
            p = 2*k - 1
            if is_probable_prime(p):
                return p

# `gcd(num, den) = 1` and `den > 0`
# returns the continued-fraction [a0; a1, ..., a_m] of the rational num/den
def continued_fraction(num: int, den: int) -> list[int]:
    if den == 1:
        return [num]
    else:
        return [num // den] + continued_fraction(den, num % den)

# returns the convergents of the rational with continued-fraction a
def convergents(a: list[int]) -> list[tuple[int, int]]:
    if len(a) == 1:
        return [(a[0], 1)]
    elif len(a) == 2:
        return [(a[0], 1), (a[0]*a[1]+1, a[1])]
    else:
        n = len(a)
        res = [(a[0], 1), (a[0]*a[1] + 1, a[1])]
        p_i, q_i = a[0], 1
        p_ii, q_ii = a[0]*a[1] + 1, a[1]
        for k in range(2, n):
            p_iii = a[k]*p_ii + p_i
            q_iii = a[k]*q_ii + q_i
            p_i = p_ii; q_i = q_ii
            p_ii = p_iii; q_ii = q_iii
            res.append((p_ii, q_ii))
        return res

