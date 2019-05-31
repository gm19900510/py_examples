# -*- coding: utf-8 -*-
import rsa

# 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
'''
(pubkey, privkey) = rsa.newkeys(1024)

pub = pubkey.save_pkcs1()
pubfile = open('public.pem', 'wb')
pubfile.write(pub)
pubfile.close()

pri = privkey.save_pkcs1()
prifile = open('private.pem', 'wb')
prifile.write(pri)
prifile.close()
'''
# load公钥和密钥
message = 'lovesoo.org'
with open('public.pem', "rb") as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    print(pubkey)
with open('private.pem', "rb") as privatefile:
    p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)
    print(privkey)
# 用公钥加密、再用私钥解密
crypto = rsa.encrypt(message.encrsaTest('utf-8'), pubkey)
print(crypto)
message = rsa.decrypt(crypto, privkey)
message = message.decode('utf-8')
print (message)

# sign 用私钥签名认证、再用公钥验证签名
signature = rsa.sign(message.encode('utf-8'), privkey, 'SHA-1')
print(signature)
method_name = rsa.verify('lovesoo.org'.encode('utf-8'), signature, pubkey)
print(method_name)