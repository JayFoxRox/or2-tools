#!/usr/bin/env python

try:
  import bpy
  import bmesh
  from bpy_extras import object_utils
  import mathutils
  export_blender = True
except:
  print("Blender export disabled")
  export_blender = False

import sys
import struct
import math
import os

sys.setrecursionlimit(10000)

from . import common
read_f = common.read_f
read_l = common.read_l
read_h = common.read_h
read_b = common.read_b

export_tags = True
export_objs = True

filename = None















def export_mesh(bm, draw_type, draw_count, indices, vertices):
  known_vertices = {}

  def emit_vertex(i):
    # Use cache for indices which have been exported already
    if i in known_vertices:
      return known_vertices[i]
    v = bm.verts.new(vertices[i]['position'])            
    known_vertices[i] = v
    return v

  def emit_face(ls):
    #if len(ls) != len(set(ls)):
    #  print("degenerate face", draw_type, ls)
    #  #assert(len(ls) == 3)
    #  return
    try:
      bm.faces.new(emit_vertex(l) for l in ls)
    except:
      print("some error during face creation")
    return

  
  if draw_type == 5:
    for i in range(draw_count):
      emit_face([indices[3*i+0], indices[3*i+1], indices[3*i+2]])
  elif draw_type == 6:
    for i in range(draw_count): #FIXME: Is this 1/2 too many?
      if i % 2:
        emit_face([indices[1+i], indices[0+i], indices[2+i]])
      else:
        emit_face([indices[0+i], indices[1+i], indices[2+i]])
  elif draw_type == 8:
    for i in range(draw_count):
      emit_face([indices[4*i+0], indices[4*i+1], indices[4*i+2], indices[4*i+3]])
  else:
    assert(False)

  bm.verts.ensure_lookup_table() # Required after adding / removing vertices and before accessing them by index.
  bm.verts.index_update()  # Required to actually retrieve the indices later on (or they stay -1).

  # Get the blender vertex index for each vertex
  known_vertices_i = {v.index:i for i,v in known_vertices.items()}

  # Set the UV coordinates by iterating through the face loops.
  if 'diffuse' in vertices[0]:
    diffuse_layer = bm.loops.layers.color.new("diffuse")
  uv_layers = [bm.loops.layers.uv.new("texture-%d" % i) for i in range(len(vertices[0]['uv']))]
  for face in bm.faces:
    for loop in face.loops:
      v = vertices[known_vertices_i[loop.vert.index]]
      for i,uv in enumerate(v['uv']):
        loop[uv_layers[i]].uv = uv
      if 'diffuse' in vertices[0]:
        loop[diffuse_layer] = [v['diffuse'][i] / 255.0 for i in [2,1,0,3]]

  #FIXME: Not working yet - this is a bit more complicated
  # Add vertex weights
  #dl = bm.verts.layers.deform.verify()
  #groups = [bm.vertex_groups.new("weight-%d" % i) for i in range(len(vertices[0]['beta']))]
  #for i,v in known_vertices_i.items():
  #  for j,beta in enumerate(vertices[v]['beta']):
  #    bm.verts[i][dl][groups[j].index] = beta

  return
























def read_object():
  tmp = {}

  tmp['unk0_flags?'] = read_l(1, silent=True)[0] # 0x442 = skidmarks?
  tmp['position'] = read_f(3, silent=True)
  tmp['unk1?'] = read_f(1, silent=True)[0]
  tmp['unk2?'] = read_l(2, silent=True)
  tmp['matrix_index?'] = read_l(1, silent=True)[0] # Optional matrix index?
  tmp['collect1_index1?'] = read_l(1, silent=True)[0]
  tmp['collect1_index2?'] = read_l(1, silent=True)[0] # index to next object?
  tmp['collect2_index?'] = read_l(1, silent=True)[0]
  tmp['collect2_indices?'] = read_l(3, silent=True) # More optional indices?

  if False:
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
  #print("WTF", tmp['unk1?'])

  #assert(tmp['unk3a?'] == 0xFFFFFFFF)

  assert(tmp['collect2_indices?'][0] <= tmp['collect2_indices?'][1])
  assert(tmp['collect2_indices?'][1] <= tmp['collect2_indices?'][2])
  if tmp['collect2_indices?'] != tuple([0xFFFFFFFF]*3):
    pass #print("WTF", tmp['collect2_indices?'])

  return tmp

