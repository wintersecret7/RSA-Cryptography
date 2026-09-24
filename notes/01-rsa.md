# The RSA Cryptosystem

## 1. The extended Euclidean algorithm - implementing `egcd`

**Statement.**

```
Given a, b ∈ ℤ, the algorithm returns a triple (g, x, y)
such that g = gcd(|a|, |b|) and a x + b y = g.
```

### The algorithm

If `a = b = 0`, return `(0, 0, 0)`. If one of `a` and `b` is `0` and the other is not, say `a = 0`, then it trivially returns the triple `(|b|, 0, sign(b))`. Similarly, if `b = 0`, it returns `(|a|, sign(a), 0)`.

Now, if `a` and `b` are non-zero, then we just have to solve the case when `a` and `b` are both positive, as the other cases have the same gcd, just different signs of `x` and `y`. Run the algorithm on `|a|`, `|b|` to get `(g, x', y')`, then set

```
x = sign(a) · x'
y = sign(b) · y'
a x + b y = |a| x' + |b| y' = g
```

as desired. For `a, b > 0`, consider the Euclidean division

```
a = q b + r
q = floor(a/b)
r = a mod b
```

Suppose `(g, x1, y1) = egcd(b, r)`. Then we just have to return

```
(g, y1, x1 - q y1)
```

**Invariant.**

```
Every remainder produced is an integer linear combination of the original a and b.
```



### Proof of correctness

The zero cases are trivial to show, as well as the cases where `a` or `b` is negative. So we only prove the result when `a` and `b` are both positive.

The case when `a < b` will just have the recursive call `egcd(b, a)`. So we only need to deal with the case `a ≥ b`. Induct on `b`; it is trivial for `b = 0`. Now assume the result holds for `0 ≤ b ≤ k` for some non-negative integer `k`. Now, for `b = k+1`, we only need to prove for arbitrary `a ≥ k+1`, consider the Euclidean division

```
a = q (k+1) + r
0 ≤ r < k+1
egcd(k+1, r) = (g, x1, y1)
```

where `g = gcd(k+1, r)` and

```
(k+1) x1 + r y1 = g
```

Now, as `g` divides both `k+1` and `r`, it also divides `a`, meaning that `g` divides `gcd(a, k+1)`. Also, as `r = a - q (k+1)`, this means `gcd(a, k+1)` also divides `r`, meaning that `gcd(a, k+1)` divides `g`. Hence

```
gcd(a, k+1) = g
```

The same identity is the invariant at this step: `r = a - q (k+1)` is already a combination of `a` and `k+1`, and `g = (k+1) x1 + r y1` is a combination of `k+1` and `r`, hence of `a` and `k+1`. Substituting `r = a - q (k+1)` into `(k+1) x1 + r y1 = g` makes the coefficients explicit:

```
a y1 + (k+1) (x1 - q y1) = g
```

giving the desired triple `(g, y1, x1 - q y1)`.

### Example `egcd(240, 46)`

```
240 = 5*46 + 10
46  = 4*10 + 6
10  = 1*6  + 4
6   = 1*4  + 2
4   = 2*2  + 0
```

so `gcd(240, 46) = 2`. Back-substitution:

```
2 = 6 - 1*4
  = 2*6 - 10
  = 2*46 - 9*10
  = 47*46 - 9*240
```

hence

```
240*(-9) + 46*47 = 2
egcd(240, 46) = (2, -9, 47)
```



## 2. Inverse - implementing `modinv`

**Statement.**

```
Let m > 1. If gcd(a, m) = 1, then a has an inverse modulo m.
Conversely, if an inverse exists, then gcd(a, m) = 1.
```



### Proof

On one hand, if `gcd(a, m) = 1` then by `egcd` above one can find `x` and `y` such that

```
a x + m y = 1
a x ≡ 1 (mod m)
```

giving the desired inverse for `a`. (If needed, replace `x` by its residue in `{0, …, m-1}`.)

On the other hand, if an inverse for `a` exists, say `x`, then

```
a x ≡ 1 (mod m)
m | (a x - 1)
```

Now, for any common divisor `d` of `a` and `m`, `d` divides `a x` and `a x - 1`, so `d | 1` and hence `d = ±1`. Therefore `gcd(a, m) = 1`.

### Failure policy

