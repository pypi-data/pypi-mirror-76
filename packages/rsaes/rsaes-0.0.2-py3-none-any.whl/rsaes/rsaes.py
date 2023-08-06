#by sidq
#telegram: @sidqdev
#pip install rsa
#pip install pycryptodomex

import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def aes_encrypt(data: bytes):
	key = get_random_bytes(32)
	cipher = AES.new(key, AES.MODE_EAX)
	nonce = cipher.nonce
	cipherdata, tag = cipher.encrypt_and_digest(data)

	return cipherdata, key + nonce

def aes_decrypt(cipherdata: bytes, key: bytes):
	key, nonce = key[:32], key[32:]
	cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaindata = cipher.decrypt(cipherdata)
	# try:
	# 	cipher.verify(tag)
	# 	print("The message is authentic:", plaintext)
	# except ValueError:
	# 	print("Key incorrect or message corrupted")
	return plaindata

def encrypt(data: bytes, pb):
	cipherdata, key = aes_encrypt(data)
	cipherkey = rsa.encrypt(key, pb)

	return cipherdata, cipherkey

def decrypt(cipherdata: bytes, cipherkey: bytes, pv):
	key = rsa.decrypt(cipherkey, pv)
	data = aes_decrypt(cipherdata, key)

	return data


# data = get_random_bytes(128)

# pb, pv = rsa.newkeys(512)

# cd, ck = encrypt(data, pb)

# print(cd, ck)

# d = decrypt(cd, ck, pv)

# print(d)