def read_collect3():
  tmp = {}
  tmp['collect6_index?'] = read_l(1, silent=True)[0]
  tmp['a_collect4_index?'] = read_l(1, silent=True)[0] # Optional index into collect4?
  tmp['b_collect4_index?'] = read_l(1, silent=True)[0] # Optional index into collect4?
  tmp['a_count?'] = read_l(1, silent=True)[0]
  tmp['b_count?'] = read_l(1, silent=True)[0]
  return tmp

def read_drawcall():
  tmp = {}
  tmp['primitive_type'] = read_l(1, silent=True)[0] # Type of draw call? [assert 6]
  tmp['index_offset'] = read_l(1, silent=True)[0] # Index offset?
  tmp['index_count'] = read_l(1, silent=True)[0] # Count of indices in draw call
  tmp['unk0?'] = read_l(1, silent=True)[0] # unknown [similar to count of indices] # Count of unique vertices?
  if tmp['primitive_type'] == 5:
    assert(tmp['unk0?'] == tmp['index_count'])
  elif tmp['primitive_type'] == 8:
    assert(tmp['unk0?'] == tmp['index_count'])
  elif tmp['primitive_type'] == 6:
    assert(tmp['unk0?'] <= tmp['index_count'])
    pass #assert([ tmp['index_count'], tmp['unk0?']] in [[25,20], [2,2], [144,96], [218,144], [70,48], [211,145], [864,412], [79,43], [10,6], [89,48], [21,16], [205,116], [87,45], [93,45]])
  else:
    print(tmp)
    #assert(False)
  return tmp

def read_texture():
  tmp = {}
  tmp['transform_index?'] = read_l(1, silent=True)[0] # index? maybe set of tex-coords?
  tmp['unk0?'] = read_l(1, silent=True)[0] # unknown [flags?]
  print(tmp)
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
    if filename[-7:].upper() == "_SMT.GZ":
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

  return tmp


def read_transform():
  #OR2006 format:
  #read_f(4)

  #read_f(3)
  #read_l(1)

  #read_f(3)
  #read_l(5)

  #read_f(1)
  #read_l(1)

  tmp = {}
  tmp['unk0?'] = read_f(4, silent=True) # Quaternion? Color?

  tmp['scale?'] = read_f(3, silent=True) # Scale?
  tmp['zero0?'] = read_l(1, silent=True)[0] # Always zero?

  tmp['bias?'] = read_f(3, silent=True) # Some bias?
  tmp['zero1?'] = read_l(1, silent=True)[0] # Always zero?

  tmp['scale2?'] = read_f(3, silent=True)
  tmp['unk2?'] = read_l(1, silent=True)[0]

  tmp['scale_factor?'] = read_f(1, silent=True)[0] # 20.0?

  if filename[-7:].upper() == "_PMT.SZ":
    tmp['unk3?'] = read_l(1, silent=True)[0]
    print(tmp['unk3?'])
    assert(tmp['unk3?'] in (0, 0xBF800000, 0xFFFFFFFF))
  
  if filename[-7:].upper() == "_SMT.GZ":
    #FIXME: These appear to be floats in OR2006
    assert(tmp['zero0?'] == 0)
    assert(tmp['zero1?'] == 0)
  return tmp


