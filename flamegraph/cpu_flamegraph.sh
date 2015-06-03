#!/bin.bash

# More about flamegraph, refer to http://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html

flamegraph=~/flamegraph/FlameGraph

sudo ~/linux/tools/perf/perf record -F 99 -a -g -- fio --name=1 --bs=1m --ioengine=libaio --iodepth=32 --size=100g --rw=read --direct=1 --filename=$1 --numjobs=$2

sudo ~/linux/tools/perf/perf script | $flamegraph/stackcollapse-perf.pl > out.perf-folded

$flamegraph/flamegraph.pl out.perf-folded > perf-kernel_$1_$2.svg
