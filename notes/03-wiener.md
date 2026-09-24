# Wiener's Attack

The goal is: given `n` and `e`, recover `d_φ = modinv(e, φ(n))` (`1 < d_φ < φ(n)`) without actually computing `φ(n)` from `p` and `q`.

Throughout this note, `d_φ` denotes the least positive inverse of `e` modulo `φ(n)`, while `d_λ` denotes the least positive inverse of `e` modulo `λ(n)`. The unqualified symbol `d` is used only for a generic RSA private exponent.

## 1. The starting Diophantine equation

Let `n = pq` for distinct odd primes `p < q`, and assume `1 < e < φ(n)`. Then we aim to find `d_φ = modinv(e, φ(n))`. Now, there exists a unique positive integer `k` such that

```
e d_φ − k φ(n) = 1
```

Moreover, since `e < φ(n)`, we have `0 < k < d_φ`. Now, the idea is that `φ(n) ≈ n` if `p` and `q` are somewhat close; this implies

```
e/n ≈ k/d_φ
```

Therefore, we might find *candidate* values of `k/d_φ` from `e/n`.

## 2. Bounding `|e/n − k/d_φ|` in terms of `d_φ`

**Classical Wiener.** Assume further `p < q < 2p` and `d_φ < n^{1/4}/3`. Then

```
|e/n − k/d_φ| < 1/(2 d_φ^2)
```



### Proof

Let `φ(n) = n − s`, so `s = p + q − 1`. Then

```
ed_φ − k φ(n) = 1
ed_φ − kn = 1 − ks
|e/n − k/d_φ| = (ks − 1) / (n d_φ)
```

As `k < d_φ`, we can bound `|e/n − k/d_φ| < s/n`. However, as `p < q < 2p` we can bound `p^2 < pq = n` and `q^2/2 < n`. Therefore

```
p < √n
q < √(2n)
```

Hence

```
|e/n − k/d_φ| < s/n
              < (1 + √2)/√n
              < (1 + √2)/(9 d_φ^2)
              < 1/(2 d_φ^2)
```

where the second-to-last inequality comes from `d_φ < n^{1/4}/3`.

Now, one might wonder: why is bounding this way good? The answer lies in the following theorem.

**Legendre's theorem.**

```
Let α be a real number, and u/v a rational in lowest terms.
Suppose |α − u/v| < 1/(2 v^2).
Then u/v is a continued-fraction convergent of α.
```



## 3. Finding candidate values of `k` and `d_φ` and recovering `p` and `q`

Since `|e/n − k/d_φ| < 1/(2 d_φ^2)`, the fraction `k/d_φ` is a continued-fraction convergent of `e/n`. Also `gcd(k, d_φ) = 1`, so the pair `(k, d_φ)` appears among the convergents `r0, r1, …, rm` of `e/n`.

The true `k` and `d_φ` satisfy `ed_φ − k φ(n) = 1`, so `k` divides `e d_φ − 1`. We then recover `φ(n) = (e d_φ − 1)/k`, and hence `p + q` as well. Let `x` be this value of `p + q`. Then `x^2 − 4n` must be a perfect square, since it equals `(p − q)^2` for the true `k` and `d_φ`. We record this as a claim.

### Claim. The only positive integers `x` for which `x^2 − 4n` is a perfect square are `x = n + 1` and `x = p + q`.

**Proof**

```
Suppose x^2 − 4n = x^2 − 4pq = y^2 for some y ≥ 0.
Then x^2 − y^2 = 4pq.

If x and y are both odd, then x^2 ≡ y^2 ≡ 1 (mod 8).
But 8 does not divide 4pq. So x and y are even.

Write x = 2 x0 and y = 2 y0.
Then x0^2 − y0^2 = pq, which yields

(x0, y0) = ((n + 1)/2, (n − 1)/2)
        or ((p + q)/2, (q − p)/2)

as proved in the Fermat note.
Hence x = 2 x0 is n + 1 or p + q, as desired.
```

The following algorithm fully describes Wiener's attack.

## 4. The algorithm

```
Let r0, r1, …, rm be the convergents of e/n, and write
ri = ki/di for each 0 ≤ i ≤ m, where ki are non-negative integers, 
di are positive integers, and gcd(ki, di) = 1.

For i from 0 to m:
  compute e di − 1 and test whether ki divides it.
  If not, go to the next i.
  If it does, set
    phi = (e di − 1)/ki
    x   = n + 1 − phi
  and check whether x > 0 and x^2 − 4n is a perfect square.
  If one of them is wrong, go to the next i.
  Otherwise, by the claim, x is either n + 1 or p + q.
  If x = n + 1, go to the next i.
  Otherwise we have x = p + q and
    phi = (p − 1)(q − 1)
  is the true value.
  Finally, return modinv(e, phi).
```

Note: Legendre's theorem guarantees that we can find a pair `(ki, di)` that satisfies

```
e di − ki φ(n) = 1
```

