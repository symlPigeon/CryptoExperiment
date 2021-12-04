import random
from typing import Optional
import time


def mygcd(a: int, b: int) -> int:
    if a < b:
        a, b = b, a
    while b != 1:
        a, b = b, a % b
    return a


def fast_pow(a: int, b: int, n: Optional[int] = None) -> int:
    result = 1
    while b > 0:
        if b % 2 == 1:
            result *= a
            if n:
                result %= n
        b //= 2
        a *= a
        if n:
            a %= n
    return result


try:
    from gmpy2 import gcd
except ImportError:
    gcd = mygcd


try:
    n = int(input("[\33[32m*\033[0m] Enter the big number n:"))
    k = int(input("[\33[32m*\033[0m] Enter the k:"))
    assert k > 0, "[\33[31m+\033[0m] k too small"
    assert n > 0, "[\33[31m+\033[0m] not valid n"
    assert k < n - 2, f"[\33[31m+\033[0m] k = \33[34m{k}\033[0m is too big for n = \33[34m{n}\033[0m"
except ValueError:
    print("[\33[31m+\033[0m] Not Valid Input.")
    exit()
except AssertionError as e:
    print(e)
    exit()


print(f"[\33[32m+\033[0m] Start Fermat Primality Test.")
print(f"    n = \33[34m{n}\033[0m")
print(f"    k = \33[34m{k}\033[0m")


start_time = time.time()
number_list = []
flag = True
for i in range(k):
    a = random.randint(2, n - 2)
    print(f" [\33[32m+\033[0m] Test \33[34m{i + 1}\033[0m, using number a = \33[34m{a}\033[0m.")
    while a in number_list:
        a = random.randint(2, n - 2)
    number_list.append(a)
    gcd_ans = gcd(a, n)
    if gcd_ans == 1:
        r = fast_pow(a, n - 1, n)
        if r != 1:
            print(f"  [\33[32m-\033[0m] a^(n-1) = \33[34m{r}\033[0m(mod n).")
            print("  [\33[32m-\033[0m] \33[32mSTOP\033[0m")
            flag = False
            break
    else:
        print(f"  [\33[32m-\033[0m] GCD(a, n) = \33[34m{gcd_ans}\033[0m")
        print("  [\33[32m-\033[0m] \33[32mSTOP\033[0m")
        flag = False
        break
    print("  [\33[32m-\033[0m] \33[32mPASS\033[0m")
    print(f"          the probablity is \33[34m{1 - 1 / pow(2, i + 1)}\033[0m.")


if flag:
    print(f"[\33[32m+\033[0m] \33[34m{n}\033[0m \033[4;37;40mis a prime\033[0m, the probablity is \33[34m{1 - 1 / pow(2, k)}\033[0m.")
else:
    print(f"[\33[32m+\033[0m] \33[34m{n}\033[0m \033[4;37;40mis not a prime\033[0m.")

print(f"[\33[32m+\033[0m] Total cost \33[34m{time.time() - start_time}\033[0m seconds.")
