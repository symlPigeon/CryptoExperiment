from sm2_1SignFunc import sm2DigitSignFunc, sm2DigitVerifyFunc, calcZ_A

def sm2_sign(uid: str, msg: bytes, privKey, pubKey):
    Z_A = calcZ_A(uid, pubKey)
    return sm2DigitSignFunc(Z_A, msg, privKey)


def sm2_verify(uid: str, msg: bytes, sign, pubKey):
    Z_A = calcZ_A(uid, pubKey)
    return sm2DigitVerifyFunc(msg, sign, Z_A, pubKey)