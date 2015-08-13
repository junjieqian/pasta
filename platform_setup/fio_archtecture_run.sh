#!/bin/bash

# node 0: 0 4 8 12 16 20 24 28
# node 1: 1 5 9 13 17 21 25 29
# node 2: 2 6 10 14 18 22 26 30
# node 3: 3 7 11 15 19 23 27 31

dir=$PWD

# single node
if [ ! -d "$dir/single_node" ]; then
    mkdir $dir/single_node
fi

cd $dir/single_node
#sudo python set_cpus.py 0,4,8,12,16,20,24,28
sudo numactl -N 0 bash $dir/run.sh


# two nodes
if [ ! -d "$dir/two_nodes" ]; then
    mkdir $dir/two_nodes
fi

cd $dir/two_nodes
#sudo python set_cpus.py 0,1,4,5,8,9,12,13,16,17,20,21,24,25,28,29
sudo numactl -N 0,1 bash $dir/run.sh