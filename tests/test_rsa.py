from src.rsa import keygen, encrypt, decrypt, decrypt_crt
import random 
import pytest 


def test_mykey():
    for m in range(713):
        c = encrypt(m, 713, 101)
        assert(decrypt(c, 713, 281) == m), f"decrypt on {m} is wrong"
        assert(decrypt_crt(c, 23, 31, 281) == m), f"decrypt_crt on {m} is wrong."

def test_secondkey():
    p = 11177; q = 11503
    dict = keygen(p,q)
    n = dict["n"]; e = dict["e"]; d = dict["d"]; lam = dict["lam"]
    sample = random.sample(range(n), k = 200)
    for m in sample:
        c = encrypt(m, n, e)
        assert(decrypt(c, n, d) == m)
        assert(decrypt_crt(c, p, q, d) == m)

@pytest.mark.parametrize("invalid_inputs", [-1,713])
def test_edge_cases_encrypt(invalid_inputs):
    with pytest.raises(AssertionError):
        encrypt(invalid_inputs, 713, 101)

@pytest.mark.parametrize("invalid_inputs", [-1,713])
def test_edge_cases_decrypt(invalid_inputs):
    with pytest.raises(AssertionError):
        decrypt(invalid_inputs, 713, 281)

@pytest.mark.parametrize("invalid_inputs", [-1,713])
def test_edge_cases_decrypt_crt(invalid_inputs):
    with pytest.raises(AssertionError):
        decrypt_crt(invalid_inputs, 23, 31, 281)

# tests same inputs on keygen raises AssertionError, no primality check
@pytest.mark.parametrize("invalid_inputs", [3,5,11])
def test_keygen(invalid_inputs):
    with pytest.raises(AssertionError):
        keygen(invalid_inputs, invalid_inputs)