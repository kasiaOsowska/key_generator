from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from PendriveRecognition import pendrive_detection


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    print("klucze zostały wygenerowane")
    print("twój klucz publiczny to: " + str(public_key.public_numbers()))

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_private_key, pem_public_key


print("trwa generowanie kluczy")

pem_private_key, pem_public_key = generate_keys()
path_to_pendrive = pendrive_detection()

pin = input("podaj pin na podstawie którego zostanie zaszyfrowany klucz: ")

hasher = SHA256.new()
hasher.update(pin.encode())
key = hasher.digest()

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(pem_private_key, AES.block_size))

print("klucz został zaszyfrowany")
with open(path_to_pendrive + "encrypted_private_key.bin", "wb") as f:
    f.write(ciphertext)
with open(path_to_pendrive + "public_key.bin", "wb") as f:
    f.write(pem_public_key)
print("klucz został zapisany na pendrive")

