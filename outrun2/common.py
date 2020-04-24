import struct
import sys
import traceback
import os

regions = []
offset = 0
data = None
base = 0

disable_tags = False

def log_region(start, size, typename, comment=None):
  global regions
  if not disable_tags:
    if comment == None:
      comment = "unknown:%s" % typename
      trace = traceback.extract_stack(limit=None)
      for t in trace[-3:-2]:
        comment += " [%s:%d]" % (os.path.basename(t[0]), t[1])
    regions += [(start, start + size, comment)]
  return

def read_t(count, ty, fmt, comment=None, silent=False):
  global offset

  if count == 0:
    return ()
    
  tys = "<%d%c" % (count, ty)

  size = struct.calcsize(tys)
  if size == 0:
    return ()

  log_region(offset, size, tys, comment)

  vs = struct.unpack_from(tys, data, offset)
  offset += size

  if not silent:
    print(";".join([fmt % v for v in vs]))

  return vs

def read_b(count, comment=None, silent=False):
  global offset
  return read_t(count, "B", "%02X", comment, silent) 

def read_h(count, comment=None, silent=False):
  global offset
  return read_t(count, "H", "%04X", comment, silent) 

def read_l(count, comment=None, silent=False):
  global offset
  return read_t(count, "L", "%08X", comment, silent) 

def read_f(count, comment=None, silent=False):
  global offset
  return read_t(count, "f", "%+.5f", comment, silent) 

def read_s(count=0, comment=None, silent=False):
  global offset

  if count == 0:
    size = 0
    while data[offset+size] != 0x00:
      size += 1
    size += 1
  else:
    size = count

  log_region(offset, size, "s%d" % count, comment)

  if count == 0:
    size -= 1

  s = data[offset:offset+size]
  s = s.decode('ascii')

  if not silent:
    print(s)

  return s

def export_tags(path):
  if disable_tags:
    print("Warning: Tags disabled!")
    return
  fo=open(path, "wb")
  fo.write(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
  fo.write(b"<wxHexEditor_XML_TAG>\n")
  fo.write(b"\t<filename path=\"%s\">\n" % b"/tmp/or2/weird.bin")
  for i, region in enumerate(regions):
    fo.write(b"\t\t<TAG id=\"%d\">\n" % i)
    fo.write(b"\t\t\t<start_offset>%d</start_offset>\n" % region[0])
    fo.write(b"\t\t\t<end_offset>%d</end_offset>\n" % (region[1]-1))
    fo.write(b"\t\t\t<tag_text>%d: 0x%X/%d: %s</tag_text>\n" % (i, region[0], region[0], region[2].encode("utf-8")))
    fo.write(b"\t\t\t<font_colour>#000000</font_colour>\n")
    if i % 2:
      fo.write(b"\t\t\t<note_colour>#CB026F</note_colour>\n")
    else:
      fo.write(b"\t\t\t<note_colour>#6F02CB</note_colour>\n")
    fo.write(b"\t\t</TAG>\n")
  fo.write(b"\t</filename>\n")
  fo.write(b"</wxHexEditor_XML_TAG>\n")

stack = []

def push():
  global stack
  global offset
  stack.append(offset)

def pop():
  global stack
  global offset
  offset = stack.pop()
