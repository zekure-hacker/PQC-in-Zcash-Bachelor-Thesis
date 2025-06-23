# Description
This repository represents the implementation and contribution for the sections "Transparent protocol" and
"Sprout protocol" in the Bachelor thesis "Post-Quantum-Cryptography: Security Evaluation and Migration Strategies".

The implementation is divided in three areas: Prototypes, Falcon library changes, ECDSA library changes.

We used "Python 3.13.2" and Visual Studio Code (plugins: Python and Pylance by Microsoft) for this implementation. The activation of the virtual environment, which is necessary for the execution,
can be looked up in the Python documentation (https://docs.python.org/3/tutorial/venv.html).

## Prototypes
We created prototypes to show the current functionality of the digital signatures "ECDSA" and "EdDSA"
in the respective Zcash protocols "Transparent" and "Sprout". These are compared with a almost equal
prototype using the Falcon (512-bit version) digital signature algorithm.

The Python script "test_function.py" can be executed to check if all the used functionality works correctly.

The Python scripts "test_compare_*.py" can be executed to benchmark the respective prototypes and their functions.

## Contributions
The following contributions were gathered alongside this project to rectify issues that would have
compromised the successful results of this project.

The current state of the contributions only aims for successful results. After polishing and customizing
them according to the original libraries, they will be documented, further tested and contributed
to the respective repositories.

### Falcon library
The included Falcon library "falcon" by Thomas Prest lacks a public key recovery mode.
Therefore, we implemented this mode based on the Falcon specification (https://falcon-sign.info/falcon.pdf). It can be found in "falcon/falcon.py".
The relevant functions which we implemented are:
    - sign_recoverable (line 395)
    - verify_recoverable (line 468)
    - recover (line 447)

### ECDSA library
The Falcon library uses SHAKE256 for hashing which is included in the PyCryptodome library (and also specified in the Falcon specification linked above).
We used the different XOF hash algorithms included in PyCryptodome (https://www.pycryptodome.org) to test the influence
of hashing on the performance of the Falcon implementation.
These algorithms were: SHAKE256, TurboSHAKE, cSHAKE, KangarooTwelve.

For meaningful comparison, we also needed to use them in the ECDSA and EdDSA libary "python-ecdsa" but
it does usually not accomodate these algorithms. Hence, we included them into the functionality of
the library. They can be found in "thesis_implementations/.venv/lib/python3.13/site-packages/ecdsa/keys.py" in the lines 6, 459, 692 and 1549.

# Setup
The virtual environment with the necessary libraries should be included in the parent directory, labelled ".venv".
If it is not possible to execute the scripts because of missing libraries, execute the following commands:
python3 -m venv .venv (Mac/Linux) or python -m venv .venv (Windows)
pip install ecdsa (before pip has to be installed!)
pip install pycryptodome
pip install numpy