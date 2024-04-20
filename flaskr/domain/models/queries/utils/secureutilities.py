_SECRET_KEY_PATH = "application/security/rsa/encrypted_private_key.key"
_PUBLIC_KEY_PATH = "application/security/rsa/public_key.key"
_SECRET_PWD = "IAmBatman"

class SecurityConstants:

    def get_secret_key_path(self):
        return _SECRET_KEY_PATH
    
    def get_public_key_path(self):
        return _PUBLIC_KEY_PATH
    
    def get_secret(self):
        return _SECRET_PWD