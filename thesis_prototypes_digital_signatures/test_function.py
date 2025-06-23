import Transparent_Prototype_ECDSA, Transparent_Prototype_Falcon, Sprout_Prototype_EdDSA

############################################################
### This script tests the functionality of all prototype ###
############################################################

# Testing of the ECDSA prototype - sign/verify are calling the same library function
# as sign_recoverable/verify_recoverable.
def test_ecdsa():
    keys = Transparent_Prototype_ECDSA.generateKeyPair()
    public_key = keys[0]
    private_key = keys[1]
    signature = private_key.sign(b"Hello World!")
    result = public_key.verify(b"Hello World!", signature)
    recovered_key = private_key.recover(b"Hello World!", signature)
    verify_recovered = (recovered_key[0] == public_key.pubkey) | (recovered_key[1] == public_key.pubkey)
    result = result & verify_recovered

    if result:
        print("ECDSA signing and verification process successful!")
    else:
        print("ECDSA signing and verification process unsuccessful!")

# Testing of the Falcon prototype
def test_falcon():
    keys = Transparent_Prototype_Falcon.generateKeyPair(512)
    public_key = keys[0]
    private_key = keys[1]

    # Testing classic sign/verify features
    signature = private_key.sign(b"Hello World!")
    result = public_key.verify(b"Hello World!", signature)

    # Testing the recoverable features
    signature = private_key.sign_recoverable(b"Hello World!")
    result = result & public_key.verify_recoverable(b"Hello World!", signature)
    recovered_key = private_key.recover(b"Hello World!", signature)
    verify_recovered = recovered_key == public_key.pubkey
    result = result & verify_recovered

    if result:
        print("Falcon signing and verification process successful!")
    else:
        print("Falcon signing and verification process unsuccessful!")

# Testing of the EdDSA prototype
def test_eddsa():
    keys = Sprout_Prototype_EdDSA.generateKeyPair()
    public_key = keys[0]
    private_key = keys[1]
    signature = private_key.sign(b"Hello World!")
    result = public_key.verify(b"Hello World!", signature)
    if result:
        print("EdDSA signing and verification process successful!")
    else:
        print("EdDSA signing and verification process unsuccessful!")


# Execution of all functionality tests which can be validated by the output in the console
if __name__ == "__main__":
    test_ecdsa()
    test_falcon()
    test_eddsa()