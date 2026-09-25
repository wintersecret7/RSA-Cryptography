# The RSA Cryptosystem and some of its weaknesses

The public key of textbook RSA is a pair `(n, e)`, where `n = pq` is a product of two distinct odd primes. Encryption of a message `m` is `c ≡ m^e (mod n)`. The private exponent `d` is generated in one of two ways: `d_λ ≡ e^{-1} (mod λ(n))`, or `d_φ ≡ e^{-1} (mod φ(n))`, where `λ` is the Carmichael function and `φ` is Euler's totient. Recovering `d` requires `λ(n)` or `φ(n)`, and computing either from `n` alone is equivalent to factoring `n`. That equivalence is what makes the cryptosystem strong. However, such a strong system still has its weaknesses. We will discuss three such vulnerabilities, and the attack that follows from each.


| Weakness          | Attack                        |
| ----------------- | ----------------------------- |
| `p ≈ q`           | Fermat factorization          |
| small `d_φ`       | Wiener's attack               |
| powersmooth `p−1` | Pollard's `p−1` factorization |




## Fermat factorization

This method factors `n = pq` when the odd primes `p < q` are close. There are only two representations of `n` as a difference of squares of positive integers; the useful one is `((p + q)/2)^2 − ((q − p)/2)^2`. Recovering `p` and `q` takes `O((q − p)^2 / √n)` integer-square-root tests, which is small when `p` and `q` are close. When `p` and `q` are far apart, as in a modern RSA modulus, that count is too large and the method is inefficient.

## Wiener's attack

Wiener's attack recovers `d_φ`, the inverse of `e` modulo `φ(n)`. That exponent is the unique positive solution of `e d_φ − k φ(n) = 1` with `0 < k < d_φ`. Since `φ(n) ≈ n`, one has `e/n ≈ k/d_φ`. If `p < q < 2p` and `d_φ < n^{1/4}/3`, then `|e/n − k/d_φ| < 1/(2 d_φ^2)`. Legendre's theorem says that `k/d_φ`, which is in lowest terms, is then a continued-fraction convergent of `e/n`, so the candidates for `k/d_φ` are among those convergents. The bound does not hold for a typical modern key, where `e` is small and `d_φ` is large.

## Pollard's `p−1` method

For a fixed base `a` with `1 < a < n` and `gcd(a, n) = 1`, the algorithm looks for an exponent `M` such that exactly one of `p` and `q` divides `a^M − 1`. Then `gcd(a^M − 1, n)` is a proper factor of `n`. By Fermat's Little Theorem, `p−1 | M` implies `p | (a^M − 1)`. Choose `B` so that `p−1` is `B`-powersmooth and `q−1` is not. Then both `M = B!` and `M = lcm(1, 2, …, B)` are multiples of `p−1`. For `M = lcm(1, 2, …, B)` one also has `q−1 ∤ M`; the same need not hold for `M = B!`. The remaining bet is `ord_q(a) ∤ M`. The method is weak on safeprimes, primes of the form `2r + 1` with `r` prime. If `p < q` are both safeprimes, the least `B` for which `p−1` or `q−1` is `B`-powersmooth is `(p−1)/2`. If `p ≈ q`, then `B` is `O(√n)`. Pollard's running time is `O(B)`, so in that case the attack is no better than trial division.

For more details on each of these attacks, read [`Fermat`](notes/02-fermat.md), [`Wiener`](notes/03-wiener.md), and [`Pollard`](notes/04-pollard-p1.md).

# How to Run

Copying the repository

```
git clone https://github.com/wintersecret7/RSA-Cryptography.git
cd RSA-Cryptography
```

From the repository root, create and activate a virtual environment, then install pytest:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pytest
```

Run the complete test suite with:

```
python -m pytest -sv
```

The test modules also provide three reproducible attack demonstrations. Each demonstration generates its weak key or modulus in the repository; no external key or ciphertext is required.

```
# Fermat factorization: primes generated close together
python -m pytest tests/test_fermat.py -sv

# Wiener's attack: keys generated with a deliberately small private exponent
python -m pytest tests/test_wiener.py -sv

