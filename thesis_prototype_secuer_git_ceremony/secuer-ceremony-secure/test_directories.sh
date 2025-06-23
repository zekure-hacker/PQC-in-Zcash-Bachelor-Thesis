#!/bin/bash
# This is the execution script according to the CI pipeline stage "structure".

# Configuration of the access GitHub repository to initialize to the branch
# the pull request is based on.
cd SECUER_ceremony
git checkout $CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME
git pull

# Execution of the script contents should only be done when 2 new additions have been provided.
number_additions=$(ls c-impl/new_additions -1 | wc -l)
if [ $number_additions -eq 2 ]; then

  # Check the existence of the necessary directories
  if [ ! -e "c-impl/curves" ]; then
    exit 1
  fi
  if [ ! -e "c-impl/proofs" ]; then
    exit 1
  fi
  if [ ! -e "c-impl/new_additions" ]; then
    exit 1
  fi

  # Saves the hash on the "verified" curves and proofs according to the pull request
  hash_curves_input=$(sha256sum c-impl/curves/* | sha256sum | head -c64)
  hash_proofs_input=$(sha256sum c-impl/proofs/* | sha256sum | head -c64)

  # Saves the reference hash of the verified curves and proofs according to the main branch.
  cd ..
  hash_curves_reference=$(cat secuer-ceremony-secure/hashes/curves.txt)
  hash_proofs_reference=$(cat secuer-ceremony-secure/hashes/proofs.txt)

  # Compares the hashes of the pull request and the main branch
  if [ ! $hash_curves_input = $hash_curves_reference ]; then
    exit 2
  fi
  if [ ! $hash_proofs_input = $hash_proofs_reference ]; then
    exit 3
  fi
fi