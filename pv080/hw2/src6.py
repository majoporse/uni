
text1 = bytes.fromhex('8e549800e24e61222ff57e3a7d0e2e401b8bf5f429be64952075125c02393dba805ecd46ec4e63672ebb6324280767470081b5da29be64952075125c02393dba83538800e0546b6b39fe646b780e61441881fb9948d501bb2075125c02393dba844b8841e8556a657aee676b61182e5d1994b4865ddf0ae10e75125c02393dba83538852e61c65703fbb642e6918615a07c4b29a09d20df3455b125c02393dba924d8852fa536a677af2646b694b625d0090b79109dd16f45a0c3c5c02393dba90548900e25277753fe9646b690762141b91a9d459cc05ec4507617202393dba8354cd41f057246b29bb632428097c51158ffb8041db44e650107e302c393dba9453824ff0556a657af77e2d6d4b67475485b78348c717b54d10612f7b173dba96578100ec5a246128fe763f61046014168bac8709dc01f34f07777c6f5c13ba')
texts = []
dblock_size = 32


for i in range(10):
    texts.append(text1[i*dblock_size : (i+1) * dblock_size])
    print(texts[i].hex())

##printing function to help with guessing the words
def print_(bytes_):
    for b in bytes_:
        if(ord('a') <= b <= ord('z') or ord('A') <= b <= ord('Z') or b == ord(' ') or b == ord('.')):
            print(chr(b), end="   ")
        else:
            if b >= 0x10:
                print(hex(b), end="")
            else:
                print(hex(b), end=" ")
        print("`",end="")
    print()
    
# xor function for bytes

def encrypt1(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

ends = texts[:]

# represents what ciphertext values map to words
_E = [(b'\xbA', b'\x00'), 
      (b'\x3d', b'\x00'),
      (b'\x39', b'\x00'),
      (b'\x02', b'\x00'),
      (b'\x5c', b'\x00'),
      (b'\x12', b'\x00'),
      (b'\x75', b'\x00'),
      (b'\x20', b'\x00'),
      (b'\x95', b'\x00'),
      (b'\x64', b'\x00'),
      (b'\xbe', b'\x00'),
      (b'\x29', b'\x00'),
      (b'\x86', b'r'),
      (b'\xb4', b'o'),
      (b'\x94', b'p'),
      (b'\x19', b'm'),
      (b'\x5d', b'i'),
      (b'.', b' '),
      (b'\x0e', b'e'),
      (b'x', b'p'),
      (b'k', b' '),
      (b'd', b's'),
      (b'\xf5', b'n'),
      (b'\x2f', b'u'),
      (b'a', b'c'),
      (b'c', b'g'),
      (b'R', b'n'),
      (b'\xe2', b'a'),
      (b'F', b'f'),
      (b'\x81', b'l'),
      (b'M', b'v'),
      (b'\x92', b'E'),]
_key =  b'\x00' * (32 - len(_E))

# with xor-ing the values from _E we get the "keystream" 
cnonce = _key + bytes(a[0] ^ b[0] for a, b in reversed(_E))

for i in range(10):
    ends[i] = encrypt1(texts[i], cnonce)
    print_(texts[i])
    print_(ends[i])
    print()

val = bytes.fromhex('71f258f59dc897219ade35df182886dde9fab4e343a25b710bcfa1e05cf105be')

key = encrypt1(val, cnonce)
print(key.hex())
print()

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

cipher = Cipher(algorithms.AES(key), modes.ECB())

decryptor = cipher.decryptor()
enc = cipher.encryptor()

# decrypt the keystream with ecb mode to obtain nonce
nonce = decryptor.update(cnonce) + decryptor.finalize()
# print(cnonce)
a = nonce[:16]
b = nonce[16:]
# print(a)
# print(b)
c = Cipher(algorithms.AES(key), modes.CTR(nonce[:16]))
encryptor = c.encryptor()

# encrypt data with the correct counter
res = [ encryptor.update(ends[i]) for i in range(10)]
for i in range(10):
    print(res[i].hex())
