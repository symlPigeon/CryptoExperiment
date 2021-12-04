import random

from Crypto.Util.number import getPrime
import gmpy2


x_bit = 512
k = 3
n = 5


def get_d_seq():
    print("[+] Generate d_i sequence...")
    d = []
    for bit_len in [201, 202, 203, 204, 205]:
        d.append(getPrime(bit_len))
    print("[+] Finish generate d_i sequence.")
    for i in range(len(d)):
        print(f"[+] d_{ i } = \33[32m{ d[i] }\033[0m")
    print(f"[+] N = \33[32m{ d[0] * d[1] * d[2] }\033[0m")
    print(f"[+] M = \33[32m{ d[3] * d[4] }\033[0m")
    return d


print("#### Secret share based on CRT ####")
d = get_d_seq()


for file_no in range(10):
    f = open(f"sec_{file_no}.txt", "r")
    x = int(f.read())
    f.close()
    print("\n\n#################")
    print("[+] Load secret:  \33[32m", x, "\033[0m")
    print("[+] Result:")
    for i in d:
        print("x=\33[34m{}\033[0m(mod \33[34m{}\033[0m)".format(x % i, i))
    a = [x % i for i in d]

    print("[+] Using 3 keys to solve...")
    r = [0, 1, 2, 3, 4]
    random.shuffle(r)
    r = r[0 : 3]
    d_ = [d[_] for _ in r]
    a_ = [a[_] for _ in r]

    print("[+] Solve:")
    M = 1
    for i in d_:
        M *= i
    M_i = []
    for i in d_:
        M_i.append(M // i)
    invert_M_i = [gmpy2.invert(a, b) for a, b in zip(M_i, d_)]
    x = 0
    for i in range(k):
        x += M_i[i] * invert_M_i[i] * a_[i]
    x %= M
    print(f"[+] Recovered: x = \33[32m{x}\033[0m")

