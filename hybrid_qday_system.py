from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import hashlib
import time


def generate_rsa_keys():
    print("[*] Generating RSA keys...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key


def rsa_encrypt(public_key, secret):
    ciphertext = public_key.encrypt(
        secret,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


# ---------------------------
# Kyber Simulation (IMPORTANT FIX)
# ---------------------------
def kyber_exchange():
    print("[*] Running Kyber simulation (Post-Quantum placeholder)...")

    # simulate shared secret (same for both sides)
    secret = os.urandom(32)

    return secret, secret


# ---------------------------
# Create Hybrid Key
# ---------------------------
def create_session_key(rsa_secret, kyber_secret):
    combined = rsa_secret + kyber_secret
    return hashlib.sha256(combined).digest()


# ---------------------------
# AES Encryption
# ---------------------------
def aes_encrypt(key, message):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, message.encode(), None)
    return nonce, ciphertext


# ---------------------------
# AES Decryption
# ---------------------------
def aes_decrypt(key, nonce, ciphertext):
    aes = AESGCM(key)
    plaintext = aes.decrypt(nonce, ciphertext, None)
    return plaintext.decode()


# ---------------------------
# MAIN PROGRAM
# ---------------------------
def main():
    print("\n=== Hybrid RSA + Kyber Simulation + AES System ===\n")

    # ---------------- RSA ----------------
    rsa_private, rsa_public = generate_rsa_keys()

    rsa_secret = os.urandom(32)

    start_rsa = time.time()
    encrypted_rsa = rsa_encrypt(rsa_public, rsa_secret)
    decrypted_rsa = rsa_decrypt(rsa_private, encrypted_rsa)
    end_rsa = time.time()

    print("[+] RSA exchange done")
    print("RSA time:", end_rsa - start_rsa, "seconds")

    # ---------------- Kyber (Simulation) ----------------
    start_kyber = time.time()
    kyber_secret_1, kyber_secret_2 = kyber_exchange()
    end_kyber = time.time()

    print("[+] Kyber simulation done")
    print("Kyber time:", end_kyber - start_kyber, "seconds")

    # ---------------- Check ----------------
    if rsa_secret == decrypted_rsa:
        print("[+] RSA secret match OK")

    if kyber_secret_1 == kyber_secret_2:
        print("[+] Kyber secret match OK")

    # ---------------- Hybrid Key ----------------
    session_key = create_session_key(rsa_secret, kyber_secret_1)

    # ---------------- Message ----------------
    message = input("\nEnter message: ")

    # AES Encryption
    start_aes = time.time()
    nonce, encrypted = aes_encrypt(session_key, message)
    end_aes = time.time()

    # AES Decryption
    decrypted = aes_decrypt(session_key, nonce, encrypted)

    print("\n--- RESULTS ---")
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print("AES time:", end_aes - start_aes, "seconds")


# Run program
if __name__ == "__main__":
    main()