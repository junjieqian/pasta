#!/bin/bash

dev=/dev/nvme0n1
name=$dev
fio=/home/junjie/fio-master/fio

for size in '512' '1024' '2048'; do
  for iter in {1..3}; do
    for nums in 1 2 4 8 16 32 64 128 256 512 1024 2048; do
      sudo $fio --name=$size_"$nums"_"$iter" --output="$size"_"$nums"_"$iter" \
      --bs=$size --ioengine=libaio --iodepth=1 --size=16g --rw=read \
      --numjobs=$nums --filename=$dev --loops=3 --thread --direct=1 \
      --group_reporting
      sleep 10
    done
  done
done