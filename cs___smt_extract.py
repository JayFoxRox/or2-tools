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

def cs___smt_extract(f):

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


    va = offsetx[3]
    vb = offsetx[4]
    vc = offsetx[5]
    vd = offsetx[6]

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

    print("")
    print("%d %d" % (head[0], counta))
    print("")

    if False:
      if head[0] != 0x30:
        print("bad offset: 0x%X" % offsetx[0])
        continue

    # This suggests that these are independent files
    assert(head[0] == 0x30)



    objects = []
    print("")
    print("Objects ? (collect1)")
    print("")
    print(common.offset - offsetx[0], head[0])
    assert(common.offset - offsetx[0] == head[0])
    i = 0
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
                                    0x021,      0x023,      0x026,            0x02A,
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

    assert(tmp['collect1_index?'] == 0xFFFFFFFF)

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
      tmp['unk0?'] = read_l(1, silent=True)[0]
      tmp['a_collect4/5_index1?'] = read_l(1, silent=True)[0] # Optional index into collect4/5?
      tmp['b_collect4/5_index2?'] = read_l(1, silent=True)[0] # Optional index into collect4/5?
      tmp['a_count?'] = read_l(1, silent=True)[0]
      tmp['b_count?'] = read_l(1, silent=True)[0]
      print(i, tmp)
      assert(tmp['unk0?'] in [0,1,2,3,4])
      assert(tmp['a_count?'] in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,24,25,26,27,28,29,30,31,32,64])
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
      tmp['unk0?'] = read_l(1, silent=True)[0] # index offset like collect5 [but different splits?]
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

        if fvf & 0x2:
          fvf &= ~0x2
          fvf_meaning += ["XYZ"]
          fvf_size += 4*3

        #FIXME: Seems to be bone related?
        if fvf & 0x4:
          fvf &= ~0x4
          fvf_meaning += ["XYZW?"]
          fvf_size += 4 #FIXME: Should be 16, but somehow happens with XYZ?

        #FIXME: Seems to be bone related?
        if fvf & 0x8:
          fvf &= ~0x8
          fvf_meaning += ["XYZB2?"]
          fvf_size += 4*3 #FIXME: Should only be 2 floats?
          if not "XYZ" in fvf_meaning:
            fvf_size += 4*2

        if fvf & 0x10:
          fvf &= ~0x10
          fvf_meaning += ["NORMAL?"]
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

        print("    unit%d: %s" % (j, tmp_texture))
        tmp['units'] += [tmp_texture]
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

    if False:

      for i in range(head[9]):
        print(i)
        print("vb_ptr", offsetx[0] + collect6[i]['vb_ptr'])
        print("ib_ptr", offsetx[0] + collect6[i]['ib_ptr'])

      print("vertices:", data_base + ptras[1])
      print("indices:", 16 + ptrbs[1])


    if False:

      if True:
        i = 0
        common.offset = offsetx[0] + collect6[i]['ib_ptr']
        print("Vertex buffers via index buffer pointer", common.offset, "(%d)" % collect6[i]['ib_ptr'])



      if True:

        print("fixup ", fixup, " for ", filename)
        print(head)

        #FIXME: This is *bad*; how to fix this?
        print("Searching vb and ib pointers at ", common.offset, " (0x%X)" % common.offset)
        while read_h(1)[0] == 0:
          pass
        common.offset -= 2
        print("Done searching vb and ib pointers at ", common.offset, " (0x%X)" % common.offset)


      if True:

        print()
        print("Vertex buffers", common.offset)
        #FIXME: Use all loop members
        for i in range(head[9]):
          ptra,a1,a2,a3 = read_l(4) # offset to list + 3x zero
          assert(a1 == 0)
          assert(a2 == 0)
          assert(a3 == 0)

          # Vertices
          common.push()
          common.offset = ptra + 16
          ptras = read_l(3)
          assert(ptras[0] == 0)
          assert(ptras[2] == 0)
          common.pop()

        print()
        print("Index buffers", common.offset)
        #FIXME: Use all loop members
        for i in range(head[9]):

          ptrb = read_l(1)[0] # offset to list

          # Indices
          common.push()
          common.offset = ptrb + 16
          ptrbs = read_l(3)
          assert(ptrbs[0] == 0)
          assert(ptrbs[2] == 0)
          common.pop()

        vb = data_base + ptras[1]
        ib = 16 + ptrbs[1]
      else:
        vb = None
        ib = None

      print()
      print("vertices:", vb)
      print("indices:", ib)

      if True:
          
        print()
        print("Exporting")

        real_offset = common.offset

        def export_mesh(path, draw_type, draw_count, vertex_buf_size, index_buf_size, vertex_size, vertex_ptr, index_ptr):

          real_offset = common.offset

          fo = open(path, "wb")

          #vertex_size = 24

          print(vertex_buf_size, vertex_size)
          assert(vertex_buf_size % vertex_size == 0)
          vertex_count = vertex_buf_size // vertex_size

          assert(index_buf_size % 2 == 0)
          index_count = index_buf_size // 2

          #FIXME: Where to get the vertex count?
          common.offset = vertex_ptr
          for i in range(vertex_count):
            v = read_f(3, silent=True)
            read_l((vertex_size - 12) // 4, silent=True)
            fo.write(b"v %f %f %f\n" % v)

          #FIXME: Display the full index buffer?
          common.offset = index_ptr
          indices = read_h(index_count, silent=True)
          if False:
            pass
          elif draw_type == 5:
            #FIXME: Untested
            for i in range(draw_count//3):
              fo.write(b"f %d %d %d\n" % (1+indices[3*i+0], 1+indices[3*i+1], 1+indices[3*i+2]))
          elif draw_type == 6:
            for i in range(draw_count): #FIXME: Is this 1/2 too many?
              if i % 2:
                fo.write(b"f %d %d %d\n" % (1+indices[1+i], 1+indices[0+i], 1+indices[2+i]))
              else:
                fo.write(b"f %d %d %d\n" % (1+indices[0+i], 1+indices[1+i], 1+indices[2+i]))
          elif draw_type == 8:
            #FIXME: Untested
            for i in range(draw_count//4):
              fo.write(b"f %d %d %d %d\n" % (1+indices[4*i+0], 1+indices[4*i+1], 1+indices[4*i+2], 1+indices[4*i+3]))


          common.offset = real_offset

        # Use draw call information

        unk_collect4 = collect4[0]
        draw_call = collect5[0]
        mesh = collect6[0]
        textures = collect7[0]

        assert(draw_call['index_offset'] == 0)
        #assert(draw_call['unk0?'] == 0x697)

        print(collect6)
        export_mesh("/tmp/or2/%s/cs___smt/draw-call-0x%X.obj" % (filename, real_offset), draw_call['primitive_type'], draw_call['index_count'], mesh['vb_size'], mesh['ib_size'], mesh['vertex_size'], vb, ib)

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


