#!/usr/bin/env python

# logreader for non group_reporting logs

import string
import os
import sys
import csv

class threadreader:
  _workload = {}
  _perf_path = ""
  _iostat_path = ""
  _workload_filename = ""
  _blocksize = ""

  def __init__(self, workload_filename, perf_path, iostat_path):
    # @param workload_filename, the defination of the workload run
    # @param perf_path, the fio log files
    # @param iostat_path, the io stat files
    self._perf_path = perf_path
    self._iostat_path = iostat_path
    self._workload_filename = workload_filename
    with open(self._workload_filename, 'rU') as csvreader:
      workloads = csv.reader(csvreader, delimiter=',', quotechar='|')
      for row in workloads:
        if "Test id" in row:
          continue
        else:
          _testnum = row[0]
          _filesize = row[1]
          self._blocksize = row[2]
          _patern = row[3]
          _access_list = _patern.split()
          _runtime = row[4]
          _ramptime = row[5]
          _startdelay = row[6]
          _workers = row[7]
          _iodepth = row[8]
          _device_num = len(row[9].split(":"))
          self._workload[_testnum] = row[1:2]
          self._workload[_testnum].append(_access_list)
          self._workload[_testnum].append(row[4:8])
          self._workload[_testnum].append(str(_device_num))

  def perf_read(self):
    if not os.path.isdir(self._perf_path):
      return
    ret = csv.writer(open("fiolog_threads.csv", "wb"))
    ret.writerow(["testnum", "iops", "disk utilization", "average bandwidth", "thread time"])
    for roots, dirs, files in os.walk(self._perf_path):
      files.sort(key=lambda x:int(x.split('.')[0]))
      for f in [os.path.join(roots, fs) for fs in files]:
        fp = open(f)
        count = 0
        _iops = 0.0
        _throughput = 0.0
        _disk_utilization = 0.0
        _cpu_user = 0.0
        _cpu_system = 0.0
        _context_switches = 0.0
        _average_bandwidth = 0.0
        _write_submission_latency = 0.0
        _write_completion_latency = 0.0
        _read_submission_latency = 0.0
        _read_completion_latency = 0.0
        _dev_id1 = -1
        _runtime = []
	for line in fp:
          if not "fio-2.1.3" in line:
            continue
          word = line.split(";")
          _dev_id1 = word.index("nvme0n1")
          count += 1
          _runtime.append(float(word[8]) + float(word[49])) # msec, the runtime for one thread
          _testnum = word[2]
          _iops += (float(word[7]) + float(word[48]))/2.0
          _throughput += _iops * int(self._blocksize.split('K')[0])
          if line.find("nvme1n1") < 0:
            _disk_utilization += float(word[-1].split('\n')[0].strip('%'))
          else:
            if line.find("nvme2n1") < 0:
              _disk_utilization += (float(word[_dev_id1 + 8].strip('%')) + float(word[_dev_id1 + 17].split('\n')[0].strip('%')))/2.0
            else:
              _disk_utilization += (float(word[_dev_id1 + 8].strip('%')) + float(word[_dev_id1 + 17].strip('%')) + float(word[_dev_id1 + 26].strip('%')) + float(word[_dev_id1 + 35].split('\n')[0].strip('%')))/4.0
          _cpu_user += float(word[87].strip('%'))
          _cpu_system += float(word[88].strip('%'))
          _context_switches += float(word[89])
          _average_bandwidth += (int(word[6])+int(word[47]))/2.0
          _write_submission_latency += float(word[52])
          _write_completion_latency += float(word[56])
          _read_submission_latency  += float(word[11])
          _read_completion_latency  += float(word[15])
    ret.writerow([_testnum, str(_iops/count), str(_disk_utilization/count), str(_average_bandwidth/count)] + _runtime)
    fp.close()
