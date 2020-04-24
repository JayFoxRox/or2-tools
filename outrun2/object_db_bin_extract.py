#!/usr/bin/env python

import sys
import struct
import os

from . import common
read_f = common.read_f
read_l = common.read_l
read_h = common.read_h
read_b = common.read_b
read_s = common.read_s

export_tags = False

def object_db_bin_extract(f):

  # Designed for object_db_bin.sz
  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  print()
  head = read_l(1)[0]

  offsets = []
  while common.offset < head:
    offset = read_l(1)[0]
    if offset == 0:
      break
    offsets += [offset]

  #for i in range(11):
  #  print("0x%X" % common.offset)
  #  read_l(2)

  #read_l(2)


  for offset in offsets:
    common.offset = offset

    print()
    print()
    print("offset", offset)
    print()
    print()

    while True:
      tmp = {}

      addr = read_l(1, silent=True)[0]
      print(addr)

      tmp['element'] = read_h(1, silent=True)[0] 
      tmp['container'] = read_h(1, silent=True)[0]

      if tmp['element'] == 0xFFFF and tmp['container'] == 0xFFFF:
        assert(addr == 0)
        break

      common.push()
      common.offset = addr
      name = read_s(0, silent=True)
      tmp['name'] = name
      common.pop()
      
      print(tmp)



  print()

  if False:
    while common.offset < len(common.data):
      v = read_l(1)[0]
      assert(v == 0)

    assert(common.offset == len(common.data))

  if export_tags:
    common.export_tags("/tmp/or2/%s/weird.bin.tags" % (filename))


