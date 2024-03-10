from cryptography.fernet import Fernet

key = b'n2iSJTx-w4LlTNbej2n_vXEAsBeIi_Ndq-vayEStOMM='
fernet = Fernet(key)

def encrypt(password: str) -> str:
    return fernet.encrypt(password.encode('utf-8')).decode('utf-8')

def decrypt(password_encrypted: str) -> str:
    return fernet.decrypt(password_encrypted.encode('utf-8')).decode('utf-8')