# 椭圆曲线参数生成
from sm2math import *
from sm3 import sm3
from typing import Tuple
import random

def genECCArg(p: int) -> Tuple[int, int, int]:
    # GM/T 0003.1-2012 D.1.1 Method 1
    # 椭圆曲线参数的生成
    assert isPrime(p), "Arg p is not a valid prime!"
    while True:
        SEED = getRandomBitSeq(192) # at least 192 bit
        H = sm3(SEED)
        r = H % p
        # choose a, b, s.t. rb^2=a^3(mod p)
        # we choose number a, then calaculate b by solving b^2=r^{-1}a^3(mod p)
        inv_r = invert(r, p)
        a = random.randint(0, p - 1)
        try:
            b = sqrtModP(p, (pow(a, 3, p) * inv_r) % p)
        except squareRootNotExistException:
            continue
        if (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p == 0:
            continue
        return (SEED, a, b)
    

def verifyECCArg(SEED, a, b, p):
    '''
    椭圆曲线参数有效性检验
    '''
    H_ = sm3(SEED)
    R_ = H_
    r_ = R_ % p
    if (r_ * pow(b, 2, p)) % p == pow(a, 3, p):
        return True
    else:
        return False

