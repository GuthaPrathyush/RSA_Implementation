from curses.ascii import isdigit
from sympy import randprime
from math import gcd
import random


def get_p_and_q():
    p = randprime(2 ** 9, 2 ** 10)
    q = randprime(2 ** 9, 2 ** 10)
    while p == q:
        q = randprime(2 ** 9, 2 ** 10)
    return p, q


def get_phi_and_e(p, q):
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi)
    return phi, e


def get_d(phi, e):
    return pow(e, -1, phi)

def get_private_and_public_key():
    p, q = get_p_and_q()
    n = p * q
    phi, e = get_phi_and_e(p, q)
    d = get_d(phi, e)
    return e, d, n

def encrypt(e, n, m):
    return pow(m, e) % n


def decrypt(d, n, c):
    return pow(c, d) % n


if __name__ == '__main__':
    p, q = get_p_and_q()
    n = p * q
    phi, e = get_phi_and_e(p, q)
    d = get_d(phi, e)
    message = input('Enter a message: ')

    if isdigit(message):  # If it's a number
        message = int(message)
        flag = False
    else:  # If it's a string, consider only the first character
        message = ord(message[0])  # Convert the first character to ASCII
        flag = True

    enc = encrypt(e, n, message)
    dec = decrypt(d, n, enc)
    if(flag):
        chr(dec)

    print(f'Encrypted message: {enc}')
    print(f'Decrypted message: {dec}')
