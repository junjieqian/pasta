#!/usr/bin/env python

import string
import os
import sys

class reader:
  _workload = {}
  _perf_path = ""
  _iostat_path = ""
  _workload_filename = ""

  def __init__(self, workload_filename, perf_path, iostat_path):
    self._perf_path = perf_path
    self._iostat_path = iostat_path
    self._workload_filename = workload_filename
    with open(self._workload_filename, 'rb') as csvreader:
      workloads = csv.reader(csvreader, delimiter=',', quotechar='|')
      for row in workloads:
        if "Test id" in row:
          continue
        else:
          _testnum = row[0]
          _filesize = row[1]
          _blocksize = row[2]
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
    for roots, dirs, files in os.path.walk(self._perf_path):
      for f in [os.join(roots, fs) for fs in files]:
        fp = open(f)
	for line in fp:
          word = line.split(";")
          _testnum = word[2]
	  _iops = word[7]
          _throughput = word[6]
          _disk_utilization = word[-1]
          _cpu_user = word[87]
          _cpu_system = word[88]
          _context_switches = word[89]
          _bandwidth = word[]
          _write_submission_latency = word[]
	  _write_completion_latency = word[]
	  _read_submission_latency  = word[]
	  _read_completion_latency  = word[]
        ret.writerow()
