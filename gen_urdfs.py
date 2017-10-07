#!/usr/bin/env python3
import os
from random import random
import sys
assert sys.argv[1], "usage: ./gen_urdfs.py <directory>"
template = open("template.urdf").read()
obj_dir = sys.argv[1]
for obj_id in os.listdir(obj_dir):
  random_rgb = "%.3f %.3f %.3f" % (random(), random(), random())
  urdf = template.replace("%%ID%%", obj_id).replace("%%RGB%%", random_rgb)
  with open("%s/%s/%s.urdf" % (obj_dir, obj_id, obj_id), "w") as f:
    f.write(urdf)
