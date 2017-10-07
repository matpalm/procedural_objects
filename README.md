# procedural generation of objects for bullet grasping

![objects](objects.png)

## generate .obj files

we generate and export `.obj` files within blender

start `blender` under this directory

open blender console (ctrl-alt-w, shift-f4) and run generation script

```
f = "gen_objs.py"
exec(compile(open(f).read(),f,'exec'))
generate_n_objects(n=10, output_dir="objs")
```

##  run convex decomposition

exported `.objs` are concave only so need to run a convex decomposition on
meshes. bullet includes `vhacd` so use that, though this might be possible
to do directly from blender as part of the `obj` export?

```
# make vhacd tool under bullet
mkdir ~/dev; cd ~/dev
git clone git@github.com:bulletphysics/bullet3.git
cd bullet3
./build_cmake_pybullet_double.sh
```

run vhacd on all exported `.obj` files to make a corresponding `.vhacd.obj` file.

`.obj` are used for visual mesh, `.vhacd.obj` are used for collision.

```
./run_vhacd.sh objs
```

## create urdfs

to load objects into bullet we need to generate `.urdf` files.
use the bullet example `data/cube.udf` as a template

```
./gen_urdfs.py objs
```

