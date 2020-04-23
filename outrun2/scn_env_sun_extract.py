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

def scn_env_sun_extract(f):

  # Designed for SCN_ENV_SUN_1A_BIN.GZ
  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/scn/" % (filename), exist_ok=True)

  print()
  head = read_l(1)[0]
  assert(head == 0xC)
  head2 = read_l((head - 4) // 4)

  #FIXME: Instead, read stream starting from head2[0] and head2[1]
  i = 0
  while common.offset < len(common.data):
    tmp = {}

    tmp['zero1?'] = read_l(1)
    tmp['unkx?'] = read_f(3) #FIXME: Sometimes looks like float, sometimes not? OR2 / OR2006 diff?
    tmp['unkz?'] = read_l(1)[0]
    tmp['position?'] = read_f(3)

    tmp['unkf?'] = read_f(4)
    tmp['matrix1?'] = read_f(4*4)
    tmp['matrix2?'] = read_f(4*4)

    tmp['unka?'] = read_l(4)
    tmp['unkb?'] = read_l(4)

    tmp['zero2?'] = read_l(36)
    print(i, tmp, "0x%X" % common.offset)

    assert(tmp['zero1?'] == tuple([0]*1))
    assert(tmp['zero2?'] == tuple([0]*36))

    print()

    if common.offset > head2[1]:
      break
    
    i += 1


  print()

  while common.offset < len(common.data):
    v = read_l(1)[0]
    assert(v == 0)

  assert(common.offset == len(common.data))

  if export_tags:
    common.export_tags("/tmp/or2/%s/weird.bin.tags" % (filename))


