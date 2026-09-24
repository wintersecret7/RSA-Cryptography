# Pollard's `p−1` algorithm for integer factorization

Let `n = pq` where `p < q` are odd primes. Fix `1 < a < n` that is coprime to `n`. **Pollard's** `p−1` algorithm is based on finding an exponent `M` such that `p | (a^M − 1)`. So `g = gcd(a^M − 1, n)` is either `p` or `n`. It aims to make the first case happen.

## 1. Ensuring `p | (a^M − 1)`

FLT states that

```
If a is coprime to p, then a^{p-1} ≡ 1 (mod p)
```

Hence `p−1 | M` implies `p | (a^M − 1)`. Therefore `gcd(a^M − 1, n)` equals `p` iff `q ∤ (a^M − 1)` iff `ord_q(a) ∤ M`, and equals `n` iff `q | (a^M − 1)` iff `ord_q(a) | M`. In particular, the gcd cannot be `1`.

## 2. How do we ensure `gcd(a^M − 1, n)` equals `p`, not `n`?

We cannot always guarantee that the gcd equals `p`. We can, however, choose `M` so that the gcd is not forced to be `n`. FLT states that `a^{q-1} ≡ 1 (mod q)` for `gcd(a, q) = 1`. So our goal is to find `M` such that `p−1 | M` but `q−1 ∤ M`. Then `g = n` only if `ord_q(a) | M`; the remaining bet is that this fails. We introduce the following definition.

### i. Powersmooth Numbers

**Definition. *(Powersmooth)*** Let `B` be a positive integer.

```
A positive integer K is called B-powersmooth if any prime power divisor of K is at most B.
```

**Lemma 1.**

```
If p−1 is B-powersmooth, then p−1 divides both B! and lcm(1, 2, …, B).
```

*Proof of lemma 1*

We show only the latter case, as `lcm(1, 2, …, B) | B!`. Consider any prime power divisor `r^e` of `p−1`. By the powersmooth condition, `r^e ≤ B`. Therefore `r^e` is one of the integers in `{1, 2, …, B}`, hence `r^e | lcm(1, 2, …, B)`. Since this is true for any prime power divisor `r^e`, we conclude `p−1 | lcm(1, 2, …, B)`.

**Lemma 2.**

```
If q−1 is not B-powersmooth, then q−1 ∤ lcm(1, 2, …, B)
```

*Proof of lemma 2*

Since `q−1` is not `B`-powersmooth, there exists a prime power `r^e | (q−1)` with `r^e > B`. Then `r^e` divides none of the integers in `{1, 2, …, B}`, so `r^e ∤ lcm(1, 2, …, B)`, which implies `q−1 ∤ lcm(1, 2, …, B)`.

```
Note: q−1 not B-powersmooth does not necessarily imply q−1 ∤ B!.
For example, q = 17, B = 8. Then 16 is not 8-powersmooth, but 16 | 8!.
```

From the two lemmas, if `B` is such that `p−1` is `B`-powersmooth and `q−1` is not, then `M = lcm(1, 2, …, B)` satisfies `p−1 | M` and `q−1 ∤ M`. The factorial choice `M = B!` still satisfies `p−1 | B!`, but `q−1 ∤ B!` need not hold (see the note).

### ii. Why not use Smooth Numbers?

**Definition. *(Smooth)*** Let `B` be a positive integer.

```
A positive integer K is called B-smooth if any prime divisor of K is at most B.
```

A `B`-smooth number **only** guarantees that the prime divisors are at most `B`; it does not guarantee anything about the prime powers. So if `p−1` is `B`-smooth, it does not follow that `p−1 | B!`. For instance, `p = 17` yields `p−1 = 16`, which is `2`-smooth, but `16 ∤ 2!`. Therefore smoothness is not a sufficient condition to ensure `p | (a^M − 1)` for `M = B!` or `M = lcm(1, 2, …, B)`.

## 3. The algorithm

The two versions below correspond to the two choices of `M` in §2: `M = B!` and `M = lcm(1, 2, …, B)`. We first introduce the factorial version.

### i. Factorial Version

Given positive integers `n`, `B`, and `a` with `1 < a < n`. The goal is to find a nontrivial factor of `n`, or raise an error if it fails. First check whether `gcd(a, n) = 1`. If not, `gcd(a, n)` is a nontrivial factor of `n` (since `1 < a < n`). Otherwise, set `x ← a`, so that `x ≡ a^{1!} (mod n)`, and check `g ← gcd(x − 1, n)`. If `g ≠ 1`, then `g` is a nontrivial factor. (Here `g = n` cannot occur, since `1 < a < n`.) Otherwise:

```
for k ← 2 to B:
    x ← x^k mod n
    g ← gcd(x − 1, n)
    if g ≠ 1 and g ≠ n:
        return g     (nontrivial factor)
    if g = n:
        raise error
```

