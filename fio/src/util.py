#!/usr/bin/env Python

import string
import os
import sys
import csv
import time
import subprocess

class Settings:
  _minimal = '--minimal'
  _output_format = '--output-format'
  _output = '--output'

  _testnum = 1
  _iodepth = 1
  _workers = 1    # num of jobs, or IO threads
  _blocksize = '4kb'
  _filesize = '100gb'
  _runtime = 14400
  _patern = 'random'
  _rw = 'read'

  _device = 'NULL' # the target device or file

  def __init__(self, workload_filename):
    self._workload_filename = workload_filename

  def run(self):
    """ Configure files: import the workload file as job settings
    """
    _cur_dir = os.getcwd()
    _log_dir = _cur_dir + os.sep + 'Logs'
    _cfg_dir = _cur_dir + os.sep + 'Configures'
    _cfg_filename = _cfg_dir + os.sep + time.strftime("%m%d%Y")

    _cfg_file = open(_cfg_filename, 'w+')
    with open(self._workload_filename, 'rU') as csvreader:
      reader = csv.reader(csvreader, delimiter=',', quotechar='|')
      for row in reader:
        if "Test id" in row:
          continue
        else:
          # workload CSV file definition:
          # col1  = Test id.        col2  = File size      col3= Block size
          # col4  = Access type     col5  = Run time       col6 = Rampup Time
          # col7  = Start Delay     col8  = Num of jobs    col9 = IOdepth
          # col10 = Target devices  col11 = Numa nodes
          self._testnum = row[0]                         # test id
          #self._filesize = str(row[1]).lower()
          self._blocksize = str(row[2]).lower()
          self._patern = row[3]
          _access_list = self._patern.split()
          self_runtime = row[4]
          self._ramptime = row[5]
          self._startdelay = row[6]
          self._workers = row[7]
          self._iodepth = row[8]
          self._device = row[9]
          _numa_nodes = row[10]

          now = time.strftime("%m%d%Y") + '_' + time.strftime("%H%M")
          job_filename = now + "_" + self._testnum
          job_log_filename = _log_dir + os.sep + self._testnum + ".log"

          _command = "sudo fio" + " " + "--name=%s"%self._testnum + " " + \
                          "--output=%s"%job_log_filename + " " + "--minimal" + " " + \
                          "--bs=%s"%self._blocksize + " " + "--ioengine=libaio" + " " + \
                          "--iodepth=%s"%self._iodepth + " " + "--size=%s"%self._filesize + \
                          " " + "--percentage_random=%s"%int(_access_list[0].rstrip("%")) + \
                          " " + "--rwmixread=%s"%int(_access_list[2].rstrip("%")) + " " + \
                          "--numjobs=%s"%self._workers + " " + "--filename=%s"%self._device + \
                          " " + "--loops=3" + " " + "--thread" + " " + "--direct=1" \
                          + " --group_reporting"
          print _command
          if _numa_nodes != "":
            _command += " " + "--numa_cpu_nodes=%s"%_numa_nodes

          _iostat = "iostat -t"
          iostat_log = open(_cur_dir + os.sep + "IOSTATs" + os.sep + self._testnum, 'w+')
          output1 = subprocess.Popen(_iostat.split(), stdout=subprocess.PIPE).communicate()[0]
          subprocess.call(_command, shell=True)
          output2 = subprocess.Popen(_iostat.split(), stdout=subprocess.PIPE).communicate()[0]
          iostat_log.write(output1)
          iostat_log.write("\n" + output2)

