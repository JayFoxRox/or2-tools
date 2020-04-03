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

if __name__ == "__main__":
  for path in sys.argv[1:]:

    f = open(path, 'rb')

    filename = os.path.basename(f.name)

    print(f.name)

    if filename[-3:] == ".GZ":
      gz_data = gz_extract(f)
      gz_f = io.BytesIO(gz_data)
    else:
      assert(False)
    gz_f.name = f.name

    if False:
      gz_f.seek(0)
      xpr_extract(gz_f)

    if filename[0:5] == "COLI_":
      gz_f.seek(0)
      coli_extract(gz_f)

    if filename[0:3] == "CS_":

      if filename[-7:] == "_SMT.GZ":
        gz_f.seek(0)
        cs___smt_extract(gz_f)

      if filename[-7:] == "_SIN.GZ":
        gz_f.seek(0)
        sin_extract(gz_f)

      if filename[-7:] == "_BIN.GZ":
        gz_f.seek(0)
        bin_extract(gz_f)

    if filename[0:4] == "OBJ_":

      if filename[-7:] == "_SMT.GZ":
        gz_f.seek(0)
        obj___smt_extract(gz_f) #FIXME: Use obj__smt instead?

        #FIXME: Remove once common parts have been factored out
        gz_f.seek(0)
        cs___smt_extract(gz_f)



