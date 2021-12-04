# GM/T 0003.1-2012 附录B的算法
# 主要是数论算法
import random
import math

class squareRootNotExistException(Exception):
    pass


def invert(a, b):
    '''
    exgcd求逆元
    '''
    x1, x2, x3, y1, y2, y3 = 1, 0, a, 0, 1, b
    while y3 != 0:
        q = x3 // y3
        x1, x2, x3, y1, y2, y3 = y1, y2, y3, x1 - q * y1, x2 - q * y2, x3 - q * y3
    return x1 % b


"""
def genLucasSequence(p, X, Y, k):
    '''
    Lucas序列的生成。
    X, Y为非零整数，定义X和Y的Lucas序列U_k, V_k:
    U_0=0, U_1=1, 当k\geq 2, U_k=X\dot U_{k-1}-Y\dot U_{k-2};
    V_0=2, V_1=X, 当k\geq 2, V_k=X\dot V_{k-1}-Y\dot V_{k-2}.
    这里采用快速计算方法
    '''
    delta = (pow(X, 2) - 4 * Y) % p
    U = 1
    V = X
    inv2 = invert(2, p)
    print(inv2)
    for i in range(int(math.log2(k)), -1, -1):
        U, V = (U * V) % p, ((pow(V, 2, p) + delta * pow(U, 2, p)) * inv2) % p
        if (k >> i) & 1:
            U, V = ((X * U + V) * inv2) % p, ((X * V + delta * U) * inv2) % p
    return U, V

def sqrtModP(p, g):
    '''
    参考GM/T 0003.1-2012 附录B
    计算y^2=g(mod p)的解。
    '''
    if p % 4 == 3:
        u = p // 4
        y = pow(g, u + 1, p)
        z = pow(y, 2, p)
        if z == g:
            return y
        else:
            raise squareRootNotExistException
    elif p % 8 == 5:
        u = p // 8
        z = pow(g, 2 * u + 1, p)
        if z == 1:
            y = pow(g, u + 1, p)
            return y
        elif z == p - 1:
            y = (2 * g * pow(4 * g, u, p)) % p
            return y
        else:
            raise squareRootNotExistException
    elif p % 8 == 1:
        u = p // 8
        Y = g
        X = random. randint(1, p - 1)
        while True:
            U, V = genLucasSequence(p, X, Y, 4 * u + 1)
            if (V * V) % p == (4 * Y) % p:
                return (V // 2) % p
            if U % p != 1 and U % p != p - 1:
                raise squareRootNotExistException
            X = random.randint(1, p)
"""


def sqrtModP(p,n):
    '''
    Tonelli-Shanks Algorithm 
    calculating x for x^2=n(mod p)
    '''
    if(int(math.pow(n,(p-1)/2))%p !=1):
        raise squareRootNotExistException()
    # find max power of 2 dividing p-1
    s=0
    while((p-1)%math.pow(2,s)==0):
        s+=1
    s-=1
    q=int((p-1)/math.pow(2,s))# p-1=q*2^s
    # Select a z such that z is a quadratic non-residue modulo p
    z=1
    res=int(math.pow(z,(p-1)/2))%p
    while(res !=p-1):
        z+=1
        res=math.pow(z,(p-1)/2)%p
    c=int(math.pow(z,q))%p
    r=int(math.pow(n,(q+1)/2))%p
    t=int(math.pow(n,q))%p
    m=s
    while(t%p !=1):
        i=0
        div=False
        while(div==False):
            i+=1
            t=int(math.pow(t,2))%p
            if(t%p==1):
                div=True
        b=int(math.pow(c,int(math.pow(2,m-i-1))))%p
        r=(r*b)%p
        t=t*(b**2)%p
        c=(b**2)%p
        m=i
    return r


def isPrime(u: int, T: int = 256) -> bool:
    '''
    Miller-Rabin Primality Test
    '''
    if u == 1:
        return False
    if u == 2:
        return True
    if u % 2 == 0:
        return False
    v = 0
    w = u - 1
    while w % 2 == 0:
        v += 1
        w //= 2
    for j in range(T):
        a = random.randint(2, u - 1)
        b = pow(a, w, u)
        if b == 1 or b == u - 1:
            continue
        flag = True
        for i in range(1, v):
            b = pow(b, 2, u)
            if b == u - 1:
                flag = False
                break
            if b == 1:
                return False
        if flag:
            return False
    return True


#print(isPrime(17))


def getRandomBitSeq(bitlen: int) -> int:
    r = ""
    for i in range(bitlen):
        r += random.choice(['0', '1'])
    return int(r, 2)
