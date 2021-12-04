from sm2_2keyExchangeFunc import sm2KeyExchangeSideA
from sm2point import point
from sm2keygen import sm2KeyGen


uidA = "ALICE123@YAHOO.COM"
privA, pubA = sm2KeyGen()

sm2KeyExchangeSideA(128, uidA, pubA, privA)