from sm2KDF import KDF
from sm2point import point, infintyPoint, point_add, point_mul, SM2_ECC, bytes2point
from sm2_1SignFunc import calcZ_A
from func import long_to_bytes, bytes_to_long
import socket
import random
import math


def sm2KeyExchangeSideA(keylen: int, uid: str, pubKey: point, privKey: int, ecc=SM2_ECC):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8888))
    print("[DEBUG] connecting to localhost:8888")

    w = round(round(math.log2(ecc.sm2_n)) / 2) - 1

    # 获得公钥，不算在密钥交换的环节里面
    PA_bytes = pubKey.toUnompressedBytes()
    s.send(PA_bytes)
    PB = bytes2point(s.recv(1024), p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
    print("[DEBUG] Server pubKey: (", hex(PB.xG), ",", hex(PB.yG), ")")
    s.send(uid.encode())
    B_uid = s.recv(1024)
    print("[DEBUG] Server UID: ", B_uid.decode())
    
    rA = random.randint(1, ecc.sm2_n - 1)
    rA = 0x83A2C9C8B96E5AF70BD480B472409A9A327257F1EBB73F5B073354B248668563
    RA = point_mul(ecc.sm2_G, rA, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
    print("[DEBUG] RA(",hex(RA.xG),",", hex(RA.yG), ")")
    RA_bytes = RA.toUnompressedBytes()
    s.send(RA_bytes)

    x1 = RA.xG
    x1_ = (pow(2, w, ecc.sm2_n) + (x1 & (pow(2, w, ecc.sm2_n) - 1))) % ecc.sm2_n
    tA = (privKey + x1_ * rA) % ecc.sm2_n
    print("[DEBUG] tA", hex(tA))
    RB = bytes2point(s.recv(1024), p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
    x2 = RB.xG
    print("[DEBUG] x2", hex(x2))
    x2_ = (pow(2, w, ecc.sm2_n) + (x2 & (pow(2, w, ecc.sm2_n) - 1))) % ecc.sm2_n
    print("[DEBUG] x2_", hex(x2_))
    try:
        RB.verify()
        pass
    except:
        print("Invalid RA!")
        conn.close()
        return
    U = point_mul(
                point_add(
                    PB, 
                    point_mul(RB, x2_, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b), 
                    p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b
                ),
                1 * tA, # h 余因子，取1 ？？？
                p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b
            )
    if type(U) == infintyPoint:
        print("Invalid V! Key exchange failed!")
        conn.close()
        return
    xU = long_to_bytes(U.xG)
    yU = long_to_bytes(U.yG)
    K_A = KDF(xU + yU + calcZ_A(uid, pubKey, ecc=ecc) + calcZ_A(B_uid.decode(), PB, ecc=ecc), klen=keylen)
    print("------------------------------")
    print("Session Key: ", hex(bytes_to_long(K_A))[2:])



def sm2KeyExchangeSideB(keylen: int, uid: str, pubKey:point, privKey: int, ecc=SM2_ECC):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 8888))
    print("[DEBUG] Starting Servering...")

    w = round(round(math.log2(ecc.sm2_n)) / 2) - 1

    s.listen(1)
    while True:
        print("[DEBUG] Waiting for connection...")
        conn, addr = s.accept()
        print("[DEBUG] Connecting from {}".format(addr))
        # 获得公钥，不算在密钥交换的环节里面
        PA = bytes2point(conn.recv(1024), p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
        print("[DEBUG] Client pubKey: (", hex(PA.xG), ",", hex(PA.yG), ")")
        PB_bytes = pubKey.toUnompressedBytes()
        conn.send(PB_bytes)
        A_uid = conn.recv(1024)
        conn.send(uid.encode())
        print("[DEBUG] Client UID", A_uid.decode())

        RA = bytes2point(conn.recv(1024), p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
        print("[DEBUG] RA :({} ,{})".format(hex(RA.xG), hex(RA.yG)))
        rB = random.randint(1, ecc.sm2_n - 1)
        rB = 0x33FE21940342161C55619C4A0C060293D543C80AF19748CE176D83477DE71C80
        RB = point_mul(ecc.sm2_G, rB, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b)
        print("[DEBUG] RB", hex(RB.xG), hex(RB.yG))
        x2 = RB.xG
        print("[DEBUG] x2", hex(x2))
        x2_ = (pow(2, w, ecc.sm2_n) + (x2 & (pow(2, w, ecc.sm2_n) - 1))) % ecc.sm2_n
        print("[DEBUG] x2_", hex(x2_))
        tB = (privKey + x2_ * rB) % ecc.sm2_n
        print("[DEBUG] tB", hex(tB))
        try:
            RA.verify()
        except:
            print("Invalid RA!")
            conn.close()
            return
        x1 = RA.xG
        print("[DEBUG] x1", hex(x1))
        x1_ = (pow(2, w, ecc.sm2_n) + (x1 & (pow(2, w, ecc.sm2_n) - 1))) % ecc.sm2_n
        print("[DEBUG] x1_", hex(x1_))
        V = point_mul(
                point_add(
                    PA, 
                    point_mul(RA, x1_, p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b), 
                    p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b
                ),
                1 * tB, # h 余因子，取1 ？？？
                p=ecc.sm2_p, a=ecc.sm2_a, b=ecc.sm2_b
            )
        if type(V) == infintyPoint:
            print("Invalid V! Key exchange failed!")
            conn.close()
            return
        print("[DEBUG] xV", hex(V.xG))
        print("[DEBUG] yV", hex(V.yG))
        xV = long_to_bytes(V.xG)
        yV = long_to_bytes(V.yG)
        K_B = KDF(xV + yV + calcZ_A(A_uid.decode(), PA, ecc=ecc) + calcZ_A(uid, pubKey, ecc=ecc), klen=keylen)
        conn.send(RB.toUnompressedBytes())
        print("-------------------------------")
        print("Session Key: ", hex(bytes_to_long(K_B))[2:])

