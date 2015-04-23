#!/usr/bin/env python

import string
import os
import sys
import csv

class reader:
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
    ret = csv.writer(open("fiolog.csv", "wb"))
    ret.writerow(["testnum", "throughput", "disk utilization", "average bandwidth", "iops"])
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
	for line in fp:
          if not "fio-2.1.3" in line:
            continue
          word = line.split(";")
          count += 1
          _testnum = word[2]
	  _iops += (float(word[7]) + float(word[48]))/2.0
          _throughput += _iops * int(self._blocksize.split('K')[0])
          _disk_utilization += float(word[-1].split('\n')[0].strip('%'))
          _cpu_user += float(word[87].strip('%'))
          _cpu_system += float(word[88].strip('%'))
          _context_switches += float(word[89])
          _average_bandwidth += (int(word[6])+int(word[47]))/2.0
          _write_submission_latency += float(word[52])
	  _write_completion_latency += float(word[56])
	  _read_submission_latency  += float(word[11])
	  _read_completion_latency  += float(word[15])
        ret.writerow([_testnum, str(_throughput/count), str(_disk_utilization/count), str(_average_bandwidth/count), str(_iops/count)])
      fp.close()

  def iostat_read(self):
    if not os.path.isdir(self._iostat_path):
      return
    ret = csv.writer(open("iostatlog.csv", "wb"))
    ret.writerow(["testnum", "software layer", "io wait"])
    # start time needs to be modified according to the system boot time
    # _boot_time format, [month, day, hour, minutes, seconds]
    _boot_time = [4, 15, 10, 25, 9]
    _cur_time  = [0, 0, 0, 0, 0]
    for roots, dirs, files in os.walk(self._iostat_path):
      _timestamp_flag = False
      _data_flag = False
      files.sort()
      for f in files:
        _testnum = f.split()[-1]
        fp = open(os.path.join(roots, f))
        _timestamp_flag = False
        _data_flag = False
        _before_flag = False
        _before_time = 0
        _after_time = 0
        _before_software_layer = 0.0
        _after_software_layer = 0.0
        _before_io_wait = 0.0
        _after_io_wait = 0.0
        for line in fp:
          if line.find("/2015")>=0 and not 'Linux' in line and not _timestamp_flag:
            _cur_time[0] = int(line.split()[0].split('/')[0])
            _cur_time[1] = int(line.split()[0].split('/')[1])
            _cur_time[2] = (int(line.split()[1].split(':')[0]) + 12) if "PM" in line.split()[2] else int(line.split()[1].split(':')[0])
            _cur_time[3] = int(line.split()[1].split(':')[1])
            _cur_time[4] = int(line.split()[1].split(':')[2])
            _before_time = 2592000 * (_cur_time[0] - _boot_time[0]) + 86400 * (_cur_time[1] - _boot_time[1]) + 3600 * (_cur_time[2] - _boot_time[2]) + 60 * (_cur_time[3] - _boot_time[3]) + (_cur_time[4])
            _timestamp_flag = True
          if line.find("/2015")>=0 and not 'Linux' in line and _timestamp_flag:
            _cur_time[0] = int(line.split()[0].split('/')[0])
            _cur_time[1] = int(line.split()[0].split('/')[1])
            _cur_time[2] = (int(line.split()[1].split(':')[0]) + 12) if "PM" in line.split()[2] else int(line.split()[1].split(':')[0])
            _cur_time[3] = int(line.split()[1].split(':')[1])
            _cur_time[4] = int(line.split()[1].split(':')[2])
            _after_time = 2592000 * (_cur_time[0] - _boot_time[0]) + 86400 * (_cur_time[1] - _boot_time[1]) + 3600 * (_cur_time[2] - _boot_time[2]) + 60 * (_cur_time[3] - _boot_time[3]) + (_cur_time[4]) 
            _timestamp_flag = False
          if line.find("avg-cpu")>=0 and not _data_flag:
            _data_flag = True
            continue
          if _data_flag:
            if not _before_flag: # this is before data
              _before_flag = True
              _before_software_layer = float(line.split()[0]) + float(line.split()[2])
              _before_io_wait = float(line.split()[3])
              _data_flag = False
            else:
              _before_flag = False
              _after_software_layer = float(line.split()[0]) + float(line.split()[2])
              _after_io_wait = float(line.split()[3])
              _data_flag = False
        _software_time = _after_software_layer * _after_time - _before_software_layer * _before_time
        _io_wait = _after_io_wait * _after_time - _before_io_wait * _before_time
        ret.writerow([_testnum, _software_time, _io_wait])
        fp.close()