```
If the inverse does not exist, modinv returns None.
```



### Example `modinv(17, 3120)`

We first run `egcd`:

```
3120 = 183*17 + 9
17   = 1*9    + 8
9    = 1*8    + 1
8    = 8*1    + 0
```

so `gcd(3120, 17) = 1`. Back-substitution:

```
1 = 9 - 1*8
  = 2*9 - 17
  = 2*3120 - 367*17
```

meaning the inverse is

```
-367 ≡ 2753 (mod 3120)
```

In the following parts, we show how RSA encryption works.

## 3. The Carmichael function

**Definition.**

```
Let n be a positive integer. The Carmichael function λ(n) is the
smallest positive integer k such that a^k ≡ 1 (mod n) for every
integer a coprime to n. Equivalently, it is the exponent of the
finite group G = (ℤ/nℤ)× (units modulo n).
```



## 4. Carmichael `λ(n)` for `n = pq`

**Statement.**

```
Let p, q be distinct primes and n = pq.
Then λ(n) = lcm(p-1, q-1). 
```



### Proof

For coprime positive integers `a, m`, define `ord_m(a)` as the smallest positive integer `k` such that `a^k ≡ 1 (mod m)`.

If `r1` is a primitive root of `p`, then so is `r1 + p k` for any integer `k`. Hence we may choose a primitive root `r` of `p` that is coprime to `q` (so `gcd(r, n) = 1`). Carmichael gives `r^{λ(n)} ≡ 1 (mod n)`, hence `r^{λ(n)} ≡ 1 (mod p)`. Therefore `ord_p(r) = p-1` divides `λ(n)` by the order-divisibility lemma. Similarly `q-1` divides `λ(n)`, so

```
lcm(p-1, q-1) | λ(n)
```

Now, for all `a` coprime to `pq`, Fermat’s Little Theorem and `p-1 | lcm(p-1, q-1)` give `a^{lcm(p-1, q-1)} ≡ 1 (mod p)`, and likewise modulo `q`. As `p` and `q` are distinct primes,

```
a^{lcm(p-1, q-1)} ≡ 1 (mod n)
```

So `lcm(p-1, q-1)` is a universal exponent, hence `λ(n) ≤ lcm(p-1, q-1)`. Combined with `lcm(p-1, q-1) | λ(n)`, we get

```
λ(n) = lcm(p-1, q-1)
```

For `n = pq`, `φ(n) = (p-1)(q-1)`. For any positive integers `a, b` one has `lcm(a, b) · gcd(a, b) = a b`, so

```
λ(n) | φ(n)
λ(n) = φ(n)  iff  gcd(p-1, q-1) = 1
```



## 5. RSA identity: `m^{ed} ≡ m (mod n)`

**Statement.**

```
Let p, q be distinct primes, n = pq, and let 1 < e < λ(n) be coprime to λ(n).
Let d satisfy ed ≡ 1 (mod λ(n)).
Then m^{ed} ≡ m (mod n) for every integer m.
(In the cryptosystem one restricts to 0 ≤ m < n.)
```



### Proof

Write

```
ed = 1 + t λ(n)
```

for some integer `t ≥ 0`.

**Case 1.** `gcd(m, n) = 1`. Carmichael gives `m^{λ(n)} ≡ 1 (mod n)`. Since `λ(n) | (ed - 1)`, we get

```
m^{ed-1} ≡ 1 (mod n)
m^{ed}   ≡ m (mod n)
```

**Case 2.** `gcd(m, n) ≠ 1`. Then `p | m` or `q | m`.

If both divide `m`, then `n | m`, so `m ≡ 0 (mod n)`. For `ed ≥ 1` we have `m^{ed} ≡ 0 ≡ m (mod n)`.

Now, without loss of generality, suppose `p | m` but `q` does not divide `m`. Consider `m + q`:

```
gcd(m + q, q) = gcd(m, q) = 1
gcd(m + q, p) = gcd(q, p) = 1
gcd(m + q, n) = 1
```

Carmichael gives `(m + q)^{λ(n)} ≡ 1 (mod n)`, hence also modulo `q`. But `m + q ≡ m (mod q)`, so `m^{λ(n)} ≡ 1 (mod q)`. As `λ(n) | (ed - 1)`, we get `m^{ed-1} ≡ 1 (mod q)`, i.e. `q | (m^{ed-1} - 1)`. Also `p | m`, so `p | (m^{ed} - m)`. Therefore `p` and `q` both divide `m^{ed} - m = m(m^{ed-1} - 1)`, hence

