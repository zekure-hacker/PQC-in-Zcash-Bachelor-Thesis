from time import perf_counter_ns
from decimal import Decimal, ROUND_FLOOR
from Sprout_Prototype_EdDSA import PublicKey, PrivateKey, generateKeyPair

###############################################################################
### This script benchmarks the functionality of "Sprout_Protoype_EdDSA.py". ###
###############################################################################


def test_generateKeyPair():
    start = perf_counter_ns()
    keys = generateKeyPair()
    end = perf_counter_ns()
    return end - start

def test_sign(keypair):
    private_key = keypair[1]
    start = perf_counter_ns()
    signature = private_key.sign(b"Hello World!")
    end = perf_counter_ns()
    return end - start

def test_verify(keypair):
    public_key = keypair[0]
    private_key = keypair[1]
    signature = private_key.sign(b"Hello World!")
    start = perf_counter_ns()
    result = public_key.verify(b"Hello World!", signature)
    end = perf_counter_ns()
    return end - start

if __name__ == "__main__":
    keypair_generation_time = 0
    for i in range(0,100):
        keypair_generation_time += test_generateKeyPair()
    keypair_generation_time = keypair_generation_time / (100 * 1000)
    print("test_generateKeyPair(): ",
          float(Decimal(str(keypair_generation_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    sign_time = 0
    for i in range(0,100):
        sign_time += test_sign(generateKeyPair())
    sign_time = sign_time / (100 * 1000)
    print("test_sign(): ",
          float(Decimal(str(sign_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    verify_time = 0
    for i in range(0, 100):
        verify_time += test_verify(generateKeyPair())
    verify_time = verify_time / (100 * 1000)
    print("test_verify(): ",
          float(Decimal(str(verify_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")






