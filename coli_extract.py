#!/usr/bin/env python

import sys
import struct
import math
import os

import common
read_f = common.read_f
read_l = common.read_l
read_h = common.read_h
read_b = common.read_b

export_tags = True

version = None
VERSION_0105 = 0x0105
VERSION_0200 = 0x0200

def coli_extract(f):

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/coli/" % (filename), exist_ok=True)

  common.regions = []
  common.data = f.read()
  common.offset = 0

  # Small helper
  def align():
    alignment = 0x20
    align_size = (alignment - common.offset % alignment) % alignment
    v = read_b(align_size, comment="Align", silent=True)
    assert(v == tuple([0xFF]*align_size))

  magic = read_b(8)
  if bytes(magic) == b"COLI0105":
    version = VERSION_0105
  elif bytes(magic) == b"COLI0200":
    version = VERSION_0200
  else:
    assert(False)

  stored = {}

  face_count, something_count = read_l(2)
  unk10, unk14, unk18, unk1C, unk20, unk24, unk28, unk2C = read_l(8)

  if version == VERSION_0200:
    unk30 = read_l(1)[0] #FIXME: What is this?

  print(face_count, something_count)
  assert(something_count < face_count)

  print("0x%X 0x%X" % (unk10, unk14))
  assert(unk10 == 0x40)

  if version == VERSION_0105:
    magic_footer = read_b(16)
    assert(bytes(magic_footer) == b"SEGA-AM2 OUTRUN2")
  elif version == VERSION_0200:
    magic_footer = read_b(12)
    assert(bytes(magic_footer) == b"NEW COLL FMT")
  else:
    assert(False)

  assert(common.offset == unk10)


  # This is a very sparse set of 16 bit values; too large to be indices to face_count or something_count
  vs = read_h(0x10000, comment="Unknown chunk")


  assert(common.offset == unk14)
  common.offset = unk14 #0x40+0x20000 # from 0x14?

  if False:
    #FIXME: I don't know what size this is or how it's used (I thought I did, but I was probably wrong)
    print(common.offset)
    #FIXME: WTF is this?
    index_count = face_count*2
    indices = read_h(index_count)
    stored['indices'] = indices
  else:
    read_b(unk18 - unk14, comment="Unknown chunk")
    common.offset = unk18



  align()
  assert(common.offset == unk18)
  common.offset = unk18 ##FIXME: From 0x18?




  # Custom names given by JayFoxRox
  surfs={
    0x01: (b"road_main",      (1.0, 1.0, 1.0)),
    0x02: (b"offroad_grass",  (0.1, 0.8, 0.2)),
    0x03: (b"offroad_sand",   (0.8, 0.8, 0.1)),
    0x04: (b"offroad_dirt",   (0.3, 0.2, 0.1)),
    0x05: (b"wall_cement",    (1.0, 0.0, 0.0)),
    0x06: (b"wall_barrier",   (1.0, 0.5, 1.0)),
    0x07: (b"offroad_water",  (0.0, 0.8, 0.8)),
    0x08: (b"gutter_road_b",  (1.0, 0.2, 0.0)), # Used in 2A start and 4D start, all along track on 4B; what's the difference to 0xB?
    0x09: (b"offroad_metal",  (0.1, 0.1, 0.1)),
    0x0A: (b"road_extra",     (0.2, 0.2, 1.0)),
    0x0B: (b"gutter_road_a",  (0.3, 0.3, 0.3)),
    0x0C: (b"gutter_stone",   (0.5, 0.5, 0.5)),
    0x0D: (b"gutter_unkown",  (0.0, 0.0, 0.0)), # Used in 7C
    0x0E: (b"wall_invisible", (1.0, 0.0, 1.0)),
    0x10: (b"wall_wood",      (0.0, 0.0, 1.0)),
    0x11: (b"wall_stone",     (0.0, 1.0, 0.0)),
    0x12: (b"wall_rope",      (1.0, 0.0, 0.1)),
    0x13: (b"wall_metal",     (0.1, 0.0, 0.0)),
    0x14: (b"road_stone",     (1.0, 0.3, 0.8)),
    0x17: (b"road_ice",       (0.3, 0.5, 1.0)),
    0x18: (b"wall_fence",     (0.0, 0.1, 0.0)),
    0x19: (b"offroad_snow",   (1.0, 1.0, 1.0)),
  }


  # Read surface types
  surf = read_b(face_count)
  stored['surf'] = surf





  print(common.offset, unk1C)
  align()
  assert(common.offset == unk1C)
  common.offset = unk1C




  # Read faces
  print(common.offset)
  faces = []
  for i in range(face_count):

    # 4 corners
    va = read_f(3)
    vb = read_f(3)
    vc = read_f(3)
    vd = read_f(3)

    print(va,vb,vc,vd)

    # Center
    v = read_f(3)
    print(v)


    # Unknown
    u = read_l(1)

    face = {'corners': (va,vb,vc,vd), 'center': v, 'unk': u }

    if version == VERSION_0105:
      # Usually 1,1,1,1
      x,y,z,w = read_f(4)
      face['unkxyzw'] = (x,y,z,w)
      print(x,y,z,w)

    print()

     

    faces += [face]

  stored['faces'] = faces


  print(common.offset, unk20)
  align()
  assert(common.offset == unk20)
  common.offset = unk20


  print("")
  print("Normals")
  normals = []
  #FIXME: WTF is this?
  # Some smaller items with 48 bytes each (1 per previous item?)
  for i in range(face_count):

    na = read_f(3)
    nb = read_f(3)
    nc = read_f(3)
    nd = read_f(3)

    if False:
      def vlen(v):
        return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
      print(vlen(na), vlen(nb), vlen(nc), vlen(nd))

    print(i) 

    normals += [(na, nb, nc, nd)]
  stored['normals'] = normals




  print(common.offset, unk24)
  align()
  assert(common.offset == unk24)
  common.offset = unk24




  #FIXME: WTF is this?
  surf2 = read_b(face_count)
  stored['surf2'] = surf2



  print(common.offset, unk28)
  align()
  assert(common.offset == unk28)
  common.offset = unk28



  # This is an index on how far along the track this face is?
  segment_index = read_h(face_count)
  stored['segment_index'] = segment_index



  print(common.offset, unk2C)
  align()
  assert(common.offset == unk2C)
  common.offset = unk2C

  #common.offset += 8 # for CS_1A
  # +28 in CS_2A instead


  # This seems to be some other file? [note from future: Why did I write this?]
  #FIXME: Store all fields
  print()
  print("Spline?")
  print()
  if True:

