from time import perf_counter_ns
from decimal import Decimal, ROUND_FLOOR
from Transparent_Prototype_ECDSA import PublicKey, PrivateKey, generateKeyPair

#####################################################################################
### This script benchmarks the functionality of "Transparent_Prototype_ECDSA.py". ###
#####################################################################################

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

def test_sign_recoverable(keypair):
    private_key = keypair[1]
    start = perf_counter_ns()
    signature = private_key.sign_recoverable(b"Hello World!")
    end = perf_counter_ns()
    return end - start


def test_recover(keypair):
    private_key = keypair[1]
    signature = private_key.sign_recoverable(b"Hello World!")
    start = perf_counter_ns()
    public_key = private_key.recover(b"Hello World!", signature)
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

def test_verify_recoverable(keypair):
    public_key = keypair[0]
    private_key = keypair[1]
    signature = private_key.sign_recoverable(b"Hello World!")
    start = perf_counter_ns()
    result = public_key.verify_recoverable(b"Hello World!", signature)
    end = perf_counter_ns()
    return end - start


if __name__ == "__main__":
    keypair_generation_time = 0
    for i in range(0,100):
        keypair_generation_time += test_generateKeyPair()
    keypair_generation_time = keypair_generation_time / (10 * 1000)
    print("test_generateKeyPair(): ",
          float(Decimal(str(keypair_generation_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    sign_time = 0
    for i in range(0,100):
        sign_time += test_sign(generateKeyPair())
    sign_time = sign_time / (10 * 1000)
    print("test_sign(): ",
          float(Decimal(str(sign_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    sign_r_time = 0
    for i in range(0, 100):
        sign_r_time += test_sign_recoverable(generateKeyPair())
    sign_r_time = sign_r_time / (10 * 1000)
    print("test_sign_recoverable(): ",
          float(Decimal(str(sign_r_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    recover_time = 0
    for i in range(0, 100):
        recover_time += test_recover(generateKeyPair())
    recover_time = recover_time / (10 * 1000)
    print("test_recover(): ",
          float(Decimal(str(recover_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    verify_time = 0
    for i in range(0, 100):
        verify_time += test_verify(generateKeyPair())
    verify_time = verify_time / (10 * 1000)
    print("test_verify(): ",
          float(Decimal(str(verify_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")

    verify_r_time = 0
    for i in range(0, 100):
        verify_r_time += test_verify_recoverable(generateKeyPair())
    verify_r_time = verify_r_time / (10 * 1000)
    print("test_verify_recoverable(): ",
          float(Decimal(str(verify_r_time)).quantize(Decimal(".01"), rounding=ROUND_FLOOR)), " microseconds")








