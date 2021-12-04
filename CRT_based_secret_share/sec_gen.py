# 生成测试明文

from Crypto.Util.number import getRandomInteger


for i in range(10):
    f = open(f"sec_{i}.txt", "w")
    f.write(str(getRandomInteger(512)))
    f.close()
