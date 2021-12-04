from sm2point import point, infintyPoint, point_add, point_mul, SM2_ECC, bytes2point
from func import long_to_bytes, bytes_to_long, bytes_xor
from sm2KDF import KDF
from sm3 import sm3
import random
import math


def sm2encrypt(msg: bytes, pubKey: point, ecc=SM2_ECC):
    while True:
        k = random.randint(1, ecc.sm2_n - 1)
        C1 = point_mul(ecc.sm2_G, k, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
        C1_bytes = C1.toUnompressedBytes()
        #S = point_mul(ecc.sm2_G, h) # optional, h没给
        P2 = point_mul(pubKey, k, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
        x2, y2 = P2.xG, P2.yG
        x2b = long_to_bytes(x2)
        y2b = long_to_bytes(y2)
        t = KDF(x2b + y2b, len(msg) * 8)
        if bytes_to_long(t) == 0:
            continue
        C2 = bytes_xor(msg, t)
        C3 = long_to_bytes(sm3(x2b + msg + y2b))
        return C1_bytes + C2 + C3


def sm2decrypt(cipher: bytes, msglen: int, privKey: int, ecc=SM2_ECC):
    keyl = math.ceil(math.log2(ecc.sm2_p) / 8) * 2 + 1
    C1b = cipher[:keyl]
    C1 = bytes2point(C1b, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
    C1.verify()
    S = point_mul(C1, privKey, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
    x2, y2 = S.xG, S.yG
    x2b, y2b = long_to_bytes(x2), long_to_bytes(y2)
    t = KDF(x2b + y2b, msglen * 8)
    assert bytes_to_long(t) != 0, "Invalid msg!"
    msg = bytes_xor(cipher[keyl:keyl + msglen], t)
    u = sm3(x2b + msg + y2b)
    C3 = cipher[-32:]
    if long_to_bytes(u) != C3:
        print("Invalid cipher")
    return msg