```
n | (m^{ed} - m)
m^{ed} ≡ m (mod n)
```

**If one inverts** `e` **only modulo** `φ(n)`**.** Suppose instead `ed ≡ 1 (mod φ(n))`. Then `φ(n) | (ed - 1)`, so the same proof applies. Equivalently, one may rerun the argument with `φ(n)` in place of `λ(n)`: Case 1 is Euler; Case 2 uses `q-1 | φ(n)` and Fermat. So a `φ(n)`-inverse always decrypts correctly; it may be a strictly larger exponent than the `λ(n)`-inverse.

## 6. Encryption and decryption

Pick a public exponent `e` with `gcd(e, λ(n)) = 1`, and let `d ≡ e^{-1} (mod λ(n))`. Encryption is `c ≡ m^e (mod n)` with `0 ≤ m < n`. Decryption is `c^d (mod n)`. By §5,

```
c^d ≡ m^{ed} ≡ m (mod n)
```

so one recovers the original **message** `m`.

## 7. Why invert modulo `λ(n)` rather than `φ(n)`?

Textbooks invert modulo `φ(n)` because Euler’s theorem is the first tool students have: if `gcd(m, n) = 1` then `m^{φ(n)} ≡ 1 (mod n)`, so any `d` with `ed ≡ 1 (mod φ(n))` decrypts the coprime case, and CRT/Fermat handles the rest. You never need to name Carmichael.

That `d` is *an* inverse of `e` modulo a multiple of the group exponent, not necessarily the exponent itself. The group `(ℤ/nℤ)×` has order `φ(n)` and exponent `λ(n)`: `λ(n)` is the smallest positive integer `k` with `a^k ≡ 1 (mod n)` for every unit `a`. For `n = pq` we have

```
λ(n) = lcm(p-1, q-1)
λ(n) | φ(n)
λ(n) < φ(n)  unless  gcd(p-1, q-1) = 1
```

Inverting modulo `λ(n)` is the decryption exponent that matches that group law. A `φ(n)`-inverse still decrypts (§5), but it may be larger than the `λ(n)`-inverse. This lab inverts modulo `λ(n)`.

Mixing the two in a later attack is the actual failure mode:

```
If keygen used φ and an attack assumes ed − k λ(n) = 1:
  you are safe on the identity, because φ(n) | (ed − 1)
  implies λ(n) | (ed − 1).
  The d stored in the key may still differ from the λ-reduced
  inverse the attack returns.

If keygen used λ (this lab) and an attack assumes ed − k φ(n) = 1:
  that Diophantine equation can be false.
  You only know λ(n) | (ed − 1), not φ(n) | (ed − 1).
  Wiener’s attack (Session 3) is built on the φ form;
  keys from this lab need that mismatch recorded.
```



## 8. Example Hand keygen

Take `p = 23` and `q = 31`.

1. `n = pq = 713`, `φ(n) = (p-1)(q-1) = 22 · 30 = 660`, `λ(n) = lcm(22, 30) = 330`.
2. Public exponent `e = 101`, with `1 < e < λ(n)` and `gcd(101, 330) = 1`.
3. Private exponent `d ≡ e^{-1} (mod λ(n))`. Running `egcd(101, 330)` gives `(1, -49, 15)`, i.e.

```
101 · (-49) + 330 · 15 = 1
101 · (-49) ≡ 1 (mod 330)
d = -49 + 330 = 281
```

1. Encrypt `m = 20`: `c ≡ m^e ≡ 20^{101} ≡ 658 (mod n)`.
2. Decrypt: `c^d ≡ 658^{281} ≡ 20 (mod n)`, which indeed equals `m`.

**CRT decrypt.** Reduce the exponent modulo `p-1` and `q-1`:

```
658^{281} ≡ 14^{17} ≡ 20  (mod 23)
658^{281} ≡ 7^{11}  ≡ 20  (mod 31)
```

Let `x = 658^{281}`. Then

```
x = 23k + 20
23k + 20 ≡ 20 (mod 31)
23k ≡ 0 (mod 31)
```

