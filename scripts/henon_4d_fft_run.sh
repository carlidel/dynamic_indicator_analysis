#!/bin/bash

export EOS_MGM_URL=root://eosuser.cern.ch
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

python3 henon_4d_fft_run.py basic $1 $2 500 polar 10 14 subbasic 0 1 0 1 0 0 -outdir ./data

eos cp data/* /eos/project/d/da-and-diffusion-studies/DA_Studies/Simulations/Models/dynamic_indicator_analysis/dynamic_indicator_analysis/data