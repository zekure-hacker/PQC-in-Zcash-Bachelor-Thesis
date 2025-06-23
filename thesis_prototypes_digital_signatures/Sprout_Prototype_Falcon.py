from falcon import falcon
###############################################################################################################
### This script represents the prototype of the potential Falcon functionality in Zcash's "Sprout" protocol ###
###############################################################################################################

# Wrapper class for a public key object
class PublicKey:
    def __init__(self, secret_key):
        self.privkey = secret_key.key
        self.pubkey = secret_key.key.h

    # Verification of an Falcon signature
    def verify(self, message, signature):
        result = self.privkey.verify(message, signature)
        return result

# Wrapper class for a private key object
class PrivateKey:
    def __init__(self, n, polys=None):
        self.key = falcon.SecretKey(n, polys)

    # Creation of a Falcon signature on a message
    def sign(self, message):
        signature = self.key.sign(message)
        return signature

# Generation of a Falcon public and private key pair
def generateKeyPair(n, polys=None):
    private = PrivateKey(n, polys)
    public = PublicKey(private)
    return public, private

