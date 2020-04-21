#!/usr/bin/env python




import sys
import zlib
import struct
import PIL
import PIL.Image
import os
import io
import gzip

os.environ["XBOX_IF"] = "none"

from xboxpy import nv2a

def gz_extract(f):

  filename = os.path.basename(f.name)

  os.makedirs("/tmp/or2/%s/" % (filename), exist_ok=True)

  data = f.read()

  try:

    # Deflate
    data = zlib.decompress(data)

    # Length?   ?           ?         ?
    # 542D0000 00000000 00000000 0C000000
    a,b,c,d = struct.unpack_from("<LLLL", data, 0)

    open("/tmp/or2/%s/raw.bin" % (filename), 'wb').write(data)

    if False:
      data = data[0x4:] # Trim a
      print(a, len(data))
      assert(a == len(data))
      data = data[0xC:] # Trim b,c,d
    else:
      b = 0
      c = 0
      d = 0xC

    open("/tmp/or2/%s/decompressed.bin" % (filename), 'wb').write(data)
    print("Decompressed 0x%X" % d)

    assert(b == 0)
    assert(c == 0)
    assert(d in [0xC, 0x28])

  except:
    try:

      def read_part(data):
        res = b''

        while bytes([data[0]]) != b' ':
          res += bytes([data[0]])
          data = data[1:]
        return data[1:], res

      data, a = read_part(data)
      data, b = read_part(data)
      assert(a == b"or2")

      print("Compressed gzip '%s' '%s'" % (a, b))


      f = io.BytesIO(data)
      fg = gzip.open(f, mode='rb')

      #FIXME: This does not work. How the fuck to do this?
      print("file info: '%s', %s" % (fg.name, fg.mtime))

      data = fg.read()

      open("/tmp/or2/%s/decompressed.bin" % (filename), 'wb').write(data)

    except:
      print("Not compressed?")
      assert(False)

  return data

if __name__ == "__main__":
  for path in sys.argv[1:]:
    f = open(path, 'rb')
    xpr_extract(f)
