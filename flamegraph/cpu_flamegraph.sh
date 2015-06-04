#!/bin.bash

# More about flamegraph, refer to http://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html

flamegraph=~/flamegraph/FlameGraph

sudo ~/linux/tools/perf/perf record -F 99 -a -g -- fio --name=1 --bs=4k \
	--ioengine=libaio --iodepth=32 --size=100g --rw=read --direct=1 \
	--filename=/dev/nvme0n1:/dev/nvme1n1 --numjobs=$1

sudo ~/linux/tools/perf/perf script | $flamegraph/stackcollapse-perf.pl > out.perf-folded

$flamegraph/flamegraph.pl out.perf-folded > perf-kernel_"$1"_double.svg