def cs___smt_extract(f):
  global filename

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
      print(vg - ve)
      if filename[-7:].upper() == "_SMT.GZ":
        assert(vg == ve + 0x30)

      vh, vi, vj, vk, vl, vm, vn = read_l(7)

      vo = read_l(1)[0] # Always zero
      assert(vo == 0)

      offsets += [(ve + 0x10, vg + 0x10, va, vb, vc, vd)]

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


  result_list = []

  for offseti, offsetx in enumerate(offsets):

    result = {}

    print()
    print()
    print()

    print("element %d" % offseti)

    print()
    print()
    print()

    header_offset = offsetx[0]
    data_offset = offsetx[1]

    index_buffer_ptr = offsetx[2] # [middle] Some start pointer?
    vertex_buffer_ptr = offsetx[3] # [lowest] Some start pointer? 0x10 bytes for each element between middle and highest?
    unk_xxx = offsetx[4] # [highest] Some end pointer [+4 / +8 on va?]
    unk_d = offsetx[5] #FIXME: Use after figuring out what this is

    print(unk_xxx, unk_d)
    #assert(unk_d == 0)

    common.offset = header_offset



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

    if filename[-7:].upper() == "_SMT.GZ":
      groups_list = (head[0],head[1])
      matrices_list = (head[1],head[2])
      collect2_list = (head[2],head[3])
      collect3_list = (head[3],head[4])
      collect4_list = (head[4],head[5])
      collect5_list = (head[5],head[6])
      collect6_list = (head[6],head[7])
      collect7_list = (head[7],head[8])
      collect8_list = (head[8],)
    elif filename[-7:].upper() == "_PMT.SZ":
      groups_list = (head[0],head[2]) #0
      matrices_list = (head[1],) #1
      collect2_list = (head[2],head[3]) #2
      collect3_list = (head[3],head[4]) #3
      collect4_list = (head[4],head[5]) #4
      collect5_list = (head[5],head[7]) #5
      collect6_list = (head[6],) #6
      collect7_list = (head[7],head[8]) #7
      collect8_list = (head[8],head[6]) #8
      #FIXME: head[1] follows in order
    else:
      assert(False)
    

    # global-header for this offset: [...some fields not in local header...]
    #                                00000914;         0000094C;00000954;00000968;00000978;00000988;000009B4;00000A0C
    # local-header in `head`:        00000030;00000068;00000068;00000070;00000084;00000094;000000A4;000000D0;00000128
    #                                00000001;00000001;00000001
    # So this local header is just the same


    if False:
      if head[0] != 0x30:
        print("bad offset: 0x%X" % offsetx[0])
        continue

    # This suggests that these are independent files
    if filename[-7:].upper() == "_SMT.GZ":
      assert(head[0] == 0x30)
    elif filename[-7:].upper() == "_PMT.SZ":

      newc = read_l(1)[0] # FIXME: part of the real head
      print()
      for i in range(len(offsets) - offseti - 1):
        read_l(9) # Read next head?
        read_l(3)
        read_l(1)
        print()
      print(common.offset)

      print(head2)
      head2 = list(head2)
      head2 = [head2[0],
               head2[2],
               newc,
               head2[1]]
      head2 = tuple(head2)
      print(head2)

      offsetx = list(offsetx)
      offsetx[0] = 0x10
      offsetx = tuple(offsetx)

    else:
      assert(False)


    #FIXME: Finds OBJ_COURSE_OBJ_CS_1A_R_SMT.GZ:
    # head1: 00000030;00000068;00000068;00000068;00000068;00000068;00000068;00000068;00000068
    # head2: 00000000;00000000;00000000
    if (list(head2) == [0]*3):
      print("Broken object?!")
      continue

    common.offset = data_offset

    groups = []
    print("")
    print("groups ? (collect1)")
    print("")
    print(common.offset - offsetx[0], groups_list[0])
    assert(common.offset - offsetx[0] == groups_list[0])
    i = 0
    tmp = None
    while((common.offset - offsetx[0]) < groups_list[1]):
      tmp = read_object()
      print(hex(tmp['unk0_flags?']))
      print(i, tmp)
      groups += [tmp]
      i += 1
    print(common.offset - offsetx[0], groups_list[1])
    assert(common.offset - offsetx[0] == groups_list[1])
    result['groups'] = groups




    if filename[-7:].upper() == "_SMT.GZ":
      print(common.offset - offsetx[0], matrices_list[0])
      assert(common.offset - offsetx[0] == matrices_list[0])

      print(matrices_list[1], matrices_list[0])
      max_matrix = (matrices_list[1] - matrices_list[0]) // ((4*4)*4) - 1
    elif filename[-7:].upper() == "_PMT.SZ":
      max_matrix = -1
      for o in groups:
        if tmp['matrix_index?'] != 0xFFFFFFFF:
          max_matrix = max(max_matrix, tmp['matrix_index?'])

      common.push()
      common.offset = offsetx[0] + matrices_list[0]

    else:
      assert(False)

    matrices = []
    print("")
    print("Matrices?")
    print("")
    for i in range(max_matrix + 1):
      print(i)
      tmp = []
      tmp += [read_f(4)]
      tmp += [read_f(4)]
      tmp += [read_f(4)]
      tmp += [read_f(4)]
      matrices += [tmp]
    #assert(head[1] == head[2])
    if filename[-7:].upper() == "_SMT.GZ":
      print(common.offset - offsetx[0], matrices_list[1])
      assert(common.offset - offsetx[0] == matrices_list[1])
    elif filename[-7:].upper() == "_PMT.SZ":
      common.pop()
    else:
      assert(False)
    result['matrices'] = matrices




    print("")
    print("Collect2")
    print("")
    collect2 = []
    print(common.offset - offsetx[0], collect2_list[0])
    assert(common.offset - offsetx[0] == collect2_list[0])
    i = 0
    while((common.offset - offsetx[0]) < collect2_list[1]):
      tmp = {}
      tmp['a_collect3_index?'] = read_l(1, silent=True)[0] # Index into collect3?
      tmp['a_count?'] = read_l(1, silent=True)[0]
      print(i, tmp)
      #assert(tmp['a_count?'] in [1,2,3,5])
      collect2 += [tmp]
      i += 1
    result['objects'] = collect2

    print("")
    print("Collect3")
    print("")
    collect3 = []
    print(common.offset - offsetx[0], collect3_list[0])
    assert(common.offset - offsetx[0] == collect3_list[0])
    i = 0
    while((common.offset - offsetx[0]) < collect3_list[1]):
      tmp = read_collect3()
      print(i, tmp)
      collect3 += [tmp]
      i += 1
    result['batches'] = collect3

    print(common.offset - offsetx[0], collect4_list[0])
    assert(common.offset - offsetx[0] == collect4_list[0])
    print("")
    print("Collect4 (Mesh?)")
    print("")
    collect4 = []
    i = 0
    while((common.offset - offsetx[0]) < collect4_list[1]):
      tmp = {}
      tmp['vertex_offset'] = read_l(1, silent=True)[0] # index offset like collect5 [but different splits?]
      tmp['collect7_index?'] = read_l(1, silent=True)[0]
      tmp['collect5_index?'] = read_l(1, silent=True)[0] # Index into collect5?
      tmp['unk3_boolean?'] = read_l(1, silent=True)[0] # Some boolean?
      if filename[-7:].upper() == "_PMT.SZ":
        tmp['some_position'] = read_f(3, silent=True)
        tmp['some_radius?'] = read_f(1, silent=True)[0]
        assert(tmp['some_radius?'] > 0.0)
      print(i, tmp)
      #assert(tmp['collect7_index?'] < head2[1]) # Some kind of texture lookup?
      #assert(tmp['unk0?'][2] < head2[1]) # Some kind of texture lookup?
      assert(tmp['unk3_boolean?'] in [0,1,2]) # 2 was only seen in OR2006
      collect4 += [tmp]
      i += 1
    result['parts'] = collect4

    print(head2)

    # Looks like some entries at the end got removed but their space is garbage, so our parser would fail
    max_c5 = 0
    for c4 in collect4:
      max_c5 = max(max_c5, c4['collect5_index?'])

    print("")
    print("Collect5 (Draw calls?)")
    print("")
    collect5 = []
    print(common.offset - offsetx[0], collect5_list[0])
    assert(common.offset - offsetx[0] == collect5_list[0])
    i = 0
    while((common.offset - offsetx[0]) < collect5_list[1]):

      print(common.offset - offsetx[0], collect5_list[1])

      if i > max_c5:
        break

      tmp = read_drawcall()
      print(i, tmp)
      collect5 += [tmp]
      i += 1
    result['drawcalls'] = collect5


    if filename[-7:].upper() == "_SMT.GZ":
      print(common.offset - offsetx[0], collect6_list[0])
      assert(common.offset - offsetx[0] == collect6_list[0])
    elif filename[-7:].upper() == "_PMT.SZ":
      print(common.offset - offsetx[0], collect5_list[1])
      assert(common.offset - offsetx[0] <= collect5_list[1])
      while((common.offset - offsetx[0]) < collect5_list[1]):
        read_l(1)

      common.push()
      common.offset = offsetx[0] + collect6_list[0]
    else:
      assert(False)

    print("")
    print("Collect6 (Draw buffer)")
    print("")
    collect6 = []
    i = 0
    for i in range(head2[0]):

      tmp = {}
      tmp['unk0?'] = read_l(1, silent=True)[0] # vertex buffer count?
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
    result['drawbuffers'] = collect6

    if filename[-7:].upper() == "_SMT.GZ":
      print(common.offset - offsetx[0], collect6_list[1])
      assert(common.offset - offsetx[0] == collect6_list[1])
    elif filename[-7:].upper() == "_PMT.SZ":
      common.pop()
    else:
      assert(False)

    print(common.offset - offsetx[0], collect7_list[0])
    assert(common.offset - offsetx[0] == collect7_list[0])

    print("")
    print("Collect7 (Texture configurations)")
    print("")
    collect7 = []
    i = 0
    while((common.offset - offsetx[0]) < collect7_list[1]):
      print(i)
      tmp = read_texture()
      assert(tmp['transform_index?'] < head2[2])
      collect7 += [tmp]
      i += 1
    result['textures'] = collect7

    print(common.offset - offsetx[0], collect8_list[0])
    assert(common.offset - offsetx[0] == collect8_list[0])

    print(head2)

    print("")
    print("Collect8 (Transforms?)")
    print("")
    collect8 = []
    for i in range(head2[2]):
      tmp = read_transform()
      print(i, tmp)
      collect8 += [tmp]
    result['transforms'] = collect8

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


    vertex_buffers = []

    print()
    common.offset = vertex_buffer_ptr + 0x10
    print("Vertex buffers", common.offset)
    #FIXME: Use all loop members
    ptrass = []
    for i in range(head2[0]):

      #FIXME: add to some list?
      ptra,a1,a2,a3 = read_l(4) # offset to list + 3x zero
      #FIXME: Not zero in OR2006?! [maybe also OR2 - I forgot]
      #assert(a1 == 0)
      #assert(a2 == 0)
      #assert(a3 == 0)

      # Vertices
      common.push()
      common.offset = ptra + 0x10
      tmp = {}
      tmp['zero0?'] = read_l(1, silent=True)[0]
      tmp['offset'] = read_l(1, silent=True)[0]
      tmp['zero1?'] = read_l(1, silent=True)[0]
      assert(tmp['zero0?'] == 0)
      assert(tmp['zero1?'] == 0)
      common.pop()

      vertex_buffers += [tmp]

    result['vertex_buffers'] = vertex_buffers

    print()
    common.offset = index_buffer_ptr + 0x10
    print("Index buffers", common.offset)
    index_buffers = []
    for i in range(head2[0]):

      #FIXME: add to some list?
      ptrb = read_l(1)[0] # offset to list

      # Indices
      common.push()
      common.offset = ptrb + 0x10
      tmp = {}
      tmp['zero0?'] = read_l(1, silent=True)[0]
      tmp['offset'] = read_l(1, silent=True)[0]
      tmp['zero1?'] = read_l(1, silent=True)[0]
      assert(tmp['zero0?'] == 0)
      assert(tmp['zero1?'] == 0)
      common.pop()

      index_buffers += [tmp]
    result['index_buffers'] = index_buffers

    print("groups: %d" % len(groups))
    print("matrices: %d" % len(matrices))

    print("collect2: %d" % len(collect2))
    print("collect3: %d" % len(collect3))


    print("collect4: %d" % len(collect4))
    print("collect5: %d" % len(collect5))

    print("collect6: %d" % len(collect6))
    print("collect7: %d" % len(collect7))
    print("collect8: %d" % len(collect8))


    #assert(len(collect2) == len(collect3))
    #assert((len(groups) + len(matrices)) == len(collect3))
    #assert(len(collect2) == head[9])
    assert(len(collect4) <= len(collect5))
    assert(len(collect6) == head2[0])
    assert(len(collect7) == head2[1])
    assert(len(collect8) == head2[2])

    print()
    print(common.offset, "hex: 0x%X" % common.offset)

    print()

    print(va,vb,vc)

    #FIXME: Broken for OR2006 and mostly unknown for OR2
    count1 = (vc - va) // 4
    count2 = (va - vb) // 0x10
    print(count1, count2, head2[0])
    if filename[-7:].upper() == "_SMT.GZ":
      assert(count1 == count2)
      assert(count1 == head2[0])



    # Decode and cache all indices and vertices
    #FIXME: Move these elsewhere so the output doesn't get ridiculously huge?
    result['indices'] = []
    result['vertices'] = []
    for i6, mesh in enumerate(collect6):

      index_ptr = index_buffers[i6]['offset'] + 0x10
      vertex_ptr = data_base + vertex_buffers[i6]['offset']


      index_buf_size = mesh['ib_size']


      assert(index_buf_size % 2 == 0)
      index_count = index_buf_size // 2
      common.offset = index_ptr
      indices = read_h(index_count, silent=True)
      result['indices'] += [indices]


      fvf = mesh['fvf?']
      vertex_buf_size = mesh['vb_size']
      vertex_size = mesh['vertex_size'] 


      assert(vertex_buf_size % vertex_size == 0)
      vertex_count = vertex_buf_size // vertex_size

      #FIXME: Fix <SPECIAL> mode [44 bytes]
      #FIXME: This should have the right size, but it will probably still be bad
      if fvf == 0:
        fvf = 0x2 | 0x10 | 0x40 | 0x300 #FIXME: Guesswork

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

      texture_count = (fvf & 0xF00) >> 8

      has_normal = fvf & 0x10
      has_diffuse = fvf & 0x40

      vertices = []

      #FIXME: Where to get the vertex count?
      common.offset = vertex_ptr
      for i in range(vertex_count):

        vertex = {}

        p = read_f(3, silent=True)
        vertex['position'] = p

        vertex['beta'] = []
        for j in range(betas):
          #FIXME: Support beta weights
          beta = read_f(1, silent=True)[0]
          vertex['beta'] += [beta]

        if has_normal:
          n = read_l(1, silent=True)[0]
          nx = (n >> 0) & ((1 << 11) - 1)
          ny = (n >> 11) & ((1 << 11) - 1)
          nz = (n >> 22) & ((1 << 10) - 1)
          nx -= (nx & (1 << 10)) << 1
          ny -= (ny & (1 << 10)) << 1
          nz -= (nz & (1 << 9)) << 1
          nz = nz * 2
          vertex['normal'] = (nx,ny,nz,n)

        if has_diffuse:
          #FIXME: Diffuse color
          vertex['diffuse'] = read_b(4, silent=True)

        vertex['uv'] = []
        for j in range(texture_count):
          u, v = read_f(2, silent=True)
          vertex['uv'] += [(u,v)]
        vertices += [vertex]
      result['vertices'] += [vertices]


    result_list += [result]


  # Now try to export all data
  for offseti, result in enumerate(result_list):

    groups = result['groups']
    matrices = result['matrices']
    collect2 = result['objects']
    collect3 = result['batches']
    collect4 = result['parts']
    collect5 = result['drawcalls']
    collect6 = result['drawbuffers']
    collect7 = result['textures']
    vertex_buffers = result['vertex_buffers']
    index_buffers = result['index_buffers']


    # Export group offsets
    if export_objs:
      fo = open("/tmp/or2/%s/cs___smt/groups-%d.obj" % (filename, offseti), "wb")
      for i, tmp in enumerate(groups):
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




    # Export actual meshes
    if export_blender:

      print()
      print("Exporting")

      # Create a collection for the object
      master_coll = bpy.context.scene.collection.children[0]
      my_sub_coll = bpy.data.collections.new(name="element-%d" % offseti)
      master_coll.children.link(my_sub_coll)

      # Process groups
      def process_group(i1, origin):
        unk_collect1 = groups[i1]

        my_sub_coll1 = bpy.data.collections.new(name="%s/groups[%d]" % (origin,i1))
        my_sub_coll.children.link(my_sub_coll1)

        print(offseti, len(offsets), ":", i1, len(groups))

        #FIXME: Apply matrix
        im = unk_collect1['matrix_index?']

        #FIXME: Why are these 2 different ones?
        for i2_index, _i2 in enumerate([unk_collect1['collect2_index?']] + list(unk_collect1['collect2_indices?'])):
          i2 = _i2

          if i2 == 0xFFFFFFFF:
            continue

          my_sub_coll2 = bpy.data.collections.new(name="collect2_%d=[%d]" % (i2_index, i2))
          my_sub_coll1.children.link(my_sub_coll2)

          unk_collect2 = collect2[i2]

          for _i3 in range(unk_collect2['a_count?']):
            i3 = unk_collect2['a_collect3_index?'] + _i3

            unk_collect3 = collect3[i3]

            i6 = unk_collect3['collect6_index?']
            mesh = collect6[i6]

            #indices = collect6_cache[i6]['indices']
            #vertices = collect6_cache[i6]['vertices']

            indices = result['indices'][i6]
            vertices = result['vertices'][i6]

            my_sub_coll3 = bpy.data.collections.new(name="collect3=[%d+%d=%d]; %d betas" % (unk_collect2['a_collect3_index?'],_i3,i3, len(vertices[0]['beta'])))
            my_sub_coll2.children.link(my_sub_coll3)

            #FIXME: Also do for b_count?
            for l4 in ['a','b']:
              for _i4 in range(unk_collect3[l4 + '_count?']):
                i4 = unk_collect3[l4 + '_collect4_index?'] + _i4
                unk_collect4 = collect4[i4]

                i5 = unk_collect4['collect5_index?']
                i7 = unk_collect4['collect7_index?']

                #FIXME: Set blender material somehow
                #activeObject = bpy.context.active_object #Set active object to variable
                #mat = bpy.data.materials.new(name="texture-%d" % (textures['units'][tex_unit_index]['texture_index'])) #set new material to variable
                #activeObject.data.materials.append(mat) #add the material to the object
                #bpy.context.object.active_material.diffuse_color = (1, 0, 0) #change color

                draw_call = collect5[i5]
                textures = collect7[i7]

                index_offset = draw_call['index_offset']
                vertex_offset = unk_collect4['vertex_offset']


                #FIXME: Handle transform
                #fo.write(b"usemtl texture-%d\n" % (textures['units'][tex_unit_index]['texture_index']))

                #assert(draw_call['index_offset'] == 0)
                #assert(draw_call['unk0?'] == 0x697)

                mesh_name = "c4%s[%s];c5[%s];c6[%s];c7[%s]" % (l4, i4, i5, i6, i7)

                # Start a new object
                blender_mesh = bpy.data.meshes.new("%s" % (mesh_name))
                bm = bmesh.new()

                # Submit actual mesh data to blender
                export_mesh(bm, draw_call['primitive_type'], draw_call['index_count'], indices[index_offset:], vertices[vertex_offset:])

                # Create actual object
                bm.to_mesh(blender_mesh)
                blender_mesh.update()
                foo = object_utils.object_data_add(bpy.context, blender_mesh)

                # Create a material (FIXME: Export these independently?)
                mat = bpy.data.materials.new(name="OR2-Material")
                mat.use_nodes = True
                mat_nodes = mat.node_tree.nodes
                mat_links = mat.node_tree.links
                # a new material node tree already has a diffuse and material output node
                output = mat_nodes['Material Output']
                diffuse = mat_nodes['Principled BSDF']

                for i, texture_unit in enumerate(textures['units']):
                  ti = texture_unit['texture_index']

                  if ti == 0xFFFFFFFF:
                    continue
                                  
                  #FIXME: This might point at the wrong one?
                  uv_node = mat_nodes.new("ShaderNodeUVMap")
                  uv_node.uv_map = "texture-%d" % i

                  node = mat_nodes.new('ShaderNodeTexImage')
                  node.projection = 'FLAT' #FIXME: Box for better interpolation near edges [only for auto-uv]
                  node.projection_blend = 1
                  node.image = bpy.data.images.load("/tmp/or2/%s/xpr/%d-texture.png" % (filename, ti))
                  mat_links.new(uv_node.outputs[0], node.inputs[0])

                  #FIXME: Instead, mix all textures
                  mat_links.new(node.outputs[0], output.inputs[0])

                #FIXME: Respect vertex-color

                # Remove default node and set it up
                mat_nodes.remove(diffuse)
                foo.data.materials.append(mat)

                print(foo)
                if im != 0xFFFFFFFF:
                  foo.matrix_world = matrices[im]

                if True:
                  # Convert from Y-up axis to Z-up axis and scale down
                  s = 0.1
                  foo.matrix_world = mathutils.Matrix([[s,0,0,0],[0,0,-s,0],[0,s,0,0],[0,0,0,1]]) @ foo.matrix_world

                #FIXME: Unlink bpy.context.scene.collection.objects.unlink(foo)
                my_sub_coll3.objects.link(foo)
                master_coll.objects.unlink(foo)

        if unk_collect1['collect1_index1?'] != 0xFFFFFFFF:
          process_group(unk_collect1['collect1_index1?'], 'left')
        if unk_collect1['collect1_index2?'] != 0xFFFFFFFF:
          process_group(unk_collect1['collect1_index2?'], 'right')

      process_group(0, 'root')

      # Done with blender export
      print()


    # Export matrices
    if len(matrices) > 0:
      fo = open("/tmp/or2/%s/cs___smt/matrices-%d.dae" % (filename, offseti), "wb")
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

  if export_tags:
    common.export_tags("/tmp/or2/%s/decompressed.bin.tags" % (filename))

  return result_list
