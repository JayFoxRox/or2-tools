#!/usr/bin/env python

import sys
import struct

path = sys.argv[1]

# AS_END_F50_BIN.GZ after decompression
print("Opening '%s'" % path)

f = open(path, 'rb')
data = f.read()



offset = 0x0

def read_t(count, ty, fmt):
  global offset
  vs = []
  for i in range(count):
    v = struct.unpack_from(ty, data, offset)[0]
    vs += [v]
    offset += struct.calcsize(ty)
  print(";".join([ fmt % v for v in vs]))  
  return tuple(vs)

def read_b(count):
  global offset
  return read_t(count, "<B", "%02X")

def read_h(count):
  global offset
  return read_t(count, "<H", "%04X")

def read_l(count):
  global offset
  return read_t(count, "<L", "%08X")

def read_f(count):
  global offset
  return read_t(count, "<f", "%+.5f") 


offset = 0x2720
for i in range(100):
  read_f(3)

