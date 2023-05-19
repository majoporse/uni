from functions import *
from cryptography.hazmat.primitives.asymmetric import rsa, dh
private_key = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDFYG6KRtxqSpyo
DXnPm1SkE4MorvETxxi2Gkn0nLKZZp7jwRvSCAXIaBR6h7t8LtUJx/SAIjFt1tnd
7PbcAplxtPByTG/bn3sySSb0ZcNP5r4azzr7a11E453CVBuHvpAz3piFCsOWdt7l
nHcsnwKmWpGQZ274lzFBCn4pHsabrhJTOgb/PWP/oZWyG9jaIowU7nDb6oPlj/NJ
NVQNmXXTGAF4Lcl+JAzUGpddqvhoOdi+hGtm31zokYZUxc09Y6NSL8zzg65ynr/F
uqv0u2XP+zyfQfL3lEaZlOqPynP6uW1Q0Lsf4xz9O3LBvQtkmz6OV33qZZHxcgPg
PWXTgUu7AgMBAAECggEBALJSX0xanQUDB+nk0uq4QY5Derok4/WkaTUNJ0fy0oE5
b9ABRetKCD95mRbizoZxoVPG7aVePx4ngIq6boVza8KJYLtDR8Q6oAlcge9IiV8E
7zg1hepko817f6p0ZrMLfij+sPlyMiccmmEELb+IodI9/UljyaSapItIuZbZEULQ
ORzy3Unos9PSEOGBlF7kEx2r8DRD8u6GSixGx++FMRvlRkFy3lQkuh10kiZvuegH
lj/yTH90Acjty1k9a5+581K5M84i0OKxSd03O+jHrObSIE84EZOd277x7vBSTomq
coowwK4gkla/mbhyJwv+dLiuiggROLXeMxRxBhzDdHECgYEA7uJgOTRfLBP33pF6
2qoCr2tnMDP39ZermIyChA2SVoZ2C7deyEQmISrmE7FKq3pAET4eMQRzYSwupLrh
dPped5xWt0vH8rsxB6hMF0qZdtcFGieclM5j1M8P0yCpPgxqQas2CLIfXWjQBLXr
83J4hZt4SNnyQFkAmF0fIjEOFG8CgYEA04S43Z9Co633OceYbsfuvLzm8WCz4DnF
+4U9bQ7EMu6yVBULbqtrztJhTMJkd4tC98fkU/1nNqC5yMd8OpjT/VmQG9LR0FMs
HoV8yrWeKQ2znZa/joRv0o7sw1+pxaFGnhb0Zi7F6rKU0DM/nY2LiCx06+6vuYEH
+w+2X95Z23UCgYBaXSnXGdeSne8as1+Mzdj8MJ21H0OCFKClsSlB+LxNnMmUvwXM
rfLagxbLhjpfyXvoyd2z3yIiNQtj5wmYLYmEp5AqADGfwW3XnrNB8EdDLC1S6n8R
z0z2WGl9DRLYVOvw8WocOf0hYZ+m2IZr7fZnXBtRO5im/MP73uYDEhloYwKBgDtZ
kVm2N0egJ6+RvsbO2MEirBZskOxIqbHSiBLSwuCbs3P+V6/c76ofw+d64B/e9pJ6
Byo9/zkHzjl1J/l1Kn57JAF6nR68R7PktshWP6O7UXvVcbh2lr3ZFrwXWpa2kw8G
19rYIvag1zq4NpBpyA4Uk1YkKjB98RRUK1MpG8OFAoGBAIDPhP9j4D3KdZKmmlxu
JKOW7GmQK7Kt/7VNuGWwbdsuBQiJ0u/yunhkBMrVX6/T8TCzNzvSF2eKFL4oxALU
Uc2W33FrewP6pspQXu8GAknyUNu1RpxlCfC2OaaWW4dO4jySP+vH4sTlD8YMViCc
NUU0T//8lnwzCWPEKqQLmQWm
-----END PRIVATE KEY-----"""

rsa_private = rsa_load_key(private_key)


####################AUTH_SERVER_START#########################

status_code, diffie_helman = send_get("/hw03/auth-server/api/dh")
assert(status_code == 200)


status_code , server_rsa_dict = send_get("/hw03/auth-server/api/rsa")
assert(status_code == 200)

server_rsa = rsa.RSAPublicNumbers(bytes_to_int(bytes.fromhex(server_rsa_dict["public_exponent_e"])), 
                                  bytes_to_int(bytes.fromhex(server_rsa_dict["modulus_n"]))).public_key()

from cryptography.hazmat.primitives.asymmetric import dh
g = hex_to_int(diffie_helman["generator"])
p = hex_to_int(diffie_helman["modulus_p"])

pn = dh.DHParameterNumbers(p, g)
parameters = pn.parameters()

private_dhk = parameters.generate_private_key()
dhk: bytes = int_to_bytes(private_dhk.public_key().public_numbers().y)
print(dhk)

signed_dhk: bytes = rsa_sign_pss_sha256(rsa_private, dhk)
status_code, data = send_post("/hw03/auth-server/api/kex", data={"payload": dhk.hex(), "signature": signed_dhk.hex(), "uco": 524805})

server_dhk: bytes = bytes.fromhex(data["payload"])
signature: bytes = bytes.fromhex(data["signature"])

assert(rsa_verify_pss_sha256(server_rsa, server_dhk, signature))

# compute shared key
from cryptography.hazmat.primitives import hashes
digest = hashes.Hash(hashes.SHA256())

public_server_dhk = dh.DHPublicNumbers(bytes_to_int(server_dhk), pn).public_key()

digest.update(private_dhk.exchange(public_server_dhk)) 
shared_key = digest.finalize()
# assert(len(shared_key) == 256)

#####################AUTH_SERVER_END##########################

##################DATABASE_SERVER_START#######################

status_code, data_rsa_dict = send_get("/hw03/database-server/api/rsa")
assert(status_code == 200)

data_mod = bytes.fromhex(data_rsa_dict["modulus_n"])
data_exp = bytes.fromhex(data_rsa_dict["public_exponent_e"])

data_rsa = rsa.RSAPublicNumbers(bytes_to_int(data_exp), bytes_to_int(data_mod)).public_key()

import secrets
mac_key = secrets.token_bytes(32)

aes_mac: bytes = aes_encrypt_cbc_pkcs7(shared_key, mac_key)
signed_mac: bytes = rsa_sign_pss_sha256(rsa_private, aes_mac)

status_code, stat_dict = send_post("/hw03/database-server/api/mac", data={"payload": aes_mac.hex(), "signature": signed_mac.hex(), "uco": 524805})
assert(status_code == 200)
assert(stat_dict["status"] == "OK")

#####################GIVE_POINTS_PART#########################
msg: bytes = b"Give 524805 3 p"
pl = aes_encrypt_cbc_pkcs7(shared_key, msg)
sg = rsa_sign_pss_sha256(rsa_private, pl)
mc = mac_create_aes_cbc(mac_key, int_to_bytes(524805))

status_code, msg = send_post("/hw03/database-server/api/points", data={"mac": mc.hex(),"payload": pl.hex(), "signature": sg.hex(), "uco": 524805})
assert(status_code == 200)

# check points
status, points = send_get("/hw03/database-server/api/points", params={"uco": 524805})
assert(status == 200)
print( "points = " + str(points["points"]))

# give 3 more points
def xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

new_msg = b"Give 445358 3 p"
new_msg_encrypted = bytes.fromhex("853da5754fac472acfc428f2256ed49bef80e6fbbeb594502f66a1b75943b188")

uco_pattern = xor(new_msg[5:11], new_msg_encrypted[5:11])
my_msg_encrypted = new_msg_encrypted[:5] + xor(uco_pattern, b"524805") + new_msg_encrypted[11:]
print(my_msg_encrypted.hex())


signature = rsa_sign_pss_sha256( rsa_private, my_msg_encrypted)
uco = 344
uco_bytes = int_to_bytes(uco)
uco_mac = bytes.fromhex("d156617b4d56535e79e4cdeae2c92c38")  # MAC of uco_bytes

padder = padding_symmetric.PKCS7(128).padder()
padded_uco_bytes = padder.update(uco_bytes) + padder.finalize()

pattern = xor(padded_uco_bytes, uco_mac)
my_uco_bytes = int_to_bytes(524805)

padder = padding_symmetric.PKCS7(128).padder()
my_padded_uco = padder.update(uco_bytes) + padder.finalize()

new_uco = xor(my_padded_uco, pattern)
print(new_uco.hex())

status_code, msg = send_post("/hw03/database-server/api/points", data={"mac": new_uco.hex(),"payload": my_msg_encrypted.hex(), "signature": signature.hex(), "uco": 344})
assert(status_code == 200)

status, points = send_get("/hw03/database-server/api/points", params={"uco": 524805})
assert(status == 200)
print( "points = " + str(points["points"]))