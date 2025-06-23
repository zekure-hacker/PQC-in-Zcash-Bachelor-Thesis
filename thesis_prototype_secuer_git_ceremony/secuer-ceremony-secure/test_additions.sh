#!/bin/bash
# This is the execution script according to the CI pipeline stage "new_additions".

# Configuration of the access GitHub repository to initialize to the branch
# the pull request is based on.
cd SECUER_ceremony
git checkout $CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME
git pull

# Checks the correct amount of additions: either none for "no new curves and proofs to be added"
#                                         or 2 for "this curve and proofs should be added"
number_additions=$(ls c-impl/new_additions -1 | wc -l)
if [ $number_additions -ne 2 ] && [ $number_additions -ne 0 ]; then
  exit 1
fi

# Execution of the script contents should only be done when 2 new additions have been provided.
if [ $number_additions -eq 2 ]; then

  # Figuring out the correct denomination of the new additions.
  # e.g.    latest, verified curve/proof: "curve1.txt" and "proof0.txt"
  #     --> new additions should be labelled: "curve2.txt" and "proof1.txt"
  curve_additions=$(ls c-impl/new_additions | head -n1)
  proof_additions=$(ls c-impl/new_additions | tail -n1)
  next_index_proof=$(ls c-impl/proofs -1 | wc -l)
  current_index_curve=$(ls c-impl/curves -1 | wc -l)
  next_index_curve=$((current_index_curve + 1))
  next_proof="proof"$next_index_proof".txt"
  next_curve="curve"$next_index_curve".txt"

  # Checks the correctness of the denomination of the new additions
  if [ $proof_additions != $next_proof ]; then
    exit 1
  fi
  if [ $curve_additions != $next_curve ]; then
    exit 1
  fi

  # Checks if the provided curve file starts at the current "tip curve"
  tip_curve_name=$(ls c-impl/curves | tail -n1)
  addition_starting_curve=$(cat c-impl/new_additions/$curve_additions | head -n1)
  current_tip_curve=$(cat c-impl/curves/$tip_curve_name | tail -n1)
  if [ $addition_starting_curve != $current_tip_curve ]; then
    exit 1
  fi
fi