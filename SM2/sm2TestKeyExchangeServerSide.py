from sm2_2keyExchangeFunc import sm2KeyExchangeSideB
from sm2point import point
from sm2keygen import sm2KeyGen


uidB = "BILL456@YAHOO.COM"
privB, pubB = sm2KeyGen()

sm2KeyExchangeSideB(128, uidB, pubB, privB)