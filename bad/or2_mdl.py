#!/usr/bin/env python

import sys
import struct

path = sys.argv[1]

# MDL_SPRANI_ADV.GZ after decompression
print("Opening '%s'" % path)

f = open(path, 'rb')
data = f.read()

def read_chunk(offset):
  print("%08X" % offset)
  while True:
    v = struct.unpack_from("<L", data, offset)
    print(offset, "%08X" % v)
    read_chunk(offset)
    if v == 0:
      break
    offset += 4

#read_chunk(0)


offset = 0x28

def read_l(count):
    global offset
    vs = []
    for i in range(count):
      v = struct.unpack_from("<L", data, offset)
      vs += ["%08X" % v]  
      offset += 4
    print(";".join(vs))  

while offset < 3688:
  def read_chunk_a():
    global offset
    read_l(64//4)
  print(offset)
  read_chunk_a()

while offset < 4408:
  def read_chunk_b():
    global offset
    read_l(48//4)
  print(offset)
  read_chunk_b()

while offset < 15232:
  def read_chunk_c():
    global offset
    read_l(88//4)
  print(offset)
  read_chunk_c()

while offset < 39400:
  def read_chunk_c():
    global offset
    read_l(152//4)
  print(offset)
  read_chunk_c()

while offset < 48304:
  def read_chunk_c():
    global offset
    read_l(56//4)
  print(offset)
  read_chunk_c()

while offset < 60400:
  def read_chunk_c():
    global offset
    read_l(64//4)
  print(offset)
  read_chunk_c()


while offset < 6040000:
  def read_chunk_c():
    global offset
    read_l(64//4)
  print(offset, "XXX")
  read_chunk_c()




if False:
  offset = 0
  while offset < len(data):
    vf = struct.unpack_from("<f", data, offset)
    print(offset, vf)
    offset += 4
