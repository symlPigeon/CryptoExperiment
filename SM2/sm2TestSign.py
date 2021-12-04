from sm2digitSign import sm2_sign, sm2_verify
from sm2keygen import sm2KeyGen
from sm2point import SM2_ECC
from binascii import b2a_base64
import random


user_id = "2163953074@qq.com"
msg = b"Hello there, this is homework for XDU SCE Cryptogam Experiments"
print("+---------------------------------------------------------------------------------------------+")
print("|                                       SM2 签名测试                                          |")
print("+---------------------------------------------------------------------------------------------+")
print(">>>> 椭圆曲线参数：y^3 = x^2 + ax + b")
print("p  = ", hex(SM2_ECC.sm2_p)[2:])
print("n  = ", hex(SM2_ECC.sm2_n)[2:])
print("a  = ", hex(SM2_ECC.sm2_a)[2:])
print("b  = ", hex(SM2_ECC.sm2_b)[2:])
print("xG = ", hex(SM2_ECC.sm2_xG)[2:])
print("yG = ", hex(SM2_ECC.sm2_yG)[2:])
print("+---------------------------------------------------------------------------------------------+")
print(">>>> 消息数据：")
print("[+] 用户标识符:", user_id)
print("[+] 消息:", msg)
print("+---------------------------------------------------------------------------------------------+")
print(">>>> 密钥信息：")
server_privKey, server_pubKey = sm2KeyGen()
print("私钥：", hex(server_privKey)[2:])
print("公钥:")
print("   x = ", hex(server_pubKey.xG)[2:])
print("   y = ", hex(server_pubKey.yG)[2:])
r, s = sm2_sign(user_id, msg, server_privKey, server_pubKey)
print("+---------------------------------------------------------------------------------------------+")
print(">>>> 签名结果：")
print("  r = ", b2a_base64(r).decode().strip())
print("  s = ", b2a_base64(s).decode().strip())
print("+---------------------------------------------------------------------------------------------+")
print(">>>> 验签结果：")
print("  是否有效： ", sm2_verify(user_id, msg, (r, s), server_pubKey))
print("+---------------------------------------------------------------------------------------------+")
print(">>>> 混淆某位：")
i = random.randint(0, len(r) - 1)
noise = random.choice([0b1, 0b10, 0b100, 0b1000, 0b10000, 0b100000, 0b1000000, 0b1000000])
r1 = b""
for j in range(len(r)):
    if j != i:
        r1 += r[j].to_bytes(1, byteorder="big")
    else:
        r1 += (r[j]^noise).to_bytes(1, byteorder="big")
print("  r = ", b2a_base64(r1).decode().strip())
print("  s = ", b2a_base64(s).decode().strip())
print(">>>> 验签结果：")
print("  是否有效： ", sm2_verify(user_id, msg, (r1, s), server_pubKey))
print("+---------------------------------------------------------------------------------------------+")
