import random
import ecdsa.eddsa as eddsa


####################################################################################################
### This script represents the prototype of the EdDSA functionality in Zcash's "Sprout" protocol ###
####################################################################################################

# Wrapper class for a public key object
class PublicKey:
    def __init__(self, secret_key):
        self.privkey = secret_key.key
        self.pubkey = self.privkey.public_key()

    # Verification of an EdDSA signature
    def verify(self, message, signature):
        result = self.pubkey.verify(message, signature)
        return result

# Wrapper class for a private key object
class PrivateKey:
    def __init__(self):
        start = random.randbytes(32) # Generation of a random 256-bit private key
        self.key = eddsa.PrivateKey(eddsa.generator_ed25519, start) # Generation of a private key object

    # Creation of an EdDSA signature on a message
    def sign(self, message):
        signature = self.key.sign(message)
        return signature

# Generation of an EdDSA public and private key pair
def generateKeyPair():
    private = PrivateKey()
    public = PublicKey(private)
    return public, private