As `gcd(23, 31) = 1`, `k ≡ 0 (mod 31)`. Hence `k = 31t` and

```
x = 23 · 31t + 20 = 713t + 20
x ≡ 20 (mod 713)
```

matching ordinary decrypt.

# 9. Miller–Rabin, determining compositeness

`is_probable_prime` and `random_prime` need a primality test.

## Why Fermat is a bad primality test

Fermat’s little theorem: if `p` is prime and `p` does not divide `a`, then

```
a^{p-1} ≡ 1 (mod p)
```

This can be used to test the primality of a number `n`: pick a random `a` in interval `[2, n-2]` and calculate `gcd(a, n)`. If this doesn't equal 1, then `n` is certainly composite. Otherwise, compute `a^{n-1} (mod n)`, if this doesn't equal 1, then `n` is composite and we say `a` is a *Fermat witness* for the compositeness of `n`.

The congruence `a^{p-1} ≡ 1 (mod p)` rarely holds for composite values of `p`. Therefore, if the congruence holds for multiple `a`, then we say `p` is probably prime. However, note that there exists infinitely many **Carmichael Numbers**; numbers `n` such that

```
a^{n-1} ≡ 1 (mod n)  for all a coprime to n
```

Hence, it's certainly possible that we find multiple prime witnesses for a composite number `n`, any such `a` for which `a^{n-1} ≡ 1 (mod n)` is called a *Fermat Liar*. Because of this, we will use Miller-Rabin as our primality test.

## Miller-Rabin

Miller–Rabin uses a stronger fact about square roots of `1` modulo a prime. If `p` is an odd prime and `x^2 ≡ 1 (mod p)`, then `p | (x−1)(x+1)`, so

```
x ≡ ±1 (mod p)
```

There is no nontrivial square root of `1` modulo a prime.

## The test

Let `n > 2` be odd. Write `n − 1 = 2^s · d` with `d` odd and `s ≥ 1`. Fix a base `a` with `1 < a < n`. If `gcd(a, n) > 1`, then `n` is composite (and you have a factor). Otherwise compute the sequence

```
a^d,  a^{2d},  a^{4d},  …,  a^{2^{s-1} d}   (mod n)
```

If `n` is prime, then `a^{n-1} ≡ 1 (mod n)`, so some term is `1`, and the first `1` must be preceded by `−1` (or the sequence starts at `1`). Equivalently, a prime `n` always satisfies **one** of:

```
a^d ≡ 1 (mod n)
or
a^{2^r d} ≡ −1 (mod n)  for some r with 0 ≤ r ≤ s−1
```

If **neither** holds, `n` is definitely composite (`a` is a Miller–Rabin witness). If the condition holds, `n` is only a *probable* prime for that base: a composite can still lie (a strong liar).

## Accuracy

The error of primality test is measured by the probability that a composite number is declared probably prime. It can be shown that if `n` is composite, then at most `1/4` bases `a` are strong liars for `n`. Therefore, running `k` iterations of the Miller-Rabin test ensures that the error is at most

```
4^{-k}
```



## Witnesses for this lab

This lab samples 40-bit and 80-bit primes. If we take `rounds = 8` random bases in `{2, …, n−2}`, the error is at most

```
4^{-8} = 2^{-16}
```

which is enough for educational keys (we are not claiming a proof of primality).

A deterministic alternative for `n < 341,550,071,728,321` (48 bits) is the fixed set `{2, 3, 5, 7, 11, 13, 17}` (Jaeschke). That set is **not** known to decide all 80-bit integers, so for `random_prime(80)` we keep random rounds.

## `is_probable_prime(n, rounds)`

Given a positive integer `n`, checks if `n` is prime. If `n` has at most 40 bits, then run **Miller-Rabin** test with bases `{2, 3, 5, 7, 11, 13, 17}`. This will determine, with no error, whether `n` is prime. Otherwise, if `n` has more than 40 bits, run **Miller-Rabin** a certain times (`rounds`) with random coprime bases. This will give an error of at most `4^{-rounds}`.

## `random_prime(bits)`

Draw a random odd integer in `{2^{bits-1}, …, 2^{bits} − 1}` and accept the first one that passes `is_probable_prime`. That is how the Fermat weak-key generator gets a random `p` before searching for a nearby `q`.