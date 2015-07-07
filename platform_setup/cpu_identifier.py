#!/usr/bin/python
# identify the cpu info

import string

def main():
  fp = open('/proc/cpuinfo', 'r')
  ids = [-1, -1, -1]
  all_id = []
  for line in fp:
    if line.find("processor") == 0:
      if ids[0] != -1:
        all_id.append(ids)
      ids = [-1, -1, -1]
      ids[0] = int(line.split(':')[1]) # processor id
    elif line.find("physical id") == 0:
      ids[1] = int(line.split(':')[1]) # physical_id
    elif line.find("core id") == 0:
      ids[2] = int(line.split(':')[1]) # core_id
  print "[processor id, physical id, core id]"
  all_id.sort(key=lambda x:x[1]) # sort based on the physical id
  for i in all_id:
    print i

if __name__ == "__main__":
  main()