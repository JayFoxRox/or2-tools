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

def oso_extract(f):

  # Designed for OSO_QT_5E3.GZ
  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/oso/" % (filename), exist_ok=True)

  while common.offset < (len(common.data) - 39):
    unkf = read_f(3)
    unkf2 = read_f(3)
    unka1 = read_l(1)[0]
    unka2 = read_l(1)[0]
    unka3 = read_l(1)[0]
    unka4 = read_l(1)[0]

    if unka1 == 0:
      break

    assert(unka4 in [0,0x14])

    print()


  print()
  print()

  while common.offset < len(common.data):
    v = read_l(1)[0]
    assert(v == 0)

  assert(common.offset == len(common.data))


  if export_tags:
    common.export_tags("/tmp/or2/%s/weird.bin.tags" % (filename))


