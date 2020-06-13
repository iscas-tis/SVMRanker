#.! /usr/bin/env bash

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ $# -ne 2 ]] ; then
  echo "Usage $0 <c-file> <boogie-file>"
  echo $MYDIR
  exit -1
fi

CFILE=$1
BPL=$2

cpp $CFILE | grep -v '^#' | python3 $MYDIR/./c2boogie.py stdin $BPL --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants
