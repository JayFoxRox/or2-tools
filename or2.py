#!/usr/bin/env python

from gz_extract import *
from xpr_extract import *
from coli_extract import *
from cs___smt_extract import *
from obj___smt_extract import *
from sin_extract import *
from bin_extract import *

import io
import os

GAME_OR2 = 1
GAME_OR2006 = 2
game = None

if __name__ == "__main__":
  for path in sys.argv[1:]:

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



