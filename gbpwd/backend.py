import hashlib
import base64
import math

from Crypto.Protocol import KDF
from Crypto.Hash import SHA256


class Generator:

    def __init__(self, token, password, binary, lenght):
        self.token = token
        self.password = password
        self.binary = binary
        self.lenght = lenght

    def password_encode(self):
        data = bytes(self.password) + self.binary
        
        data = SHA256.new(base64.b64encode(data)).digest()

        return data

    def derive(self):
        return self._derive(self.password_encode(), self.token)[0:self.lenght-3] + '1A_'


class ScryptGen(Generator):

    def _derive(self, mkey, token):
        kdf = KDF.scrypt

        data = kdf(mkey, token, 32, 2**18, 8, 1)

        return base64.b64encode(data).decode()

class PBKDF2Gen(Generator):

    def _derive(self, mkey, token):
        kdf = KDF.PBKDF2

        data = kdf(mkey, token, count=2*10**6)

        return base64.b64encode(data).decode()


class PasswordChecker:

    def __init__(self, password):
        self.password = password
    
    def check(self):
        return math.log(self._unique_char()**len(self.password), 2)
    
    def _unique_char(self):
        chars = set()

        for c in self.password:
            chars.add(c)
        
        return len(chars)