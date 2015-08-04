#!/bin/bash

# node 0: 0 4 8 12 16 20 24 28
# node 1: 1 5 9 13 17 21 25 29
# node 2: 2 6 10 14 18 22 26 30
# node 3: 3 7 11 15 19 23 27 31

# single node
if [ ! -d "$PWD/single_node" ]; then
    mkdir $PWD/single_node
fi

cd $PWD/single_node
sudo python set_cpus.py 0,4,8,12,16,20,24,28
bash $PWD/run.sh

# two nodes
if [ ! -d "$PWD/two_nodes" ]; then
    mkdir $PWD/two_nodes
fi

cd $PWD/two_nodes
sudo python set_cpus.py 0,1,4,5,8,9,12,13,16,17,20,21,24,25,28,29
bash $PWD/run.sh