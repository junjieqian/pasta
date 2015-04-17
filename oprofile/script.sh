#!/bin/bash
# Oprofile install auto
# sudo apt-get install binutils-dev libpopt-dev git libiberty-dev -y
#
# git clone git://git.code.sf.net/p/oprofile/oprofile ./oprofile
#
# cd ./oprofile
#
# bash autogen.sh
#
# ./configure && make && sudo make install
# Or: sudo apt-get install oprofile
sudo operf fio --name=1 --bs=4k --ioengine=libaio --iodepth=1 --size=1g --percentage_random=100 --rwmixread=100 --numjobs=4 --filename=/dev/nvme0n1 --group_reporting --thread
sudo opreport -l