# Pollard's p−1: one prime generated with a smooth p−1
python -m pytest tests/test_pollard_p1.py -sv
```

Individual test functions can be run with pytest's `::` selector. Replace `function_name` with the name of the test function you want to run:

```
python -m pytest tests/test_fermat.py::function_name -sv
```

For example:

```
python -m pytest tests/test_fermat.py::test_handkey -sv
```

The successful tests verify that the attacks recover a factor or private exponent and that the recovered key decrypts RSA ciphertext correctly. The negative tests also show cases where the relevant weakness is absent or the smoothness bound is too small.

## Honest limitations

This repository uses educational RSA keys generated specifically to satisfy the weakness required by each attack. The experiments demonstrate key recovery for those weak keys; they do not break properly generated modern RSA, and they do not claim to break RSA in general. The code is intended for mathematical study and testing only. It should not be used against live systems, real certificates, or someone else's ciphertext. The Python implementations are also not constant-time cryptographic software and are not suitable for protecting real secrets.

## Function reference

The functions below use integer inputs and implement the arithmetic, RSA operations, key generation, and attacks used in this lab.

### `src/ntt.py`

- `egcd(a, b)` takes two integers and returns `(g, x, y)` satisfying `a*x + b*y = g`, where `g = gcd(a, b)`.
- `modinv(a, m)` takes an integer and a modulus and returns the multiplicative inverse of `a` modulo `m`, or `None` when the inverse does not exist.
- `isqrt(n)` takes a non-negative integer and returns its integer square root.
- `is_perfect_square(n)` takes a non-negative integer and returns its square root when `n` is a perfect square, otherwise `None`.
- `is_probable_prime(n, rounds=8)` tests whether an integer is prime. It is deterministic for inputs up to 40 bits and probabilistic for larger inputs.
- `random_prime(bits)` generates a probable prime with the requested bit length.
- `continued_fraction(num, den)` takes a reduced rational number and returns its continued-fraction coefficients.
- `convergents(a)` takes continued-fraction coefficients and returns the corresponding numerator-denominator convergents.

### `src/rsa.py`

- `lambda_n(p, q)` takes two distinct odd primes and returns Carmichael's function `λ(pq)`.
- `keygen(p, q, e=None)` takes two distinct odd primes and optionally a public exponent. It returns an RSA key dictionary containing `n`, `e`, `d`, `p`, `q`, and `λ(n)`.
- `encrypt(m, n, e)` takes a message representative `m`, a modulus `n`, and a public exponent `e`, and returns the ciphertext `m^e mod n`.
- `decrypt(c, n, d)` takes a ciphertext, modulus, and private exponent and returns the decrypted message representative.
- `decrypt_crt(c, p, q, d)` decrypts a ciphertext using the Chinese Remainder Theorem and the two prime factors.

### `src/attacks/fermat.py`

- `fermat_factor(n, max_steps=None)` takes an odd composite RSA modulus and searches for a representation of `n` as a difference of squares. It returns `(p, q)` when successful, or `None` when a bounded search reaches `max_steps` without finding factors.
- `recover_rsa_from_factors(p, q, e)` takes the two recovered factors and a public exponent and returns the private exponent by inverting `e` modulo `λ(pq)`.

### `src/attacks/wiener.py`

- `wiener_attack(n, e)` takes a public RSA modulus and exponent and searches the continued-fraction convergents of `e/n` for a small private exponent. It returns the recovered `d_φ`, or `None` when the key is outside the attack's conditions.
- `generate_small_d_lambda_key(p, q, d)` takes two primes and a chosen small private exponent. It returns a compatible public exponent, or `None` when `d` is not invertible modulo `λ(pq)`.

### `src/attacks/pollard_p1.py`

- `is_prime(n)` tests primality by trial division and is used for the small prime bounds in the Pollard implementation.
- `pollard_p1_factorial(n, B, a=2)` takes an RSA modulus, a smoothness bound, and an optional base, then searches using factorial-style exponentiation for a non-trivial factor.
- `pollard_p1(n, B, a=2)` takes the same inputs and uses prime-power exponents up to `B` to search for a non-trivial factor.
- `smooth_prime(bits, B)` generates a probable prime of the requested size whose `p−1` is `B`-powersmooth, for use in Pollard demonstrations.

