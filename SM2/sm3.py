from typing import Union
from func import *

# Reference 《SM3密码杂凑算法》
# 国家密码管理局 2010.12

# 初始值
IV = [
    0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
    0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
]

# 常量
Tj = []
for j in range(16):
    Tj.append(0x79cc4519)
for j in range(16, 64):
    Tj.append(0x7a879d8a)

# 布尔函数
def FF_j(X, Y, Z, j):
    if 0 <= j and j <= 15:
        return X ^ Y ^ Z 
    else:
        return (X & Y) | (X & Z) | (Y & Z)

def GG_j(X, Y, Z, j):
    if 0 <= j and j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (~X & Z)

# 置换函数
def P0(X):
    return (X ^ rotl32(X, 9) ^ rotl32(X, 17))

def P1(X):
    return X ^ rotl32(X, 15) ^ rotl32(X, 23) 

# 填充
def padding(M: bytes) -> bytes:
    l = len(M) * 8 # bytes * 8
    M += b"\x80"
    while len(M) % 64 != 56:
        M += b"\x00"
    M += long_to_bytes8(l)
    return M


# 压缩函数
def CF(Vi, Bi):
    # 消息扩展
    W = bytes_to_word(Bi)
    W_ = []
    for j in range(16, 68):
        W.append((P1(W[j - 16] ^ W[j - 9] ^ rotl32(W[j - 3], 15)) ^ rotl32(W[j - 13], 7) ^ W[j - 6]))
    for j in range(64):
        W_.append((W[j] ^ W[j + 4]))
    # 压缩
    A, B, C, D, E, F, G, H = Vi
    for j in range(64):
        SS1 = rotl32((rotl32(A, 12) + E + rotl32(Tj[j], j)) & 0xffffffff, 7)
        SS2 = SS1 ^ rotl32(A, 12)
        TT1 = (FF_j(A, B, C, j) + D + SS2 + W_[j]) & 0xffffffff
        TT2 = (GG_j(E, F, G, j) + H + SS1 + W[j]) & 0xffffffff
        A, B, C, D = TT1, A, rotl32(B, 9), C
        E, F, G, H = P0(TT2), E, rotl32(F, 19), G
    return list_xor([A, B, C, D, E, F, G, H], Vi)


def sm3(M: Union[int, bytes]) -> int:
    if type(M) == int:
        M = long_to_bytes(M)
    M = padding(M)
    Vi = IV
    for i in range(len(M) // 64):
        Bi = M[i * 64: (i + 1) * 64]
        Vi = CF(Vi, Bi)
    return word_to_long(Vi)
