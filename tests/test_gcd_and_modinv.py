import random
import math
from src.ntt import egcd, modinv

N = 100 
a = random.choices(range(-1001,1001), k=N)
b = random.choices(range(-1001,1001), k=N)
m = random.choices(range(2,1001), k=N)
g, x, y, inv_a = [], [], [], []

for i in range(N):
    g1, x1, y1 = egcd(a[i], b[i])
    g.append(g1), x.append(x1), y.append(y1)
    m1 = modinv(a[i], m[i])
    inv_a.append(m1)

def test_egcd():
    for i in range(N):
        assert math.gcd(a[i], b[i]) == g[i], f"gcd wrong on input {i}"
        assert a[i]*x[i] + b[i]*y[i] == g[i], f"x,y pairs wrong on input {i}"
    assert egcd(0,0) == (0,0,0), "error on inputs (0, 0)"
    assert egcd(240 ,46) == (2, -9, 47)

def test_modinv():
    for i in range(N):
        if inv_a[i] is not None:
            assert inv_a[i] >= 0 and inv_a[i] < m[i], f"inverse not in range [0,m) on input{i}"
            assert (a[i]*inv_a[i])%m[i] == 1, f"not an inverse on input{i}"
        else:
            assert math.gcd(a[i], m[i]) != 1, f"returns None on input{i} but gcd is 1"
    assert modinv(17, 3120) == 2753
    assert modinv(2, 4) is None