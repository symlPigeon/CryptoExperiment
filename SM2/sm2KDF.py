from sm3 import sm3
from func import *


def KDF(Z: bytes, klen: int) -> bytes:
    # 密钥派生函数
    # 一般长度也都是8的整数倍，所以说就返回一个bytes这样子方便一点，要不是的话那就自己去舍掉
    # 要命，能用就行
    v = 32
    l = round(klen / v)
    ct = 0x00000001
    Ha = []
    for i in range(l):
        #print(long_to_bytes4(ct))
        Ha.append(sm3(Z + long_to_bytes4(ct)))
        ct += 1
    if klen % v == 0:
        Ha_ = Ha[l - 1]
    else:
        Ha_ = (Ha[l - 1] >> (8 - klen + v * l)) << (8 - klen + v * l)
    key = b""
    for i in range(0, l - 1):
        temp = long_to_bytes(Ha[i])
        while len(temp) < 32:
            temp = b"\x00" + temp
        key += temp
    temp = long_to_bytes(Ha_)
    while (len(temp) < 32):
        temp = b"\x00" + long_to_bytes(Ha_)
    key += temp
    return key[:klen // 8]

'''
Z = long_to_bytes(0x47C826534DC2F6F1FBF28728DD658F21E174F48179ACEF2900F8B7F566E409052AF86EFE732CF12AD0E09A1F2556CC650D9CCCE3E249866BBB5C6846A4C4A295E4D1D0C3CA4C7F11BC8FF8CB3F4C02A78F108FA098E51A668487240F75E20F316B4B6D0E276691BD4A11BF72F4FB501AE309FDACB72FA6CC336E6656119ABD67)
klen = 128
print(hex(bytes_to_long(KDF(Z, klen))))
'''