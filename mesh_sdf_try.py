from mesh_to_sdf import mesh_to_voxels
import trimesh
import skimage.measure
import numpy as np 

mesh = trimesh.load('../trimesh/models/Alan_4.stl') #trimesh.primitives.Sphere() '../trimesh/models/Alan_4.stl'
voxels = mesh_to_voxels(mesh, 64, pad=True)
np.save('voxel_grid', voxels_mold)
print (voxels)

#vertices, faces, normals, _ = skimage.measure.marching_cubes_lewiner(voxels, level=0)
#mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
#mesh.show()
#scene = trimesh.Scene([mesh1, mesh])
#(scene).show(smooth=False)