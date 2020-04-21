#!/usr/bin/env python

import sys
import struct
import os

from . import common
read_f = common.read_f
read_l = common.read_l
read_h = common.read_h
read_b = common.read_b

export_tags = False

def bin_extract(f):

  # Designed for CS_LRBK_1A_BIN.GZ
  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/bin/" % (filename), exist_ok=True)

  addr0 = read_l(1)[0]
  addrs = [addr0]

  # Header seems to contain a list of streams?
  # In sin_extract.py this would be the `offset` loop; not the addr loop
  i = 0
  while(common.offset < addr0):
    print(i)

    addr = read_l(1)[0]
    addrs += [addr]
    print(addr)
    i += 1

  print()
  print(common.offset)
  print()


  for addr in addrs:
    print("Visiting address from header")
    print(common.offset)
    print()

    addr_base = addr
    common.offset = addr_base
    print(common.offset, hex(common.offset))
    while True:
      v = read_l(1)[0]
      if v == 0xFFFFFFFF:
        break

    print()

  assert(common.offset == len(common.data))


  if export_tags:
    common.export_tags("/tmp/or2/%s/weird.bin.tags" % (filename))


