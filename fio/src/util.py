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

  _iodepth = 1
  _workers = 1    # num of jobs, or IO threads
  _blocksize = '4kb'
  _filesize = '1gb'
  _runtime = 14400
  _patern = 'random'
  _rw = 'read'

  _device = 'NULL' # the target device or file

  _cur_dir = os.getcwd()
  _log_dir = _cur_dir + os.sep + 'Logs'
  _cfg_dir = _cur_dir + os.sep + 'Configures'

  def _util_create_cfg():
    """ Configure files: import the workload file as job settings
    """
    _cfg_filename = _cfg_dir + os.sep + time.strftime("%m%d%Y")
    _cfg_file = open(_cfg_filename, "wb")
    with open(_workload_filename, 'rb') as csvreader:
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
          _testnum = row[0]                         # test id
          _filesize = str(row[1]).lower()
          _blocksize = str(row[2]).lower()
          _patern = row[3]
          _access_list = _patern.split()
          _runtime = row[4]
          _ramptime = row[5]
          _startdelay = row[6]
          _workers = row[7]
          _iodepth = row[8]
          _device = row[9]
          _numa_nodes = row[10]

          now = time.strftime("%m%d%Y") + '_' + time.strftime("%H%M")
          job_filename = now + "_" + _testnum
          job_log_filename = _log_dir + os.sep + _testnum + ".log"

          _command = "fio" + " " + "--name=%s"%_testnum + " " + "--output=%s"%job_log_filename + " " + "--minimal" + " " + "--bs=%s"%_blocksize + " " + "--ioengine=libaio" + " " + "--iodepth=%s"%_iodepth + " " + "--size=%s"%_filesize + " " + "--direct=1" + " " + "--percentage_random=%s"%int(_access_list[0].rstrip("%")) + " " + "--rwmixread=%s"%int(_access_list[2].rstrip("%")) + " " + "--numjobs=%s"%_workers + " " + "--filename=%s"%_device + "--group_reporting" + " " + "--loops=3" + " " + "--thread"
          if _numa_nodes != "":
            _command += " " + "--numa_cpu_nodes=%s"%_numa_nodes

          subprocess.call(_command, shell=True)

