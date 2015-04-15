#!/usr/bin/env Python

import re
import os
import sys
import platform

from src.util import Settings
from src.logreader import reader

def display_usage():
  print '*' * 66
  print 'I/O evaluation with FIO for parallel I/Os on many-core system'
  print 'Author: Junjie Qian (jqian.unl@gmail.com)'
  print '-' * 66
  print 'Usage: %s [options]'%sys.argv[0]
  print '  -f workload: Set the test workload file path required'
  print '*' * 66
  return

def main():
#  util = Settings(sys.argv[1])
#  util.run()
  logreader = reader("./workload/workload_numjobs.csv", "./Logs", "./IOSTATs")
  logreader.perf_read()
  logreader.iostat_read()

if __name__ == "__main__":
  if not platform.system() == "Linux":
    sys.exit("OS version not supported\n")
  if len(sys.argv) < 2:
    display_usage()
    sys.exit()
  main()
