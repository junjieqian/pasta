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

#sudo operf fio --name=1 --bs=4k --ioengine=libaio --iodepth=1 --size=10g \
#         --percentage_random=100 --rwmixread=100 --numjobs=256 \
#	 --filename=/dev/nvme0n1 --group_reporting --thread

sudo operf fio --name=1 --bs=1m --ioengine=libaio --iodepth=32 --size=100g --rw=read --direct=1 --filename=/dev/nvme0n1 --numjobs=$1

sudo opreport -l

