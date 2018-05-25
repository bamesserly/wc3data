#!/bin/bash

ARCH=`uname`

CONDAENVNAME="W3AElo"
CONDAINSTALL=""
MINIDIR=""

if [[ $ARCH == "Darwin" ]]; then
  CONDAINSTALL=Miniconda2-latest-MacOSX-x86_64.sh
  MINIDIR="miniconda2"
else
  echo "Only configured for Mac OSX so far."
  exit 1
fi

#if [[ ! -d "$HOME/$MINIDIR" ]]; then
#  wget https://repo.continuum.io/miniconda/$CONDAINSTALL
#  bash $CONDAINSTALL -b -p $HOME/$MINIDIR
#fi
#
#export PATH="$HOME/$MINIDIR/bin:$PATH"

conda info --envs
conda remove --name $CONDAENVNAME --all
conda create -q -y -n $CONDAENVNAME python=2.7
. activate $CONDAENVNAME

conda install -q -y -c anaconda beautifulsoup4 
conda install -q -y -c conda-forge dropbox
conda install -q -y -c anaconda numpy
conda install -q -y -c anaconda dateutil 
