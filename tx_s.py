import hashlib
import json
import socket
from ecdsa import SECP256k1, SigningKey

def start_sender(host="127.0.0.1", port=65432):
    # 1. Generate keys
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()

    msg = "Alice sends 10 BTC to Bob"
    encrypted_hash = sk.sign(msg.encode(), hashfunc=hashlib.sha256)

    payload = {
        "message": "Alice sends 10 BTC to Bob",
        "encrypted_hash": encrypted_hash.hex(),
        "public_key": vk.to_string().hex(),
    }

    with socket.create_connection((host, port)) as client:
        print(f"[SENDER] Original Message: '{msg}'")
        client.sendall(json.dumps(payload).encode())

        response = client.recv(1024).decode()
        print(f"[SENDER] Server Status  : {response}")

if __name__ == "__main__":
    start_sender()