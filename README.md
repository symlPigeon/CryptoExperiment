# CryptoExperiment

## 第一次实验
Fermat素性检测
程序`./Fermat_Primality_Test/Fermat.py`

## 第二次实验
中国剩余定理
程序`./CRT/CRT.py`

## 第三次实验
基于CRT门限的秘密共享方案
程序`./CRT_based_secret_share/sec_share.py`
`sec_gen.py`用于生成共享的秘密文件进行测试

## 第四次实验
Elgamal密码算法
`./ElGamal/Elgamal.py`

## 大作业
SM2公钥密码算法
`./SM2/`
```
- ECCgen.py                 椭圆曲线参数生成
- func.py                   SM2、SM3算法中的一些函数，主要是格式转换等  
- sm2_1SignFunc.py          SM2-1椭圆曲线数字签名算法函数
- sm2_2keyExchangeFunc.py   SM2-2椭圆曲线密钥交换算法函数
- sm2_3EncDecFunc.py        SM2-3椭圆曲线加密解密算法函数
- sm2digitSign.py           SM2-1函数的封装
- sm2KDF.py                 SM2密钥派生函数
- sm2keygen.py              SM2公私钥生成和验证
- sm2math.py                SM2中的数论算法
- sm2point.py               SM2参数定义和椭圆曲线点运算
- sm2TestDecEnc.py          SM2-3加密解密测试
- sm2TestKeyExchangeClient.py SM2-2密钥交换客户端测试
- sm2TestKeyExchangeServer.py SM2-2密钥交换服务端测试
- sm2TestSign.py            SM2-1签名算法测试
- sm3.py                    SM3算法实现
- test_sm3.py               SM3算法测试
``` 