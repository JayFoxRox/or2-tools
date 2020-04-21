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

def sin_extract(f):

  # Designed for CS_CS_1A_SIN.GZ
  common.data = f.read()
  common.offset = 0

  # These seem to have a prefix with length, and then file offsets are +4
  filelength = read_l(1)[0]
  assert(len(common.data) == (4+filelength))

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/sin/" % (filename), exist_ok=True)

  head = read_l(3)

  assert(head[0] == 0)
  assert(head[1] == 0)
  print("0x%X" % head[2])
  

  # Header seems to contain a list of stream tables?
  if ((common.offset - 4) >= head[2]):

    print("Warning: Only a single stream found in %s!" % filename)

    assert((common.offset - 4) == head[2])

    addrs = [head[2]]

  else:

    i = 0
    addrs = []
    while((common.offset - 4) < head[2]):
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

    addr_base = 4 + addr
    common.offset = addr_base

    offset0 = read_l(1)[0]
    offsets = [offset0]
    while((common.offset - addr_base) < offset0):
      offset = read_l(1, silent=True)[0]
      offsets += [offset]

    for offset in offsets:
      common.offset = addr_base + offset
      print(offset, common.offset, hex(common.offset))
      while True:
        v = read_h(1)[0]
        if v == 0xFFFF:
          break
    print(common.offset)
    if common.offset % 4 != 0:
      eos = read_h(1)[0]
      assert(eos == 0xCDCD)

    print()

  assert(common.offset == len(common.data))


  if export_tags:
    common.export_tags("/tmp/or2/%s/weird.bin.tags" % (filename))


