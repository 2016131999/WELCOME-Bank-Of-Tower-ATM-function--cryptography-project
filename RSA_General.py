import random
import math


def is_prime(num):
    if num == 2:
        return True
    elif num < 2:
        return False
    elif num % 2 == 0:
        return False
    else:
        for i in range(3, int(math.sqrt(num)), 2):
            if num%i == 0:
                return False
    return True


def modular_inverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        q = a // m
        t = m

        # m is the remainder
        # same as the Euclid's gcd() algorithm
        m = a % m
        a = t
        t = y

        # update x and y accordingly
        y = x - q * y
        x = t

        # make sure x>0 so x is positive
    if (x < 0):
        x = x + m0
    return x


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_keys():
    p = random.randint(10, 100)
    while not is_prime(p):
        p = random.randint(10, 100)
    q = random.randint(10, 100)
    while not is_prime(q):
        q = random.randint(10, 100)
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi)
    d = modular_inverse(e, phi)
    return p, q, e, d


def encrypt(plain, pub, n):
    cipher = []
    cipher_text = ""
    for char in plain:
        a = ord(char)
        cipher.append(pow(a, pub, n))
    for item in cipher:
        cipher_text += chr(item)
    return cipher_text, cipher


def decrypt(cipher, priv, n):
    plain = ''
    for num in cipher:
        a = pow(num, priv, n)
        plain = plain + str(chr(a))
    return plain


def decrypt_text(cipher_text, priv, n):
    cipher = [ord(x) for x in cipher_text]
    return decrypt(cipher, priv, n)