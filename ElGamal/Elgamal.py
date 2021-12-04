from Crypto.Util.number import getPrime, getRandomRange, getRandomInteger, getStrongPrime
from gmpy2 import invert


def generate_key(bits):
    p = getStrongPrime(bits)
    phi = p - 1 # phi = 2 * q, q is a prime
    q = phi // 2
    g = getRandomRange(2, p - 1)
    while pow(g, q, p) == 1 and pow(g, 2, p) == 1:
        g = getRandomRange(2, p - 1)
    x = getRandomRange(1, q - 1)
    h = pow(g, x, p)
    return (h, p, g), x


def encrypt(m, pub_key):
    h, p, g = pub_key
    r = getRandomRange(1, p - 2)
    c1 = pow(g, r, p)
    c2 = (m * pow(h, r, p)) % p
    return c1, c2


def decrypt(c, pub_key, pri_key):
    h, p, g = pub_key
    c1, c2 = c
    s = pow(c1, pri_key, p)
    m = (c2 * invert(s, p)) % p
    return m


def main():
    print("[+] Generating Key...")
    key, pri_key = generate_key(1024)
    print("[+] Generated Key:")
    print("##### PUBLIC  KEY #####")
    print(f"  h=\33[34m{key[0]}\033[0m")
    print(f"  p=\33[34m{key[1]}\033[0m")
    print(f"  g=\33[34m{key[2]}\033[0m")
    print("##### PRIVATE KEY #####")
    print(f"  x=\33[34m{pri_key}\033[0m")
    print("#######################")
    m = int(input("[+] Input the Message: \33[32m"))
    c = encrypt(m, key)
    print("\033[0m[+]  Encrypt:")
    print(f"  c1=\33[34m{c[0]}\033[0m")
    print(f"  c2=\33[34m{c[1]}\033[0m")
    print("[+] Decrypt:\nm=\33[32m", decrypt(c, key, pri_key), "\033[0m")


if __name__ == '__main__':
    main()