Therefore, successfully recovering `φ(n)` and `d_φ = modinv(e, φ(n))`.

## 5. Conclusion of Wiener's Attack

**i. Guarantee under Classical Wiener**

Assume the hypotheses of **Classical Wiener**:

```
1 < e < φ(n)
d_φ = modinv(e, φ(n)) < n^{1/4}/3
p < q < 2p
```

Then the algorithm of §4, given only `(n, e)`, returns the inverse `d_φ` of `e` modulo `φ(n)`. Hence, a working decryption key.

**ii. What** `keygen` **actually stores**

Our `keygen` stores `d_λ = e^{-1} (mod λ(n))`, while Wiener's attack recovers `d_φ = e^{-1} (mod φ(n))`. These satisfy

```
e d_λ − k_λ λ(n) = 1
e d_φ − k_φ φ(n) = 1
```

for some positive integers `k_λ` and `k_φ`. Since `λ(n) | φ(n)`, we have `e d_φ ≡ e d_λ ≡ 1 (mod λ(n))`. As `gcd(e, λ(n)) = 1`, it follows that `d_φ ≡ d_λ (mod λ(n))`. Combined with `0 < d_λ < λ(n)` and `0 < d_φ < φ(n)`,

```
d_φ = d_λ + j λ(n)
```

for some integer `j` with `0 ≤ j < φ(n)/λ(n) = gcd(p − 1, q − 1)`. Thus `d_φ` equals `d_λ` plus a non-negative integer multiple of `λ(n)` (possibly zero).

**iii. Practical consequence**

It is possible that `d_λ` is small while `d_φ` is much larger than `n^{1/4}/3`. In that case the attack usually misses `d_φ` and recovers nothing. On the other hand, the **Classical Wiener** bound is sufficient, not necessary: `d_φ` may lie slightly above `n^{1/4}/3` and the attack can still hit. If it does, the returned exponent is `d_φ`, which decrypts even when `d_φ ≠ d_λ`.

For instance, in `test_wiener`, specifically in `test_d_phi_large`, `d_φ` was chosen between 3 and 4 times `n^{1/4}/3`. In some runs, Wiener's attack successfully recovered `d_φ`, and the resulting key decrypted correctly; on other instances, the attack may fail to recover it.

## 6. Finding the convergents of a rational

For an integer `a_0` and positive integers `a_1, …, a_n`, write `[a_0; a_1, …, a_n]` for the usual finite continued fraction.

**Lemma.** Let `k ≥ 0` be an integer, let `a_0` be an integer, and let `a_1, …, a_{k+2}` be positive integers. For `i = k, k+1, k+2`, let `p_i/q_i` be `[a_0; a_1, …, a_i]` in lowest terms with `q_i > 0`. Then

```
p_{k+2} = a_{k+2} p_{k+1} + p_k
q_{k+2} = a_{k+2} q_{k+1} + q_k
```

The claim is that this holds for every such sequence (not for a single fixed sequence).

*Proof of Lemma*

Induct on `k`. For `k = 0`,

```
[a_0]           = a_0 / 1
[a_0; a_1]      = (a_0 a_1 + 1) / a_1
[a_0; a_1, a_2] = (a_0 a_1 a_2 + a_2 + a_0) / (a_1 a_2 + 1)
```

Each fraction is already in lowest terms:

```
gcd(a_0, 1) = 1
gcd(a_0 a_1 + 1, a_1) = gcd(1, a_1) = 1
gcd(a_0 a_1 a_2 + a_2 + a_0, a_1 a_2 + 1) = gcd(a_2, 1) = 1
```

and these numerators and denominators satisfy the claimed recurrence.

Now fix `k ≥ 0` and assume the lemma holds at this `k` for every eligible sequence. We prove it at `k+1`. Let `a_0` be an integer and let `a_1, …, a_{k+3}` be positive integers. Then

```
[a_0; a_1, …, a_{k+1}] = a_0 + 1 / [a_1; a_2, …, a_{k+1}]
[a_0; a_1, …, a_{k+2}] = a_0 + 1 / [a_1; a_2, …, a_{k+2}]
[a_0; a_1, …, a_{k+3}] = a_0 + 1 / [a_1; a_2, …, a_{k+3}]
```

For `i = k+1, k+2, k+3`, let `p_i/q_i` be the tail `[a_1; a_2, …, a_i]` in lowest terms with `q_i > 0`. Applying the inductive hypothesis to the shifted sequence `a_1, a_2, …, a_{k+3}` gives

```
p_{k+3} = a_{k+3} p_{k+2} + p_{k+1}
q_{k+3} = a_{k+3} q_{k+2} + q_{k+1}
```

Hence

```
[a_0; a_1, …, a_{k+1}] = (a_0 p_{k+1} + q_{k+1}) / p_{k+1}
[a_0; a_1, …, a_{k+2}] = (a_0 p_{k+2} + q_{k+2}) / p_{k+2}
[a_0; a_1, …, a_{k+3}] = (a_0 p_{k+3} + q_{k+3}) / p_{k+3}
```

