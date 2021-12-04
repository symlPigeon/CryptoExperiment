from func import long_to_bytes, bytes_to_long
from sm3 import sm3
from sm2point import *
import random
from typing import Tuple


def calcZ_A(usr_id: str, pubKey: point, ecc = SM2_ECC) -> bytes:
    """
    用户的杂凑值。
    Z_A=SM3(ENTL_A||ID_A||a||b||x_G||y_G||x_A||y_A)
    """
    entl = long_to_bytes(len(usr_id) * 8)
    assert len(entl) <= 2, "User id too long!"
    if len(entl) == 1:  
        entl = b'\x00' + entl
    data = entl + usr_id.encode()
    data += long_to_bytes(ecc.sm2_a) + long_to_bytes(ecc.sm2_b) + long_to_bytes(ecc.sm2_xG) + long_to_bytes(ecc.sm2_yG)
    data += long_to_bytes(pubKey.xG) + long_to_bytes(pubKey.yG)
    H = long_to_bytes(sm3(data))
    return H


def sm2DigitSignFunc(Z_A: bytes, msg: bytes, privKey: int, ecc = SM2_ECC) -> tuple[bytes, bytes]:
    """
    SM2 签名，返回一个(r, s)
    """
    # M_ = Z_A || msg
    M = Z_A + msg
    # e = H_256(M_)
    e = sm3(M)
    while True:    
        k = random.randint(1, ecc.sm2_n - 1)
        G = ecc.sm2_G
        # p' = [k]G
        p_ = point_mul(G, k, ecc.sm2_p, ecc.sm2_a, ecc.sm2_b)
        x1 = p_.xG
        # x1, y1 = p'
        # r = (e + x1) mod n
        r = (e + x1) % ecc.sm2_n
        if r == 0 or r + k == sm2_n:
            continue
        inv_d = invert(privKey + 1, ecc.sm2_n)
        # s = (d_A + 1)^{-1} * (k - r * d_A) mod n
        s = (inv_d * ((k - r * privKey))) % ecc.sm2_n
        if s == 0:
            continue
        return (long_to_bytes(r), long_to_bytes(s))


def sm2DigitVerifyFunc(msg: bytes, sign: Tuple[bytes, bytes], Z_A: bytes, pubKey: point, ecc = SM2_ECC) -> bool:
    """
    验签
    """
    r, s = sign
    r, s = bytes_to_long(r), bytes_to_long(s)
    if not(0 <= r <= ecc.sm2_n - 1) or not(0 <= s <= ecc.sm2_n - 1):
        return False
    M_ = Z_A + msg
    e = sm3(M_)
    t = (r + s) % ecc.sm2_n
    if t == 0:
        return False
    P = point_add(
            point_mul(ecc.sm2_G, s, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b), 
            point_mul(pubKey, t, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b),
            p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b
        )
    x1 = P.xG
    R = (e + x1) % ecc.sm2_n
    if R == r:
        return True
    else:
        return False


'''
class test_ecc_class:
    sm2_p = 0x8542d69e4c044f18e8b92435bf6ff7de457283915c45517d722edb8b08f1dfc3
    sm2_a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    sm2_b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    sm2_xG = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    sm2_yG = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    sm2_n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    def __init__(self):
        self.sm2_G = point(
            xG = self.sm2_xG,
            yG = self.sm2_yG,
            is_sm2=False,
            p = self.sm2_p,
            a = self.sm2_a,
            b = self.sm2_b
        )
test_ecc = test_ecc_class()

P = point(
    xG = 0x0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A,
    yG = 0x7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857,
    is_sm2=False,
    p=test_ecc.sm2_p,
    a=test_ecc.sm2_a,
    b=test_ecc.sm2_b
)

d = 0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
Z_A = calcZ_A("ALICE123@YAHOO.COM", P, test_ecc)
sign = sm2DigitSignFunc(Z_A, b"message digest", d, ecc=test_ecc)
print(sm2DigitVerifyFunc(b"message digest", sign, Z_A, P, ecc=test_ecc))
'''