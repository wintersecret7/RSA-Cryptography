# Fermat factorization 

Let `p < q` be odd primes and `n = pq`. We hope to factorize `n` without knowing `p` and `q`.

## 1. Representing `n = pq` as a difference of squares

Set

```
a = (p + q)/2
b = (q − p)/2
```

Then `a` and `b` are positive integers (because `p` and `q` are both odd), and

```
a^2 − b^2 = ((p + q)^2 − (q − p)^2) / 4
          = (4pq) / 4
          = n
```

In particular

```
p = a − b
q = a + b
```

These are not the only positive integers `x > y > 0` with `x^2 − y^2 = n`. That equation is `(x + y)(x − y) = pq` with `x + y > x − y > 0`. The factor pairs of `pq` with first factor larger than the second are only `(pq, 1)` and `(q, p)`, so there are exactly two solutions:

```
1.  x + y = n,  x − y = 1
    ⇒  x = (n + 1)/2,  y = (n − 1)/2

2.  x + y = q,  x − y = p
    ⇒  x = (p + q)/2,  y = (q − p)/2
```

The second pair is the Fermat pair `(a, b)` above. The first is much larger:

```
(n + 1)/2 > (p + q)/2
```

as `q > p > 2`.

## 2. Finding `a` and `b` in `O((q − p)^2 / √n)` iterations

Let `a0 = ceil(√n)` (integer ceiling of the exact real square root). By AM-GM,

```
a = (p + q)/2 ≥ √(pq) = √n
```

and `a` is an integer, so `a ≥ a0`.

Fermat’s method: try `x = a0, a0+1, …` until `x^2 − n` is a perfect square `y^2`. The only candidates for such an `x` are `(p + q)/2` and `(n + 1)/2`. The second is larger, so the first hit is the true `a`. Then `b = √(a^2 − n)`, and `p = a − b`, `q = a + b`. The method therefore terminates at that `a`.

The number of trials is `a − a0 + 1`. Since `a0 ≥ √n`,

```
a − a0 + 1 ≤ (a − √n) + 1
a − √n = (q − p)^2 / (4(a + √n))
```

Again `a ≥ √n`, so `a + √n ≥ 2√n`, hence

```
a − √n ≤ (q − p)^2 / (8√n)
a − a0 + 1 ≤ (q − p)^2 / (8√n) + 1
```

That is why close primes are the weakness: the work is

```
O((q − p)^2 / √n)
```

not “try all factors up to `√n`.”

## 3. Float square-root error on large `n`

A Python `float` is IEEE 754 binary64: a 53-bit mantissa. Any integer with more than 53 bits of significance cannot be stored exactly. `math.sqrt(n)` first converts `n` to `float` (already wrong), then takes an approximate square root. Then `ceil` of that value need not equal `ceil(√n)`, so Fermat can start at the wrong `a0` with no exception.

Replace it by an integer square root: the largest integer `s` with `s*s ≤ n` (`isqrt`). Then

```
a0 = s      if s*s == n
a0 = s + 1  otherwise
```

`math.isqrt` is an integer algorithm and is allowed; `math.sqrt` is not.

## 4. Example: factoring `n = 1022117`

```
1010^2 = 1020100 < n
1011^2 = 1022121 > n
a0 = ceil(√n) = 1011
```

| `x` | `x^2 − n` | square? |
|---|---|---|
|`1011`|`4`|`2^2 = 4`, yes|

So

```
a = 1011
b = 2
p = a − b = 1009
q = a + b = 1013
1009 · 1013 = 1022117
```

Trial division up to `floor(√1013) = 31` (and likewise for `1009`): no prime `≤ 31` divides `1009` or `1013`. Hence `1022117 = 1009 · 1013` is the prime factorization.
