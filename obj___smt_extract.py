#!/usr/bin/env python

import sys
import struct
import os

import common
read_f = common.read_f
read_l = common.read_l
read_h = common.read_h
read_b = common.read_b


export_tags = False

def obj___smt_extract(f):

  return False

  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/obj___smt/" % (filename), exist_ok=True)

  if False:
    return

  if True:
    if True:
      # Hardcoded for OBJ_MISSIONOBJ_SMT.GZ

      #FIXME: Also search 0x30 / 48 header which is also used in CS_*_SMT

      offsets = [
        # Index count at 0x990
        # Indices at 0xAA0 [offset -16 is at 0xA98]
        # Pointer to vertices relative to data section at 0xA8C
        (0xDA28+4*6, 1988, "Lff"), #FIXME: Should be 1992 as indices go up to 1991

        (103584+18*4, 88, "L"),

        (105064+6*4, 30+15, "Lff"),
        #(105808, 15, "Lff"),

        (106168+2*4, 87, "L"),

      ]
    else:
      # Hardcoded for OBJ_PLCAR_F50_SMT.GZ
      offsets = [
        (0x5E93C, 2140, "L"), # Decoration and hull inside?
        (421628-8, 5742, "Lff"), # Exterior hull (xyz,uv)?

        (559424-4, 429, "L"), # windscreen wiper

        (566284, 1476, "Lff"), # Front and details

        (601708+4*2, 169, "Lffff"), # 


        #(601724+8, 149, "L"), # 2 objects interleaved? wth?

        #(604132+4*4, 124, "LLLLL"), # dashboard
        #(608100, 332, "ffL"),


        #(608308+16, 322, "Lff"),
        #(616052, 92, "L"),

        #(617524+16, 416, "Lff"),
      ]
  else:
    common.offset = 0x490A0 # OBJ_COURSE_OBJ_CS_1A_SMT.GZ  [FIXME: Is this relative to XPR tag?]
    count = 265+1000 # Then 8 bytes unknown and then objects of size 32 follow [about 1000 bytes of that]
    unk = 3 # Unk, Float, Float

  for offset in offsets:

    common.offset = offset[0]
    count = offset[1]
    unk = offset[2]

    fo = open("/tmp/or2/%s/obj___smt/foo-%d-%s.obj" % (filename, offset[0], unk), "wb")
    fo.write(b"g 0x%X\n" % offset[0])

    d = 0
    for i in range(count):
      def check(v):
        pass
        assert(abs(v) < 1e3)

      print()
      print(i, count)
      v = read_f(3)
      p = []
      for c in unk:  
        reader = {
          'f': read_f,
          'L': read_l,
        }  
        p = reader[c](1)
      check(v[0])
      check(v[1])
      check(v[2])

      d = p[0]
      fo.write(b"v %f %f %f\n" % v)
      print(common.offset)

    #FIXME: This is merely a lookahead
    print()

    read_l(100)


    if False:
      for i in range(100):
        fo.write(b"f %d %d %d\n" % (1+i*2,2+i*2,3+i*2))

