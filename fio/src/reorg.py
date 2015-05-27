#!/usr/bin/python

import string
import csv
import sys

def main():
  _ret = sys.argv[1]
  ret = csv.writer(open("fiolog_ret.csv", "wb"))
  ret.writerow(["testnum", "iops", "disk utilization", "average bandwidth"])
  strs = {}
  with open(_ret, 'rU') as csvreader:
    reader = csv.reader(csvreader, delimiter=',', quotechar='|')
    for row in reader:
      if "testnum" in row:
        continue
      else:
        x = int(row[0])%16
        if not x in strs:
          strs[x] = []
        strs[x].append(row)
  for x in strs:
    for row in strs[x]:
      ret.writerow(row)

if __name__ == "__main__":
  main()
