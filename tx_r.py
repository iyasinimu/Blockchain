import hashlib
import json
import socket
from ecdsa import SECP256k1, BadSignatureError, VerifyingKey


def start_receiver(host="127.0.0.1", port=65432):
    server = socket.create_server((host, port))
    print(f"[RECEIVER] Listening on {host}:{port}...")

    conn, addr = server.accept()
    payload = json.loads(conn.recv(4096).decode())

    msg = payload["message"]
    encrypted_hash = payload["encrypted_hash"]
    pk_hex = payload["public_key"]

    received_msg_hash = hashlib.sha256(msg.encode()).hexdigest()
    print(f"[RECEIVER] Message received : '{msg}'")
    print(f"[RECEIVER] Calculated SHA-256: {received_msg_hash}")

    try:
        vk = VerifyingKey.from_string(bytes.fromhex(pk_hex), curve=SECP256k1)
        vk.verify(bytes.fromhex(encrypted_hash), msg.encode(), hashfunc=hashlib.sha256)

        print("[VERIFICATION] SUCCESS: Decrypted signature matches calculated hash!")
        conn.sendall(b"SUCCESS: Hashes match")
    except BadSignatureError:
        print("[VERIFICATION] FAILED: Decrypted signature does NOT match message!")
        conn.sendall(b"ERROR: Verification failed")

    conn.close()
    server.close()

if __name__ == "__main__":
    start_receiver()