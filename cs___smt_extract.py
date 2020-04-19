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

fo = None
obj_v_index = None
obj_vt_index = None
obj_vn_index = None
tex_unit_index = 0

def cs___smt_extract(f):

  global fo
  global obj_v_index
  global obj_vt_index
  global obj_vn_index

  # Designed for CS_CS_1A_SMT.GZ   weird.bin

  common.regions = []
  common.data = f.read()
  common.offset = 0

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/cs___smt/" % (filename), exist_ok=True)

  #FIXME: Read other header fields
    
  unk0, unk4, weird, unkC = read_l(4)
  data_base = weird + 0x10
  assert(data_base == (struct.unpack_from("<L", common.data, 8)[0] + 16))


  offsets = []

  # OBJ_*_SMT
  if True:
    zzz = read_l(1)[0]
    assert(zzz == 0)
    head2 = read_l(2)
    assert(head2[0] == unk0)
    assert(head2[1] == unk4)
    zzz4 = read_l(4)
    assert(list(zzz4) == [0]*4)
    print()

    cy = 0
    for j in range(head2[0]):
      print()

      va,vb,vc = read_l(3)

      vd = read_l(1)[0]
      #assert(vd == 0) # Typically true, but not always

      ve,vf = read_l(2) # Header pointers
      assert(ve == vf)

      vg = read_l(1)[0] # Collection pointer?
      assert(vg == ve + 0x30)

      vh, vi, vj, vk, vl, vm, vn = read_l(7)

      vo = read_l(1)[0] # Always zero
      assert(vo == 0)

      offsets += [(ve + 0x10, 0, 0, va, vb, vc, vd)]

      cy += 1
      print(cy)

    off = common.data.find(b'XPR0')
    pad = (off - common.offset) // 4
    assert(pad == head2[1])
    print(pad)
    for i in range(pad):
      v = read_l(1)[0]
      assert(v == 0)

  print()
  print(common.offset)

  #FIXME: This is a stupid heuristic
  # offsets of FFFFFFFFFFFFFFFFFFFFFFFF patterns in file
  ranges = []
  if False:
    of = 0
    while((of + 56) < len(common.data)):
      ofa = common.data.find(bytes([0xFF]*12), of + 56)
      print(ofa)
      if ofa == -1:
        break

      ofb = ofa+56
      while common.data[ofb:ofb+12] == bytes([0xFF]*12):
        ofb += 56

      ofb -= 56
      of = ofb

      print("adding", ofa, ofb)
      fixup = 0 #FIXME: For CS_
      ranges += [(ofa+fixup, ofb+fixup, fixup)]
      fixup = 16 #FIXME: For OBJ_
      ranges += [(ofa+fixup, ofb+fixup, fixup)]


  for r in ranges:
    print(r)
    offsets += [(r[0]-44-48,1+(r[1]-r[0])//56,r[2])]



  for offsetx in offsets:


    common.offset = offsetx[0]
    counta = offsetx[1]
    fixup = offsetx[2]


    va = offsetx[3] # [middle] Some start pointer?
    vb = offsetx[4] # [lowest] Some start pointer? 0x10 bytes for each element between middle and highest?
    vc = offsetx[5] # [highest] Some end pointer [+4 / +8 on va?]
    vd = offsetx[6] #FIXME: Use after figuring out what this is






    print("")
    print("")
    print("")
    print("")
    print("")
    print("%d = 0x%X" % (common.offset, common.offset))
    print("")

    assert(common.offset - offsetx[0] == 0)
    head = read_l(9)
    head2 = read_l(3)

    # global-header for this offset: [...some fields not in local header...]
    #                                00000914;         0000094C;00000954;00000968;00000978;00000988;000009B4;00000A0C
    # local-header in `head`:        00000030;00000068;00000068;00000070;00000084;00000094;000000A4;000000D0;00000128
    #                                00000001;00000001;00000001
    # So this local header is just the same


    print("")
    print("%d %d" % (head[0], counta))
    print("")

    if False:
      if head[0] != 0x30:
        print("bad offset: 0x%X" % offsetx[0])
        continue

    # This suggests that these are independent files
    assert(head[0] == 0x30)


    #FIXME: Finds OBJ_COURSE_OBJ_CS_1A_R_SMT.GZ:
    # head1: 00000030;00000068;00000068;00000068;00000068;00000068;00000068;00000068;00000068
    # head2: 00000000;00000000;00000000
    if (list(head2) == [0]*3):
      print("Broken object?!")
      continue



    objects = []
    print("")
    print("Objects ? (collect1)")
    print("")
    print(common.offset - offsetx[0], head[0])
    assert(common.offset - offsetx[0] == head[0])
    i = 0
    tmp = None
    while((common.offset - offsetx[0]) < head[1]): # Similar to counta?

      tmp = {}

      tmp['unk0_flags?'] = read_l(1, silent=True)[0] # 0x442 = skidmarks?
      tmp['position'] = read_f(3, silent=True)
      tmp['unk1?'] = read_f(1, silent=True)[0]
      tmp['unk2?'] = read_l(2, silent=True)
      tmp['matrix_index?'] = read_l(1, silent=True)[0] # Optional matrix index?
      tmp['unk3b?'] = read_l(1, silent=True)[0]
      tmp['collect1_index?'] = read_l(1, silent=True)[0] # index to next object?
      tmp['collect2_index?'] = read_l(1, silent=True)[0]
      tmp['collect2_indices?'] = read_l(3, silent=True) # More optional indices

      print(i, tmp)

      print(hex(tmp['unk0_flags?']))
      assert(tmp['unk0_flags?'] in [0x001,0x002,0x003,0x005,            0x009,
                                    0x011,            0x015,            0x019,
                                    0x021,      0x023,0x025,0x026,      0x029,0x02A,
                                    0x041,0x042,0x043,0x045,0x046,      0x049,0x04A,
                                    0x051,
                                    0x061,      0x063,0x065,0x066,0x067,0x069,0x06A,0x06B,
                                    0x101,0x102,                    
                                    0x141,      0x143,
                                    0x181,
                                                0x203,
                                          0x402,0x403,
                                    0x441,0x442,0x443,0x445,0x446,0x447,0x449,      0x44B,
                                    0x541,
                                    0x801,0x802,      0x805,0x806,      0x809,0x80A,
                                    0x841,0x842,      0x845,0x846,      0x849,0x84A,
                                    0x861,            0x865,0x866,0x867,0x869,0x86A,0x86B,
                                                                        0xC09,
                                                            0xC66,            0xC6A      ])

      assert(tmp['unk1?'] >= 0.0)
      print("WTF", tmp['unk1?'])

      #assert(tmp['unk3a?'] == 0xFFFFFFFF)

      #if i == 0:
      #  assert(tmp['collect1_index?'] == 1)
      if i < counta - 1:
        assert(tmp['collect1_index?'] != 0xFFFFFFFF)
        assert(tmp['collect1_index?'] == i+1)

      # Almost always holds true.. but not always
      #assert(tmp['collect2_index?'] == i)
      if i < counta:
        assert(tmp['collect2_index?'] <= i)

      #assert(tmp['unk3?'] == tuple([0xFFFFFFFF]*2))
      if i < counta:
        assert(tmp['collect2_indices?'] == tuple([0xFFFFFFFF]*3))
      assert(tmp['collect2_indices?'][0] <= tmp['collect2_indices?'][1])
      assert(tmp['collect2_indices?'][1] <= tmp['collect2_indices?'][2])
      if tmp['collect2_indices?'] != tuple([0xFFFFFFFF]*3):
        pass #print("WTF", tmp['collect2_indices?'])

      objects += [tmp]
      i += 1

    if tmp != None:
      assert(tmp['collect1_index?'] == 0xFFFFFFFF)

    fo = open("/tmp/or2/%s/cs___smt/objects-0x%X.obj" % (filename, offsetx[0]), "wb")
    for tmp in objects:
      fo.write(b"usemtl 0x%08X\n" % tmp['unk0_flags?'])
      def rot(v, angle, f):
        angle *= math.pi / 180.0
        vr = (
          v[0]+math.sin(angle) * f,
          v[1],
          v[2]+math.cos(angle) * f
        )
        return vr 
      fy = 8.0
      fx = fy / 4.0
      fo.write(b"v %f %f %f\n" % tuple(rot(tmp['position'], tmp['unk1?']+0.0, fx)))
      fo.write(b"v %f %f %f\n" % tuple(rot(tmp['position'], tmp['unk1?']+90.0, fy)))
      fo.write(b"v %f %f %f\n" % tuple(rot(tmp['position'], tmp['unk1?']+180.0, fx)))
      fo.write(b"v %f %f %f\n" % tuple(rot(tmp['position'], tmp['unk1?']+270.0, 0.0)))
      fo.write(b"f %d %d %d %d\n" % (1+i*4,2+i*4,3+i*4,4+i*4))


    matrices = []
    print("")
    print("Matrices?")
    print("")
    print(common.offset - offsetx[0], head[1])
    assert(common.offset - offsetx[0] == head[1])
    i = 0
    while((common.offset - offsetx[0]) < head[2]):
      print(i)
      tmp = []
      tmp += [read_f(4)]
      tmp += [read_f(4)]
      tmp += [read_f(4)]
      tmp += [read_f(4)]
      matrices += [tmp]
      i += 1
    #assert(head[1] == head[2])

    print("")
    print("Collect2")
    print("")
    collect2 = []
    print(common.offset - offsetx[0], head[2])
    assert(common.offset - offsetx[0] == head[2])
    i = 0
    while((common.offset - offsetx[0]) < head[3]):
      tmp = {}
      tmp['a_collect3_index?'] = read_l(1, silent=True)[0] # Index into collect3?
      tmp['a_count?'] = read_l(1, silent=True)[0]
      print(i, tmp)
      assert(tmp['a_count?'] in [1,2,3,5])
      collect2 += [tmp]
      i += 1

    print("")
    print("Collect3")
    print("")
    collect3 = []
    print(common.offset - offsetx[0], head[3])
    assert(common.offset - offsetx[0] == head[3])
    i = 0
    while((common.offset - offsetx[0]) < head[4]):
      tmp = {}
      tmp['collect6_index?'] = read_l(1, silent=True)[0]
      tmp['a_collect4/5_index?'] = read_l(1, silent=True)[0] # Optional index into collect4/5?
      tmp['b_collect4/5_index?'] = read_l(1, silent=True)[0] # Optional index into collect4/5?
      tmp['a_count?'] = read_l(1, silent=True)[0]
      tmp['b_count?'] = read_l(1, silent=True)[0]
      print(i, tmp)
      assert(tmp['a_count?'] in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,64])
      assert(tmp['b_count?'] in [0,1,2,3,4,5,  6,7,9,10,11,40]) # 4 and 5 are rare; 6 and up are only in OBJ_ but not in CS_
      collect3 += [tmp]
      i += 1

    print("")
    print("Collect4 (Renderstates for draw calls?)")
    print("")
    collect4 = []
    print(common.offset - offsetx[0], head[4])
    assert(common.offset - offsetx[0] == head[4])
    i = 0
    while((common.offset - offsetx[0]) < head[5]):
      tmp = {}
      tmp['vertex_offset'] = read_l(1, silent=True)[0] # index offset like collect5 [but different splits?]
      tmp['collect7_index?'] = read_l(1, silent=True)[0]
      tmp['collect5_index?'] = read_l(1, silent=True)[0] # Index into collect5?
      tmp['unk3_boolean?'] = read_l(1, silent=True)[0] # Some boolean?
      #assert(tmp[0] == 0) seems to be some offset or something?
      #assert(tmp[1] in [0,1,2,3,4])
      #assert(tmp[2] in [0,1,2,3,4])
      print(i, tmp)
      assert(tmp['collect7_index?'] < head2[1]) # Some kind of texture lookup?
      #assert(tmp['unk0?'][2] < head2[1]) # Some kind of texture lookup?
      assert(tmp['unk3_boolean?'] in [0,1])
      collect4 += [tmp]
      i += 1

    print("")
    print("Collect5 (Draw calls?)")
    print("")
    collect5 = []
    print(common.offset - offsetx[0], head[5])
    assert(common.offset - offsetx[0] == head[5])
    i = 0
    while((common.offset - offsetx[0]) < head[6]):
      tmp = {}
      tmp['primitive_type'] = read_l(1, silent=True)[0] # Type of draw call? [assert 6]
      tmp['index_offset'] = read_l(1, silent=True)[0] # Index offset?
      tmp['index_count'] = read_l(1, silent=True)[0] # Count of indices in draw call
      tmp['unk0?'] = read_l(1, silent=True)[0] # unknown [similar to count of indices] # Count of unique vertices?
      print(i, tmp)
      collect5 += [tmp]
      if tmp['primitive_type'] == 5:
        assert(tmp['unk0?'] == tmp['index_count'])
      elif tmp['primitive_type'] == 8:
        assert(tmp['unk0?'] == tmp['index_count'])
      elif tmp['primitive_type'] == 6:
        assert(tmp['unk0?'] <= tmp['index_count'])
        pass #assert([ tmp['index_count'], tmp['unk0?']] in [[25,20], [2,2], [144,96], [218,144], [70,48], [211,145], [864,412], [79,43], [10,6], [89,48], [21,16], [205,116], [87,45], [93,45]])
      else:
        assert(False)
      i += 1

    print(common.offset - offsetx[0], head[6])
    assert(common.offset - offsetx[0] == head[6])

    print("")
    print("Collect6 (Mesh data)")
    print("")
    collect6 = []
    i = 0
    while((common.offset - offsetx[0]) < head[7]):
      tmp = {}
      tmp['unk0?'] = read_l(1, silent=True)[0]
      tmp['ib_ptr'] = read_l(1, silent=True)[0]
      tmp['vb_ptr'] = read_l(1, silent=True)[0]
      tmp['unk1_ptr?'] = read_l(3, silent=True)  #FIXME: Maybe index buffers for LOD?
      tmp['ib_size'] = read_l(1, silent=True)[0] # Size of index buffer?
      tmp['vb_size'] = read_l(1, silent=True)[0] # Size of vertex buffer?
      tmp['fvf?'] = read_l(1, silent=True)[0] # FVF?
      tmp['vertex_size'] = read_l(1, silent=True)[0] # Vertex size?
      tmp['unk2?'] = read_l(1, silent=True)[0] # Always zero?
      print(i, tmp)

      fvf = tmp['fvf?']
      print("FVF: 0x%X" % fvf)
      fvf_meaning = []
      if fvf == 0:
        fvf_meaning = ["<SPECIAL>"]
        fvf_size = 44
      else:
        fvf_size = 0


        if fvf & 0xE == 0x2:
          fvf &= ~0x2
          fvf_meaning += ["XYZ"]
          fvf_size += 4*3
        if fvf & 0xE == 0x6:
          fvf &= ~0x6
          fvf_meaning += ["XYZB1"]
          fvf_size += 4*3+1*4
        if fvf & 0xE == 0x8:
          fvf &= ~0x8
          fvf_meaning += ["XYZB2"]
          fvf_size += 4*3+2*4
        if fvf & 0xE == 0xA:
          fvf &= ~0xA
          fvf_meaning += ["XYZB3"]
          fvf_size += 4*3+3*4


        if fvf & 0x10:
          fvf &= ~0x10
          fvf_meaning += ["NORMAL"]
          fvf_size += 4 #FIXME: Should be 12, but somehow forces compression on Xbox?

        if fvf & 0x40:
          fvf &= ~0x40
          fvf_meaning += ["DIFFUSE"]
          fvf_size += 4

        texture_count = (fvf & 0xF00) >> 8
        fvf &= ~0xF00
        assert(texture_count <= 4)
        if texture_count > 0:
          fvf_meaning += ["TEX%d" % texture_count]
          fvf_size += 8 * texture_count

      print(fvf_meaning, fvf_size, hex(fvf))
      assert(fvf == 0)
      assert(fvf_size == tmp['vertex_size'])

      assert(tmp['unk0?'] in [1,4])
      assert(tmp['unk2?'] in [0,2,3])
      collect6 += [tmp]
      i += 1

    print(common.offset - offsetx[0], head[7])
    assert(common.offset - offsetx[0] == head[7])

    print("")
    print("Collect7 (Texture configurations)")
    print("")
    collect7 = []
    i = 0
    while((common.offset - offsetx[0]) < head[8]):
      tmp = {}
      tmp['transform_index?'] = read_l(1, silent=True)[0] # index? maybe set of tex-coords?
      tmp['unk0?'] = read_l(1, silent=True)[0] # unknown [flags?]
      print(i, tmp)
      tmp['units'] = []
      for j in range(4):
        tmp_texture = {}
        tmp_texture['unk0?'] = read_l(1, silent=True)[0]
        tmp_texture['unk1?'] = read_l(1, silent=True)[0] # Mostly zero
        tmp_texture['unk2?'] = read_l(1, silent=True)[0] # Almost float or memory address?
        tmp_texture['unknown_f'] = read_f(1, silent=True)[0]
        tmp_texture['texture_index'] = read_l(1, silent=True)[0] # texture index

        print("    unit%d: %s" % (j, tmp_texture))
        tmp['units'] += [tmp_texture]

        #print("0x%08X, #WTFREMOVEME" % tmp_texture['unk0?'])
        assert(tmp_texture['unk0?'] in [
0x00000000,
0x00089000,
0x00089001,
0x00089008,
0x0008A000,
0x00091000,
0x00092000,
0x00099000,
0x0009A000,
0x0009B000,
0x0009B001,
0x0009B002,
0x0009B008,
0x0009B100,
0x000C9000,
0x000C9001,
0x000CB000,
0x000DB000,
0x00289000,
0x00289001,
0x00289004,
0x00289008,
0x0028A000,
0x0028A001,
0x0028B000,
0x00292000,
0x00292001,
0x00299000,
0x0029A000,
0x0029B000,
0x0029B001,
0x0029B002,
0x0029B008,
0x0029B100,
0x002C9000,
0x00489000,
0x00489001,
0x00489008,
0x0048A000,
0x0048B000,
0x00491000,
0x00492000,
0x00499000,
0x0049A000,
0x0049B000,
0x0049B002,
0x0049B008,
0x004C9000,
0x004DB000,
0x00C89000,
0x06099000,
0x06289000,
0x06299000,
0x0629B000,
0x06489000,
0x10089000,
0x10089001,
0x1009B000,
0x100C9000,
0x10289000,
0x10489000,
0x10889000,
0x10A89000,
0x10C89000,
0x14C89000,
])

        #assert(tmp_texture['unk2?'] % 0x200000 == 0) # Broken by 0xBF333333, 0xBF4CCCCD
        assert(tmp_texture['unk2?'] in [0x00000000, 0xBF000000, 0xBF333333, 0xBF4CCCCD, 0xBF800000, 0xBFC00000, 0xC0000000, 0xC0200000, 0xC0400000, 0xC0600000, 0xC0800000])

      assert(tmp['transform_index?'] < head2[2])
      collect7 += [tmp]
      i += 1

    print(common.offset - offsetx[0], head[8])
    assert(common.offset - offsetx[0] == head[8])

    print("")
    print("Collect8 (Transforms?)")
    print("")
    collect8 = []
    for i in range(head2[2]):
      tmp = {}
      tmp['unk0?'] = read_f(4, silent=True, comment=str(head[9:])) # Quaternion? Color?
      tmp['scale?'] = read_f(3, silent=True) # Scale?
      tmp['zero0?'] = read_l(1, silent=True)[0] # Always zero?
      tmp['bias?'] = read_f(3, silent=True) # Some bias?
      tmp['zero1?'] = read_l(1, silent=True)[0] # Always zero?
      tmp['scale2?'] = read_f(3, silent=True)
      tmp['unk2?'] = read_l(1, silent=True)[0]
      tmp['scale_factor?'] = read_f(1, silent=True)[0] # 20.0?
      print(i, tmp)
      assert(tmp['zero0?'] == 0)
      assert(tmp['zero1?'] == 0)
      collect8 += [tmp]

    #111916

    print(head)

    print(common.offset - offsetx[0])
    print(common.offset)

    if False:
      if len(matrices) > 0:
        print()
        print("Matrices 2")
        print()
        read_l(1)
        for i in range(len(matrices)):
          print(i)
          read_f(4)
          read_f(4)
          read_f(4)
          read_f(4)

        print()


    print("objects: %d" % len(objects))
    print("matrices: %d" % len(matrices))

    print("collect2: %d" % len(collect2))
    print("collect3: %d" % len(collect3))


    print("collect4: %d" % len(collect4))
    print("collect5: %d" % len(collect5))

    print("collect6: %d" % len(collect6))
    print("collect7: %d" % len(collect7))
    print("collect8: %d" % len(collect8))

    print()
    print(common.offset, "hex: 0x%X" % common.offset)

    print()

    print(va,vb,vc)

    count1 = (vc - va) // 4
    count2 = (va - vb) // 0x10
    assert(count1 == count2)
    assert(count1 == head2[0])


    if True:

      print()
      common.offset = vb + 0x10
      print("Vertex buffers", common.offset)
      #FIXME: Use all loop members
      ptrass = []
      for i in range(head2[0]):
        ptra,a1,a2,a3 = read_l(4) # offset to list + 3x zero
        assert(a1 == 0)
        assert(a2 == 0)
        assert(a3 == 0)

        # Vertices
        common.push()
        common.offset = ptra + 0x10
        ptras = read_l(3)
        assert(ptras[0] == 0)
        assert(ptras[2] == 0)
        common.pop()

        ptrass += [ptras[1]]

      print()
      common.offset = va + 0x10
      print("Index buffers", common.offset)
      #FIXME: Use all loop members
      ptrbss = []
      for i in range(head2[0]):

        ptrb = read_l(1)[0] # offset to list

        # Indices
        common.push()
        common.offset = ptrb + 0x10
        ptrbs = read_l(3)
        assert(ptrbs[0] == 0)
        assert(ptrbs[2] == 0)
        common.pop()

        ptrbss += [ptrbs[1]]


      if True:
          
        print()
        print("Exporting")

        real_offset = common.offset         

        obj_v_index = 1
        obj_vt_index = 1
        obj_vn_index = 1
        fo = open("/tmp/or2/%s/cs___smt/offset-0x%X.obj" % (filename, offsetx[0]), "wb")
        fo.write(b"s 1\n")
        fo.write(b"mtllib ../xpr/xpr.mtl\n")

        def sanitize(f):
          if math.isnan(f):
            return 0.0 #FIXME: WHY?!
          return f

        def export_mesh(draw_type, fvf, draw_count, vertex_buf_size, index_buf_size, vertex_size, vertex_ptr, index_ptr):
          global fo
          global obj_v_index
          global obj_vt_index
          global obj_vn_index

          real_offset = common.offset

          #vertex_size = 24

          print(vertex_buf_size, vertex_size)
          assert(vertex_buf_size % vertex_size == 0)
          vertex_count = vertex_buf_size // vertex_size

          assert(index_buf_size % 2 == 0)
          index_count = index_buf_size // 2

          #FIXME: Fix <SPECIAL> mode
          if fvf == 0:
            assert(False)

          has_normal = False
          has_texture = False

          #FIXME: Where to get the vertex count?
          common.offset = vertex_ptr
          for i in range(vertex_count):

            fo.write(b"# %d %d 0x%X\n" % (common.offset, vertex_size, fvf))

            p = read_f(3, silent=True)
            fo.write(b"v %f %f %f\n" % p)

            if True:

              #FIXME: Weight betas support
              if fvf & 0xE == 0x2:
                betas = 0
              elif fvf & 0xE == 0x6:
                betas = 1
              elif fvf & 0xE == 0x8:
                betas = 2
              elif fvf & 0xE == 0xA:
                betas = 3
              else:
                assert(False)

              for j in range(betas):
                read_f(1, silent=True)[0]

              if fvf & 0x10:
                n = read_l(1, silent=True)[0]
                nx = (n >> 0) & ((1 << 11) - 1)
                ny = (n >> 11) & ((1 << 11) - 1)
                nz = (n >> 22) & ((1 << 10) - 1)
                nx -= (nx & (1 << 10)) << 1
                ny -= (ny & (1 << 10)) << 1
                nz -= (nz & (1 << 9)) << 1
                nz = nz * 2
                fo.write(b"vn %d %d %d\n# 0x%08X\n" % (nx,ny,nz,n))
                has_normal = True

              if fvf & 0x40:
                #FIXME: Diffuse color
                read_l(1, silent=True)

              texture_count = (fvf & 0xF00) >> 8
              for j in range(texture_count):
                u, v = read_f(2, silent=True)
                if j == tex_unit_index:
                  pass
                  fo.write(b"vt %f %f\n" % (sanitize(u), sanitize(v)))
                  has_texture = True
            else:
              read_l((vertex_size - 12) // 4, silent=True)
              

          def emit_index(i):
            global fo
            fo.write(b" %d" % (obj_v_index+i))

            if has_texture:
              fo.write(b"/%d" % (obj_vt_index+i))
            else:
              if has_normal:
                fo.write(b"/")

            if has_normal:    
              fo.write(b"/%d" % (obj_vn_index+i))      
          
          def emit_face(ls):
            global fo
            fo.write(b"f")
            for l in ls:
              emit_index(l)
            fo.write(b"\n")

          #FIXME: Display the full index buffer?
          common.offset = index_ptr
          indices = read_h(index_count, silent=True)
          if False:
            pass
          elif draw_type == 5:
            #FIXME: Untested
            for i in range(draw_count//3):
              emit_face([indices[3*i+0], indices[3*i+1], indices[3*i+2]])
          elif draw_type == 6:
            for i in range(draw_count): #FIXME: Is this 1/2 too many?
              if i % 2:
                emit_face([indices[1+i], indices[0+i], indices[2+i]])
              else:
                emit_face([indices[0+i], indices[1+i], indices[2+i]])
          elif draw_type == 8:
            #FIXME: Untested
            for i in range(draw_count//4):
              emit_face([indices[4*i+0], indices[4*i+1], indices[4*i+2], indices[4*i+3]])

          obj_v_index += vertex_count
          if has_texture:
            obj_vt_index += vertex_count
          if has_normal:
            obj_vn_index += vertex_count

          common.offset = real_offset

        # Use draw call information

        for _i2 in range(len(collect2)):
          i2 = _i2

          unk_collect2 = collect2[i2]

          for _i3 in range(unk_collect2['a_count?']):
            i3 = unk_collect2['a_collect3_index?'] + _i3

            unk_collect3 = collect3[i3]

            #FIXME: Also do for b_count?
            for l4 in ['a','b']:
              for _i4 in range(unk_collect3[l4 + '_count?']):
                i4 = unk_collect3[l4 + '_collect4/5_index?'] + _i4
                unk_collect4 = collect4[i4]

                i5 = unk_collect4['collect5_index?']
                i6 = unk_collect3['collect6_index?']
                i7 = unk_collect4['collect7_index?']

                mesh = collect6[i6]
                draw_call = collect5[i5]
                textures = collect7[i7]

                vb = data_base + ptrass[i6]
                ib = ptrbss[i6] + 0x10

                print()
                print("vertices:", vb)
                print("indices:", ib)

                #FIXME: Handle transform
                fo.write(b"usemtl texture-%d\n" % (textures['units'][tex_unit_index]['texture_index']))

                #assert(draw_call['index_offset'] == 0)
                #assert(draw_call['unk0?'] == 0x697)

                ib_skip = draw_call['index_offset'] * 2
                vb_skip = mesh['vertex_size'] * unk_collect4['vertex_offset']

                print(collect6)
                fo.write(("o collect2[%s];collect3[%s];collect4%s[%s]\n" % (i2, i3, l4, i4)).encode('ascii'))
                export_mesh(draw_call['primitive_type'], mesh['fvf?'], draw_call['index_count'], mesh['vb_size'] - vb_skip, mesh['ib_size'] - ib_skip, mesh['vertex_size'], vb + vb_skip, ib + ib_skip)

        common.offset = real_offset


    print()

    #assert(len(collect2) == len(collect3))
    #assert((len(objects) + len(matrices)) == len(collect3))
    #assert(len(collect2) == head[9])
    assert(len(collect4) == len(collect5))
    assert(len(collect6) == head2[0])
    assert(len(collect7) == head2[1])
    assert(len(collect8) == head2[2])

    if export_tags:
      common.export_tags("/tmp/or2/%s/decompressed.bin.tags" % (filename))

    if len(matrices) > 0:
      fo = open("/tmp/or2/%s/cs___smt/matrices.dae" % (filename), "wb")
      fo.write(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
      fo.write(b"<COLLADA xmlns=\"http://www.collada.org/2005/11/COLLADASchema\" version=\"1.4.1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
      fo.write(b"  <asset>\n")
      fo.write(b"    <up_axis>Y_UP</up_axis>\n")
      fo.write(b"  </asset>\n")
      fo.write(b"  <library_visual_scenes>\n")
      fo.write(b"    <visual_scene id=\"Scene\" name=\"Scene\">\n")
      for i, matrix in enumerate(matrices):     
        fo.write(b"      <node id=\"Empty\" name=\"Matrix%d\" type=\"NODE\">\n" % i)
        fo.write(b"<matrix sid=\"transform\">\n")
        fo.write(b"%f %f %f %f\n" % (matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0]))
        fo.write(b"%f %f %f %f\n" % (matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1]))
        fo.write(b"%f %f %f %f\n" % (matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2]))
        fo.write(b"%f %f %f %f\n" % (matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3]))
        fo.write(b"</matrix>\n" )
        fo.write(b"      </node>\n")
      fo.write(b"    </visual_scene>\n")
      fo.write(b"  </library_visual_scenes>\n")
      fo.write(b"  <scene>\n")
      fo.write(b"    <instance_visual_scene url=\"#Scene\"/>\n")
      fo.write(b"  </scene>\n")
      fo.write(b"</COLLADA>\n")


