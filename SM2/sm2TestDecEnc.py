from sm2_3EncDecFunc import sm2encrypt, sm2decrypt
from sm2keygen import sm2KeyGen
from sm2point import SM2_ECC
from binascii import b2a_base64


print(">>>> 椭圆曲线参数：y^3 = x^2 + ax + b")
print("p  = ", hex(SM2_ECC.sm2_p)[2:])
print("n  = ", hex(SM2_ECC.sm2_n)[2:])
print("a  = ", hex(SM2_ECC.sm2_a)[2:])
print("b  = ", hex(SM2_ECC.sm2_b)[2:])
print("xG = ", hex(SM2_ECC.sm2_xG)[2:])
print("yG = ", hex(SM2_ECC.sm2_yG)[2:])
privKey, pubKey = sm2KeyGen()
print("SM2 测试：")
print("公钥: ({}, {})".format(hex(pubKey.xG)[2:], hex(pubKey.yG)[2:]))
print("私钥: {}".format(hex(privKey)[2:]))
text = b"Are the fireflies brighter than usual, or is it just your imagination? Tonight will be a long night."
cipher = sm2encrypt(text, pubKey)
print("密文: {}".format(b2a_base64(cipher).decode()))
msg = sm2decrypt(cipher, len(text), privKey).decode()
print("解密结果：{}".format(msg))