After the iteration for `k`, we have `x ≡ a^{k!} (mod n)`, since `a^{k!} = (a^{(k−1)!})^k`. Reducing modulo `n` keeps the accumulator `x` in `{1, …, n − 1}`, so we never form the integer `B!` as an exponent: each step only raises `x` to the small power `k`. Calling `gcd` after each `k` lets us test `M = 1!, 2!, …, B!` instead of only the last `M`. If we gcd only at the end and `n | (a^{B!} − 1)`, we recover nothing. We also abort when `gcd(x − 1, n) = n` in the middle of the loop: `a^{k!} ≡ 1 (mod n)`, and for every later index `m > k` we have `k! | m!`, hence `a^{m!} ≡ 1 (mod n)` as well.

If the algorithm has not returned after the loop, raise an error. That means `B` is not large enough, i.e. for every `1 ≤ k ≤ B` neither `p` nor `q` divides `a^{k!} − 1`, and we have to increase `B`.

### ii. Prime-powers Version

Given the same `n`, `B`, and `a`. The goal and the opening checks are as above: `gcd(a, n)`, then `x ← a`, then `gcd(a − 1, n)`. The difference is that we accumulate `M = lcm(1, 2, …, B) = ∏_{r ≤ B} r^{⌊log_r B⌋}`, prime by prime.

```
for prime r ← 2 to B:
    e ← ⌊log_r B⌋
    x ← x^{r^e} mod n
    g ← gcd(x − 1, n)
    if g ≠ 1 and g ≠ n:
        return g   (nontrivial factor)
    if g = n:
        raise error
```

After the iteration for `R`, we have `x ≡ a^{M_R} (mod n)` where `M_R = ∏_{r ≤ R} r^{⌊log_r B⌋}`. At the end of the loop this is `lcm(1, 2, …, B)`.

As in the factorial version, reducing modulo `n` keeps the accumulator `x` small, and calling `gcd` after each prime (each batch `r^e`) lets us test `M = M_1, M_2, …, M_B`. This allows `n` to split even if the full `lcm` is a multiple of both `p−1` and `q−1`. If `g = n` at some point, the remaining exponent is a multiple of the current `M_R`, so later gcds stay `n` and we abort.

If the algorithm has not returned after the loop, raise an error. Then `gcd(a^{M_R} − 1, n) = 1` after every prefix of primes, in particular for the full `M = lcm(1, 2, …, B)`. So neither `p` nor `q` divides `a^M − 1`; hence neither `p−1` nor `q−1` is `B`-powersmooth. We have to increase `B`.

## 4. Safeprimes

A prime `p` is a **safeprime** if `p = 2r + 1` for some prime `r`. Then, for `a` coprime to `p`, `ord_p(a)` divides `p−1 = 2r`. Therefore `ord_p(a)` is one of `1, 2, r, 2r`. Note that

```
ord_p(a) = 1  ⇔  a ≡ 1 (mod p)
ord_p(a) = 2  ⇔  a ≡ −1 (mod p)
```

These are only two residue classes modulo `p`. So when choosing a random `1 < a < n` coprime to `n`, it is almost certain that `ord_p(a)` equals `r` or `2r`. In either case we need `r | M` for `M = B!` or `M = lcm(1, 2, …, B)`. Since `r` is prime, this holds iff `r ≤ B`. Thus the minimum `B` required is `r = (p−1)/2`, and the attack still performs `O(p)` operations. If `p ≈ q`, this is `O(√n)` — no better than trial division. For any smaller `B`, typically `ord_p(a) ∤ M` and the gcd stays `1`.

## 5. Example

Suppose `n = 59713` and `a = 2`. We use the factorial version, starting from `x ← 2`.


| `B` | `x`                               | `gcd(x − 1, n)` |
| --- | --------------------------------- | --------------- |
| 2   | `x ← 2^2 (mod 59713) ≡ 4`         | 1               |
| 3   | `x ← 4^3 (mod 59713) ≡ 64`        | 1               |
| 4   | `x ← 64^4 (mod 59713) ≡ 57576`    | 1               |
| 5   | `x ← 57576^5 (mod 59713) ≡ 58806` | 1               |
| 6   | `x ← 58806^6 (mod 59713) ≡ 50151` | 1               |
| 7   | `x ← 50151^7 (mod 59713) ≡ 23422` | 211             |


Therefore `211` is a factor of `n`. Trial division up to `⌊√211⌋ = 14` and `⌊√283⌋ = 16` shows that both `211` and `283 = 59713/211` are prime. Now `p−1 = 210` is `7`-powersmooth, while `q−1 = 282` is `47`-powersmooth. So `B = 7` is the smallest bound with `p−1 | B!`, hence `211 | (2^{7!} − 1)`. The remaining bet is that `ord_{283}(2) ∤ 7!`; this holds, since `ord_{283}(2) = 94`.

## 6. 20-bit prime instance

One generated instance from [`test_pollard_p1`](../tests/test_pollard_p1.py) shows that both algorithms successfully factored `n = 516211723051 = 565489 * 912859 = p * q`, both recovering a nontrivial factor `565489`.