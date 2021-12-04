# func for SM3

def rotl32(x: int, r: int) -> int:
    # 循环移位
    r = r % 32
    return ((x << r) | (x >> (32 - r))) & 0xffffffff


def bytes_to_word(m: bytes) -> list[int]:
    # 将bytes转换为32位int的list
    while len(m) % 4 != 0:
        m += b'\x00'
    l = []
    for i in range(len(m) // 4):
        # 小端序
        l.append(int.from_bytes(m[i * 4 : i * 4 + 4], byteorder='big'))
    return l


def long_to_bytes(n: int) -> bytes:
    # 将int转换为bytes, 求求了别再出错了
    b = b""
    while n > 0:
        b = int.to_bytes(n & 0xff, 1, byteorder="big") + b
        n >>= 8
    return b


def bytes_to_long(m: bytes) -> int:
    # 将bytes转换为int
    return int.from_bytes(m, byteorder='big')


def word_to_long(m: list) -> int:
    # 将32位int的list转换为int
    ans = 0
    for i in m:
        ans <<= 32
        ans += i
    return ans


def long_to_bytes8(x: int) -> bytes:
    # 将int转换为bytes，但是长度为64
    x = long_to_bytes(x)
    assert len(x) <= 8, "Length is too large"
    return b'\x00' * (8 - len(x)) + x


def long_to_bytes4(x: int) -> bytes:
    # 将int转换为bytes，但是长度为64
    x = long_to_bytes(x)
    assert len(x) <= 4, "Length is too large"
    return b'\x00' * (4 - len(x)) + x


def list_xor(l1: list, l2: list) -> list:
    assert len(l1) == len(l2), "list length not equal!"
    l = []
    for i in range(len(l1)):
        l.append(l1[i] ^ l2[i])
    return l


def bytes_xor(b1, b2):
    assert len(b1) == len(b2)
    b = b""
    for i in range(len(b1)):
        b += int.to_bytes(b1[i] ^ b2[i], 1, byteorder="big")
    return b