#!/usr/bin/env Python

import re
import os
import sys
import platform

def display_usage():
  print '*' * 66
  print 'I/O evaluation with FIO for parallel I/Os on many-core system'
  print 'Author: Junjie Qian (jqian.unl@gmail.com)'
  print '-' * 66
  print 'Usage: %s [options]'%sys.argv[0]
  print '  -f workload: Set the test workload file path required'
  print '*' * 66
  return

if __name__ == "__main__":
#  if not platform.system() == "Linux":
#    sys.exit("OS version not supported\n")
  display_usage()
  main()
