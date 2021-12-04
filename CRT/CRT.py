from gmpy2 import gcd


def invert(a: int, b: int) -> int:
    """
    a*x0+b*y0=1
    --> a*x0 = 1 (mod b)
    """
    x1, x2, x3, y1, y2, y3 = 1, 0, a, 0, 1, b
    while y3 != 0:
        q = x3 // y3
        x1, x2, x3, y1, y2, y3 = y1, y2, y3, x1 - q * y1, x2 - q * y2, x3 - q * y3
    return x1


k = 3
a = []
m = []

try:
    for i in range(k):
        a.append(int(input(f"[+] a_{i + 1} = ")))
    for i in range(k):
        m.append(int(input(f"[+] m_{i + 1} = ")))
except:
    print("[x] Invalid input!")
    exit()

for i in range(k - 1):
    for j in range(i + 1, k):
        if gcd(m[i], m[j]) != 1:
            print(f"[x] GCD({m[i]}, {m[j]}) is not equal to 1.")
            exit()

M = 1
for i in m:
    M *= i
M_i = []
for i in m:
    M_i.append(M // i)
invert_M_i = [invert(a, b) for a, b in zip(M_i, m)]
x = 0
for i in range(k):
    x += M_i[i] * invert_M_i[i] * a[i]
x %= M
print(f"[+] x = {x} (mod {M})")
