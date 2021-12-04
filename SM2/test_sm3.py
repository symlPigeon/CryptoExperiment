from sm3 import sm3

print("================================== SM3 HASH ALGORITHM ==================================")
print("|                                        TEST 1                                        |")
print("========================================================================================")
print("|  Message    \"abc\"                                                                    |")
m = b"abc"
hash = sm3(m)
print("|  Hash:", hex(hash)[2:], "             |")
print("========================================================================================")
if hex(hash)[2:] == "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0":
    print("                                  ==========")
    print("                                  || PASS ||")
    print("                                  ==========")
else:
    print("                                  ==========")
    print("                                  || FAIL ||")
    print("                                  ==========")
print("\n\n\n\n")

print("================================== SM3 HASH ALGORITHM ==================================")
print("|                                        TEST 2                                        |")
print("========================================================================================")
print("|  Message    \"abcdabcda...abcd\" for 128 times                                         |")
m = b"abcd" * 16 
hash = sm3(m)
print("|  Hash:", hex(hash)[2:], "             |")
print("========================================================================================")
if hex(hash)[2:] == "debe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732":
    print("                                  ==========")
    print("                                  || PASS ||")
    print("                                  ==========")
else:
    print("                                  ==========")
    print("                                  || FAIL ||")
    print("                                  ==========")