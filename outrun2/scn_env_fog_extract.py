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

def scn_env_fog_extract(f):

  # Designed for SCN_ENV_FOG_1A_BIN.GZ
  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/scn/" % (filename), exist_ok=True)

  print()
  head = read_l(1)[0]
  if head == 0xC:
    head2 = read_l((head - 4) // 4)

  if head == 0x10:
    #FIXME: These seem to be working a bit differently?
    print("Skipping SCN for %s" % filename)
    return

  #FIXME: Instead, read stream starting from head2[0] and head2[1]
  i = 0
  while common.offset < len(common.data):
    tmp = {}

    tmp['begin?'] = read_l(1)[0] # Begin?
    if False:
      tmp['unka'] = read_f(1)[0]
      tmp['unkb'] = read_l(1)[0]
      tmp['unkc'] = read_f(1)[0]
    else:
      tmp['unkabc'] = read_f(3)
    tmp['end?'] = read_l(1)[0] # End?

    is_eos = (tmp['begin?'] == 0xFFFF and tmp['end?'] == 0xFFFF)

    tmp['position?'] = read_f(3)

    tmp['unkd?'] = read_f(4)


    tmp['unk2'] = []
    for i in range(2):
      tmp2 = {}
      tmp2['unkx'] = read_l(4)
      tmp2['unky'] = read_f(1)[0]
      tmp2['unkz'] = read_l(1)[0]
      tmp2['color?'] = read_l(1)[0]
      tmp['unk2'] += [tmp2]
      if not is_eos:
        assert(tmp2['unkx'] in [(1,2,0,0),(1,1,0,0)])
        assert(tmp2['unkz'] == 0x00FFFFFF)
        assert(tmp2['color?'] & ~0xFFFFFF == 0)

    tmp['zero?'] = read_l(18)
    print(i, tmp, "0x%X" % common.offset)

    assert(tmp['zero?'] == tuple([0]*18))

    print()

    if common.offset > head2[1]:
      if is_eos:
        break
    
    i += 1


  print()

  while common.offset < len(common.data):
    v = read_l(1)[0]
    assert(v == 0)

  assert(common.offset == len(common.data))

  if export_tags:
    common.export_tags("/tmp/or2/%s/weird.bin.tags" % (filename))


