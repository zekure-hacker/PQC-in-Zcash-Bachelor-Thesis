#!/bin/bash
# This is the execution script according to the CI pipeline stage "verification".

# Configuration of the Gitlab repository for secure storage to initialize to the branch
# the pull request is based on.
cd secuer-ceremony-secure
git config --global user.email "hacker11@ads.uni-passau.de"
git config --global user.name "hacker"
git remote set-url origin https://oauth2:${AUTOMATION_ACCESS_TOKEN}@git.fim.uni-passau.de/hacker/secuer-ceremony-secure.git
cd ..

# Configuration of the access GitHub repository to initialize to the branch
# the pull request is based on.
cd SECUER_ceremony
git config --global user.email "hanneshacker1@gmail.com"
git config --global user.name "hacker"
git remote set-url origin https://oauth2:${ACCESS_GITHUB_TOKEN}@github.com/zekure-hacker/SECUER_ceremony.git
git checkout $CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME
git pull

# Saving necessary information about the new additions
curve_additions=$(ls c-impl/new_additions | head -n1)
proof_additions=$(ls c-impl/new_additions | tail -n1)
number_additions=$(ls c-impl/new_additions -1 | wc -l)
cd ..

# Execution of the script contents should only be done when 2 new additions have been provided.
if [ $number_additions -eq 2 ]; then

  # Building a reliable instance of the verification application
  cd secuer-ceremony-secure/c-impl
  make
  make test
  cd ../..

  # Verification of the provided proof
  ./secuer-ceremony-secure/c-impl/verify_434 < SECUER_ceremony/c-impl/new_additions/$proof_additions > secuer-ceremony-secure/testcurve.txt

  # Check if the provided curve file is equal to the result of the reliable verification
  input_file="SECUER_ceremony/c-impl/new_additions/$curve_additions"
  input_hash=$(sha256sum "$input_file" | head -c64)
  reference_file="secuer-ceremony-secure/testcurve.txt"
  reference_hash=$(sha256sum "$reference_file" | head -c64)
  rm secuer-ceremony-secure/testcurve.txt
  if [ ! $input_hash = $reference_hash ]; then
    exit 1
  fi

  # Add the verified additions to the respective directories.
  mv SECUER_ceremony/c-impl/new_additions/proof* SECUER_ceremony/c-impl/proofs
  mv SECUER_ceremony/c-impl/new_additions/curve* SECUER_ceremony/c-impl/curves

  # Update the reference hashes for the verified proofs and curves.
  cd SECUER_ceremony
  sha256sum c-impl/proofs/* | sha256sum | head -c64 > proofs.txt
  sha256sum c-impl/curves/* | sha256sum | head -c64 > curves.txt
  cd ..
  rm secuer-ceremony-secure/hashes/*
  ls secuer-ceremony-secure/hashes
  cd secuer-ceremony-secure
  touch hashes/proofs.txt
  touch hashes/curves.txt
  cat /builds/hacker/SECUER_ceremony_CICD2/SECUER_ceremony/proofs.txt > hashes/proofs.txt
  cat /builds/hacker/SECUER_ceremony_CICD2/SECUER_ceremony/curves.txt > hashes/curves.txt
  rm /builds/hacker/SECUER_ceremony_CICD2/SECUER_ceremony/proofs.txt
  rm /builds/hacker/SECUER_ceremony_CICD2/SECUER_ceremony/curves.txt

  # Pushing the new state of the Gitlab repository for secure storage.
  git add --all
  git commit -m "$curve_additions and $proof_additions have been successfully appended!"
  git push --all

  # Pushing the new state of the pull request's branch of the GitHub repository.
  cd ..
  cd SECUER_ceremony
  git add --all
  git commit -m "new_additions have been cleared!"
  git push -u origin $CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME

  # Merging the added, verified state of the GitHub repository to the main (default) branch.
  git checkout main
  git pull
  git merge $CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME
  git push -u origin main
fi