# Courses:
#00000001;00000008;00000000;00000001;00000000
#00000283
#
#FFFFFFFF;FFFFFFFF
#00000000
#
#FFFFFFFF;FFFFFFFF
#00000000
#
#FFFFFFFF;FFFFFFFF
#00000284

# BK
#00000004;00000014;00000F68;00001EBC;00002270
#00000064

#00000001;00000000
#000000F1

#FFFFFFFF;FFFFFFFF
#00000000

#FFFFFFFF;FFFFFFFF
#00000000




    heada, headb, headc, headd= read_l(4)
    something_else_count = read_l(1)[0]
    print()


    stored['spline?'] = []

    for xxx in range(heada):

      #FIXME: heada * heada is probably wrong; but it seems to work for now?
      read_l(heada)
      print()

      read_l(2)
      something_else_count3 = read_l(1)[0]
      print()

      unka = read_l(2)
      read_l(1)[0]
      print()

      unkb = read_l(2)
      something_else_count2 = read_l(1)[0]
      print()

      print(something_else_count, something_else_count3, something_else_count2)

      #assert(something_else_count <= something_else_count2)

      print(common.offset)


      # Some smaller items with 16 bytes each
      spline = []
      for i in range(something_else_count2):
        pos = read_f(3) # Spline coordinates maybe? Seems to follow ideal route [not center?]
        unk0 = read_l(1)[0]
        assert(unk0 == 0xFFFFFFFF)

        spline += [{"position": pos, "unk0": unk0}]

        print(i)
      stored['spline?'] += [spline]

    print(common.offset)


  if version == VERSION_0200:
    print(common.offset, unk30)
    align()
    assert(common.offset == unk30)

    #FIXME: Broken?
    for i in range(face_count+1):
      read_b(4)

    #FIXME: Broken!
    read_l(6) # Seen 2, 4, 6 weird values

  print(common.offset, len(common.data))
  align()
  assert(common.offset == len(common.data))




  surfs2 = {
    0: b""
  }

  for i, tmps in enumerate(stored['spline?']):
    fo = open("/tmp/or2/%s/coli/spline-%d.obj" % (filename, i), "wb")
    for j, tmp in enumerate(tmps):
      fo.write(b"v %f %f %f\n" % tmp['position'])
    fo.write(b"l")
    for i in range(len(tmps)):
      fo.write(b" %d" % (1+i))
    fo.write(b"\n")

  fo = open("/tmp/or2/%s/coli/collision_mesh.mtl" % (filename), "wb")
  for s1 in surfs:
    fo.write(b"newmtl 0x%02X-%s\n" % (s1, surfs[s1][0]))
    fo.write(b"kd %f %f %f\n" % surfs[s1][1])
   

  fo = open("/tmp/or2/%s/coli/collision_mesh.obj" % (filename), "wb")
  for i, face in enumerate(stored['faces']):
    va,vb,vc,vd = face['corners']
    v = face['center']

    vna,vnb,vnc,vnd = stored['normals'][i]

    s1 = stored['surf'][i]
    s2 = stored['surf2'][i]
    #i1 = stored['indices'][i*2:i*2+2]
    i2 = stored['segment_index'][i]

    #fo.write(b"g 0x%04X:0x%04X\n" % (indices[i*2+0],indices[i*2+1]))

    fo.write(b"usemtl 0x%02X-%s\n" % (s1, surfs[s1][0]))
    #fo.write(b"usemtl 0x%02X-%s\n" % (s2, surfs2[0]))
    #fo.write(b"usemtl 0x%X:%X\n" % (i1[0], i1[1])) # ???
    #fo.write(b"usemtl 0x%X\n" % (i2))

    #FIXME: normals and center points
    fo.write(b"vn %f %f %f\n" % vna)
    fo.write(b"v %f %f %f\n" % va)
    fo.write(b"vn %f %f %f\n" % vnb)
    fo.write(b"v %f %f %f\n" % vb)
    fo.write(b"vn %f %f %f\n" % vnc)
    fo.write(b"v %f %f %f\n" % vc)
    fo.write(b"vn %f %f %f\n" % vnd)
    fo.write(b"v %f %f %f\n" % vd)
    fo.write(b"f %d//%d %d//%d %d//%d %d//%d\n" % (4+i*5,4+i*4, 3+i*5,3+i*4, 2+i*5,2+i*4, 1+i*5,1+i*4))
    fo.write(b"v %f %f %f\n" % v)

  if export_tags:
    common.export_tags("/tmp/or2/%s/decompressed.bin.tags" % (filename))

if __name__ == "__main__":
  for path in sys.argv[1:]:
    f = open(path, 'rb')
    coli_extract(f)
