#!/bin/bash

export MYPYTHON=/afs/cern.ch/work/c/camontan/public/miniconda3

source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev4cuda9/latest/x86_64-centos7-gcc62-opt/setup.sh
unset PYTHONHOME
unset PYTHONPATH
source $MYPYTHON/bin/activate
export PATH=$MYPYTHON/bin:$PATH

which python

mkdir data
mkdir img

echo $1
echo $2

python3 henon_4d_general_run.py basic $1 $2 500 polar 10000000 1e-10 1e-11 10 100000 49 100 1e-12 subbasic 0 1 0 1 0 0 -outdir /afs/cern.ch/work/c/camontan/public/dynamic_indicator_analysis/data