import hashlib
import base58
from ecdsa import SigningKey, SECP256k1

private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key().to_string()

private_key = private_key.to_string()

print("Private Key:", private_key.hex())
print("Public Key:", public_key.hex())
print(len(public_key.hex()))

sha256 = hashlib.sha256(public_key).digest()

ripemd160 = hashlib.new("ripemd160", sha256).digest()

versioned_payload = b'\x00' + ripemd160

checksum = hashlib.sha256(
    hashlib.sha256(versioned_payload).digest()
).digest()[:4]

final_data = versioned_payload + checksum

bitcoin_address = base58.b58encode(final_data).decode()

print("\nBitcoin Address:", bitcoin_address)