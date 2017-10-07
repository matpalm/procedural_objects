# Run from in blender; 2.76b

import bmesh
import bpy
import os
import random

ORIGIN = 0, 0, 0

# some debugging utils for dev in blender console
def _l():
  return bpy.context.scene.objects[0]
def _m():
  bpy.ops.mesh.primitive_cube_add(location=ORIGIN, radius=1.1)
  marker = bpy.context.scene.objects[0]
  marker.name = 'marker'
  return marker


def recalc_com(obj):
  # recalculate center of mass; required whenever mesh changes
  # black magic from forums, required any time mesh data changed...
  bpy.ops.object.select_all(action='DESELECT')
  obj.select = True
  bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')


def smooth(obj):
  obj.modifiers.new(type='SUBSURF', name='smooth')
  obj.modifiers['smooth'].levels = 1


def union(o1, o2):
  # create boolean modifier against o1 that unions o2
  bool_modifier = o1.modifiers.new(type='BOOLEAN', name='o2_union')
  bool_modifier.object = o2
  bool_modifier.operation = 'UNION'
  # create mesh from o1 + modifier  
  mesh = o1.to_mesh(bpy.context.scene, True, 'PREVIEW')
  # replace o1 mesh with this explicit flattened mesh
  bm = bmesh.new()
  bm.from_mesh(mesh)
  bm.to_mesh(o1.data)
  bm.free()
  # drop modifier
  o1.modifiers.remove(bool_modifier)
  # update center of mass
  recalc_com(o1)
  # remove o2
  bpy.context.scene.objects.unlink(o2)  


def rnd(magnitude):
  return (random.random() * 2 - 1) * magnitude


def perturb_vertices(obj):
  mag = 0.01
  for vertex in obj.data.vertices:
    vertex.co += Vector((rnd(mag), rnd(mag), rnd(mag)))


def create_prism(name, radius=1):
  # create (6, 2r, 2r) rectangular prism
  bpy.ops.mesh.primitive_cube_add(location=ORIGIN, radius=radius)
  prism = bpy.context.scene.objects[0]
  for i in range(4):
    # x values range from -r to r so shift -r values (first 4 vertices)
    # to -6-r to make total length 6
    prism.data.vertices[i].co.x = -6 + radius

  # since coplanar surfaces gives grief to later unioning do
  # a small perturbation of vertices
  perturb_vertices(prism)
  
  recalc_com(prism)
  prism.name = name
  prism.location = ORIGIN  
  return prism


def create_object(name, parts=5):
  assert parts >= 2
  
  # create base object
  o1 = create_prism(name, radius=1.0)
  add_pts = set([(-2, 0, 0), (0, 0, 0), (2, 0, 0)])
  
  # add N-1 new objects
  for _ in range(parts-1):
    # create a new object
    o2 = create_prism('o2',
                      radius=random.choice([0.25, 0.5, 1.0]))

    # decide where to add it  
    add_pt = random.choice(list(add_pts))
    add_pts.remove(add_pt)
    add_pt = Vector(add_pt)
    o2.location = add_pt
  
    # pick axis to align to and depending on this alignment
    # add a new set of add points
    axis = random.choice(['x', 'y', 'z'])
    if axis == 'x':
      # note: object created aligned with x axis
      add_pts.add(tuple(add_pt + Vector((2, 0, 0))))
      add_pts.add(tuple(add_pt + Vector((-2, 0, 0))))
    elif axis == 'y':
      o2.rotation_euler.z = pi/2
      add_pts.add(tuple(add_pt + Vector((0, 2, 0))))
      add_pts.add(tuple(add_pt + Vector((0, -2, 0))))
    else:  # z
      o2.rotation_euler.y = pi/2
      add_pts.add(tuple(add_pt + Vector((0, 0, 2))))
      add_pts.add(tuple(add_pt + Vector((0, 0, -2))))
      
    # trigger redraw. TODO: why?!?
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    # add o2 to o1 and reset to origin
    union(o1, o2)
    o1.location = ORIGIN

  # smooth sometimes
  if random.random() < 0.5:
    smooth(o1)

  return o1


def generate_n_objects(n, output_dir):
  for i in range(n):
    # create object
    obj_id = "%04d" % i
    obj = create_object(name=obj_id,
                        parts=random.choice([4,5]))
    # export .obj to disk
    obj_dir = "%s/%s" % (output_dir, obj_id)
    os.makedirs(obj_dir)
    filepath = "%s/%s.obj" % (obj_dir, obj.name)
    bpy.ops.export_scene.obj(filepath=filepath,
                             global_scale=0.015)
    # delete from scene
    bpy.context.scene.objects.unlink(obj)
