# 椭圆曲线算法点定义和运算实现

from sm2math import *
import math
from typing import Union
# 使用素数域上的椭圆曲线

# 椭圆曲线参数，参考GM/T 0003.5-2012
# 素域F_p，其中p为256位素数
sm2_p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
sm2_a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
sm2_b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
sm2_xG = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
sm2_yG = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
sm2_n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123


class point():
    def __init__(
            self, 
            xG: int, 
            yG: int, 
            is_sm2: bool = True, 
            p: Union[int, None] = None, 
            a: Union[int, None] = None,
            b: Union[int, None] = None
        ):
        self.xG = xG
        self.yG = yG
        if is_sm2:
            self.p = sm2_p
            self.a = sm2_a
            self.b = sm2_b
        else:
            self.p = p
            self.a = a
            self.b = b

    def verify(self):
        if pow(self.yG, 2, self.p) != (pow(self.xG, 3, self.p) + self.xG * self.a + self.b) % self.p:
            raise InvalidInputPointException

    # convert point to bytes.
    # GM/T 0003.1-2012 4.2.9
    def toCompressedBytes(self):
        y_ = self.yG & 1
        if y_ == 1:
            PC = b'\x03'
        else:
            PC = b'\x02'
        S = PC + self.xG.to_bytes(32, byteorder='big')
        return S

    def toUnompressedBytes(self):
        return b"\x04" + self.xG.to_bytes(32, byteorder='big') + self.yG.to_bytes(32, byteorder='big')

    def toHybridBytes(self):
        y_ = self.yG & 1
        if y_ == 1:
            PC = "\x07"
        else:
            PC = "\x06"
        return PC + self.xG.to_bytes(32, byteorder='big') + self.yG.to_bytes(32, byteorder='big')


class SM2_ECC_Class:
    sm2_p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    sm2_a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    sm2_b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    sm2_xG = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    sm2_yG = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    sm2_n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    sm2_G = point(
        xG = sm2_xG,
        yG = sm2_yG,
        is_sm2 = False,
        p = sm2_p,
        a = sm2_a,
        b = sm2_b
    )

SM2_ECC = SM2_ECC_Class()


class infintyPoint(point):
    # 这里没用父类的init方法，感觉并不好
    def __init__(self):
        self.xG = 0
        self.yG = 0


class InvalidBytesInputException(Exception):
    pass

class InvalidInputPointException(Exception):
    pass

    
# convert bytes to point.
# GM/T 0003.1-2012 4.2.10
def bytes2point(S: bytes, p: int = sm2_p, a: int = sm2_a, b: int = sm2_b) -> point:
    data = S[1:]
    PC = S[0]
    # log2(p) = 256
    if len(data) > 32: # uncompressed or hybrid
        if PC == 4:
            x = data[:32]
            y = data[32:]
            return point(int.from_bytes(x, byteorder='big'), int.from_bytes(y, byteorder='big'))
        elif PC == 6 or PC == 7:
            # GM/T 0003.1-2012 A.5.2
            x = data[:32]
            x = int.from_bytes(x, byteorder='big')
            if PC == 6:
                y_ = 0
            else:
                y_ = 1
            alpha = (pow(x , 3) + a * x + b) % p
            beta = sqrtModP(p, alpha)
            if beta & 1 == y_:
                y = beta
            else:
                y = p - beta
            return point(x, y)
        else:
            raise InvalidBytesInputException
    else: # compressed
        if PC == 2:
            y_ = 0
        elif PC == 3:
            y_ = 1
        else:
            raise InvalidBytesInputException
        data = data[:32]
        x = int.from_bytes(data, byteorder='big')
        alpha = (pow(x , 3) + a * x + b) % p
        beta = sqrtModP(p, alpha)
        if beta & 1 == y_:
            y = beta
        else:
            y = p - beta
        return point(x, y)

            
def point_add(p1: point, p2: point, p: int = sm2_p, a: int = sm2_a, b: int = sm2_b) -> point:
    # 仿射坐标下的加法
    if type(p1) == infintyPoint:
        return p2
    elif type(p2) == infintyPoint:
        return p1
    if p1.xG == p2.xG:
        if p1.yG % p == -p2.yG % p:
            return infintyPoint()
        lam = (3 * pow(p1.xG, 2, p) + a) * invert(2 * p1.yG, p) % p  
        # pow要加上模数，不然会出现玄学问题，国标文档里面的算例没有覆盖到
        # 下面的pow也是的
    else:
        lam = (p2.yG - p1.yG) * invert(p2.xG - p1.xG, p) % p
    x3 = (pow(lam, 2, p) - p1.xG - p2.xG) % p   
    y3 = (lam * (p1.xG - x3) - p1.yG) % p
    return point(x3, y3, is_sm2=False, p=p, a=a, b=b)


def point_mul(P: point, k: int,  p: int = SM2_ECC.sm2_p, a: int = SM2_ECC.sm2_a, b: int = SM2_ECC.sm2_b) -> point:
    # GM/T 0003.1-2012 A.3.2 椭圆曲线上多倍点运算的实现
    # 采用比较简单的二进制展开法，此外还有加减法和滑动窗法
    Q = infintyPoint()
    for j in range(int(math.log2(k)), -1, -1):
        # 类似快速幂的实现，对k进行二进制分解
        Q = point_add(Q, Q, p, a, b)
        if (k >> j) & 1:
            Q = point_add(Q, P, p, a, b)
    return Q    