Each of these is already in lowest terms, since `gcd(a_0 p_i + q_i, p_i) = gcd(q_i, p_i) = 1`. Write `P_i/Q_i` for `[a_0; a_1, …, a_i]` in lowest terms. Then `P_i = a_0 p_i + q_i` and `Q_i = p_i` for `i = k+1, k+2, k+3`, and

```
P_{k+3} = a_0 p_{k+3} + q_{k+3}
        = a_0 (a_{k+3} p_{k+2} + p_{k+1}) + (a_{k+3} q_{k+2} + q_{k+1})
        = a_{k+3} (a_0 p_{k+2} + q_{k+2}) + (a_0 p_{k+1} + q_{k+1})
        = a_{k+3} P_{k+2} + P_{k+1}

Q_{k+3} = p_{k+3}
        = a_{k+3} p_{k+2} + p_{k+1}
        = a_{k+3} Q_{k+2} + Q_{k+1}
```

as required.

*end of proof*

Therefore, if a rational `A/B` has continued-fraction expansion `[a_0; a_1, …, a_m]`, its convergents may be computed by

```
1.  p_0 = a_0,  q_0 = 1
    p_1 = a_0 a_1 + 1,  q_1 = a_1

2.  for 2 ≤ i ≤ m,
    p_i = a_i p_{i-1} + p_{i-2}
    q_i = a_i q_{i-1} + q_{i-2}
```

By the lemma, `[a_0; a_1, …, a_i] = p_i/q_i` in lowest terms for all `0 ≤ i ≤ m`.

## 7. Example attack

This key is generated so that `d_φ = e^{-1} (mod φ(n))` is small: `p = 383`, `q = 523`, `d_φ = 5`, and `e = 39881`. Then `n = 200309` and `p < q < 2p`, with `d_φ = 5 < n^{1/4}/3 ≈ 7`. Suppose we are given only the pair `(n, e) = (200309, 39881)`. Then

```
e/n = 39881/200309 = [0; 5, 44, 8, 1, 1, 1, 1, 3, 1, 1, 2]
```

The recurrence of §6 gives

```
1.  p_0 = 0,  q_0 = 1
    p_1 = 1,  q_1 = 5

2.  for 2 ≤ i ≤ 11,
    p_i = a_i p_{i-1} + p_{i-2}
    q_i = a_i q_{i-1} + q_{i-2}
```

and therefore

```
p_0/q_0   = 0/1
p_1/q_1   = 1/5
p_2/q_2   = 44/221
p_3/q_3   = 353/1773
p_4/q_4   = 397/1994
p_5/q_5   = 750/3767
p_6/q_6   = 1147/5761
p_7/q_7   = 1897/9528
p_8/q_8   = 6838/34345
p_9/q_9   = 8735/43873
p_10/q_10 = 15573/78218
p_11/q_11 = 39881/200309
```

These are the candidates for `k/d_φ`. Skip `0/1`. The next pair `1/5` already satisfies `k | (ed_φ − 1)`:

```
ed_φ − 1 = 39881 · 5 − 1 = 199404
φ(n)   = 199404 / 1 = 199404
x      = n + 1 − φ(n) = 906
x^2 − 4n = 19600 = 140^2
```

Here `x > 0` and `x ≠ n + 1`, so `x = p + q` and `q − p = 140`. Hence `p = 383`, `q = 523`, and `d_φ = 5`. Encrypting `m = 42` gives `c = 42^e (mod n) = 43867`, and `c^{d_φ} ≡ 42 (mod n)`.

## 8. A documented miss: `(n, e) = (195571, 12965)`

The same algorithm, applied to `e/n`, recovers no `d_φ`.

```
e/n = 12965/195571 = [0; 15, 11, 1, 4, 1, 6, 5, 5]
```

```
p_0/q_0 = 0/1
p_1/q_1 = 1/15
p_2/q_2 = 11/166
p_3/q_3 = 12/181
p_4/q_4 = 59/890
p_5/q_5 = 71/1071
p_6/q_6 = 485/7316
p_7/q_7 = 2496/37651
p_8/q_8 = 12965/195571
```

Skip `0/1`. Only `1/15` satisfies `k | (e d_i − 1)`. For that pair, `x = 1098` and `x^2 − 4n = 423320` is not a square. Every later pair fails the divisibility check. So §4 recovers nothing.

This is expected under Classical Wiener: `n^{1/4}/3 ≈ 7`, while every candidate after `0/1` has denominator `d_i ≥ 15 > 7`. The bound in §2 does not apply.

The miss is the phenomenon of §5 part iii: this public key has a tiny `λ`-inverse `d_λ = 5` (which does decrypt `m = 42`) and a large `φ`-inverse `d_φ = 64829`. Convergents of `e/n` hunt `k/d_φ`, so the attack never sees `5`. After factoring,

```
n = 223 · 877
φ(n) = 194472
λ(n) = 32412
d_φ = d_λ + 2 λ(n)
```

