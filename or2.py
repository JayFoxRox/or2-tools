#!/usr/bin/env python

from outrun2.gz_extract import *
from outrun2.xpr_extract import *
from outrun2.coli_extract import *
from outrun2.cs___smt_extract import *
from outrun2.obj___smt_extract import *
from outrun2.sin_extract import *
from outrun2.oso_extract import *
from outrun2.scn_env_fog_extract import *
from outrun2.scn_env_sun_extract import *
from outrun2.bin_extract import *

try:
  import bpy
  is_blender = True
except:
  is_blender = False

import io
import os

GAME_OR2 = 1
GAME_OR2006 = 2
game = None

if __name__ == "__main__":

  if not is_blender:
    argi = 1
  else:
    for argi, arg in enumerate(sys.argv):
      if arg == "--":
        break
    argi += 1
  print(argi)
  args = sys.argv[argi:]

  print(args)

  for path in args:

    

    f = open(path, 'rb')

    filename = os.path.basename(f.name)

    print(f.name)

    if filename[-3:].upper() == ".GZ":
      game = GAME_OR2 # OutRun 2
      gz_data = gz_extract(f)
      gz_f = io.BytesIO(gz_data)
    elif filename[-3:].upper() == ".SZ":
      game = GAME_OR2006 # OutRun 2006
      gz_data = gz_extract(f)
      gz_f = io.BytesIO(gz_data)
    else:
      assert(False)
    gz_f.name = f.name

    if True:
      gz_f.seek(0)
      xpr_extract(gz_f)

    if filename[0:5].upper() == "COLI_":
      if game == GAME_OR2006:
        #FIXME: Assert that the length is as expected
        gz_f.seek(0)
        print(struct.unpack("<L", gz_f.read(4))[0])
        gz_f.seek(4)
      else:
        gz_f.seek(0)
      coli_extract(gz_f)

    if filename[0:4].upper() == "OSO_":
      gz_f.seek(0)
      if filename.upper() in ["OSO_DYN_BK_1A_BIN.GZ", "OSO_DYN_CS_3B_BIN.GZ"]:
        # These seem to be very different; bug? unused files?
        print("Skipping OSO for %s" % filename)
      else:
        oso_extract(gz_f)

    if filename[0:12].upper() == "SCN_ENV_FOG_":
      if game == GAME_OR2006:
        #FIXME: Assert that the length is as expected
        gz_f.seek(0)
        print(struct.unpack("<L", gz_f.read(4))[0])
        gz_f.seek(4)
      else:
        gz_f.seek(0)
      scn_env_fog_extract(gz_f)

    if filename[0:12].upper() == "SCN_ENV_SUN_":
      if game == GAME_OR2006:
        #FIXME: Assert that the length is as expected
        gz_f.seek(0)
        print(struct.unpack("<L", gz_f.read(4))[0])
        gz_f.seek(4)
      else:
        gz_f.seek(0)
      scn_env_sun_extract(gz_f)

    if filename[0:3].upper() == "CS_":

      if filename[-7:].upper() == "_SMT.GZ":
        gz_f.seek(0)
        cs___smt_extract(gz_f)

      if filename[-7:].upper() == "_PMT.SZ":
        gz_f.seek(0)
        cs___smt_extract(gz_f)

      if filename[-7:].upper() == "_SIN.GZ":
        gz_f.seek(0)
        sin_extract(gz_f)

      if filename[-7:].upper() == "_BIN.GZ":
        gz_f.seek(0)
        bin_extract(gz_f)

    if filename[0:4].upper() == "OBJ_":

      if filename[-7:].upper() == "_SMT.GZ":
        gz_f.seek(0)
        obj___smt_extract(gz_f) #FIXME: Use obj__smt instead?

        #FIXME: Remove once common parts have been factored out
        gz_f.seek(0)
        cs___smt_extract(gz_f)



