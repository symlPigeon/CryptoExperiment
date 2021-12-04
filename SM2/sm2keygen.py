# SM2密钥生成和检验

from sm2math import *
from sm2point import *
from typing import Tuple
import random
import time


def sm2KeyGen(p: int = sm2_p, n: int = sm2_n, a: int = sm2_a, b: int = sm2_b, xG: int = sm2_xG, yG: int = sm2_yG) -> Tuple[int, point]:
    """
    SM2密钥生成
    """
    d = random.randint(1, n - 2)
    G = point(xG, yG, is_sm2=True)
    P = point_mul(G, d)
    return (d, P)


def sm2VerifyPubKey(P: point, p: int = sm2_p, a: int = sm2_a, b: int = sm2_b, n: int = sm2_n) -> bool:
    """
    SM2公钥有效性检验
    """
    if type(P) == infintyPoint:
        return False
    if not(0 <= P.xG <= p - 1) or not(0 <= P.yG <= p - 1):
        return False
    if pow(P.yG, 2, p) != (pow(P.xG, 3, p) + a * P.xG + b) % p:
        return False
    if type(point_mul(P, n)) != infintyPoint:
        return False
    return True


start_time = time.time()
d, P = sm2KeyGen()
while not sm2VerifyPubKey(P):
    d, P = sm2KeyGen()
print("SM2密钥生成和检验用时：", time.time() - start_time)