'''
######
load mesh
voxelise mesh to get occupency of each cell
Take points from sprayer class
check for intersection between these points and voxelised mesh


Possible issues:
Points should be wrt same origin (sprayer and mesh)

######
'''

from mesh_to_sdf import *
import trimesh
import skimage.measure
import numpy as np 
import pyrender
from multipledispatch import dispatch

fname_mesh = '../trimesh/models/Alan_4.stl'
fname_save = 'voxel_mold'

def save_mesh(fname_mesh, fname_save):
	mesh = trimesh.load('../trimesh/models/Alan_4.stl') #trimesh.primitives.Sphere() '../trimesh/models/Alan_4.stl'
	voxels = mesh_to_voxels(mesh, 200, pad=True)
	np.save(fname_save, voxels)
	return voxels #print (voxels)

def load_voxel(fname):
	voxels = np.load(fname)
	return voxels

def recontruct_mesh(voxels):
	vertices, faces, normals, _ = skimage.measure.marching_cubes_lewiner(voxels, level=0)
	mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
	#mesh.show()
	return mesh

@dispatch(trimesh.base.Trimesh)
def find_sdf(mesh):
	points, sdf = sample_sdf_near_surface(mesh, number_of_points=250000)
	colors = np.zeros(points.shape)
	colors[sdf < 0, 2] = 1
	colors[sdf > 0, 0] = 1
	cloud = pyrender.Mesh.from_points(points, colors=colors)
	scene = pyrender.Scene()
	scene.add(cloud)
	viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

@dispatch(np.ndarray)
def find_sdf(voxels):
	mesh = recontruct_mesh(voxels)
	points, sdf = sample_sdf_near_surface(mesh, number_of_points=250000)
	colors = np.zeros(points.shape)
	colors[sdf < 0, 2] = 1
	colors[sdf > 0, 0] = 1
	cloud = pyrender.Mesh.from_points(points, colors=colors)
	scene = pyrender.Scene()
	scene.add(cloud)
	viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

#voxels = save_mesh(fname_mesh, fname_save)
voxels = load_voxel(fname_save+'.npy')
print (type(voxels))
mesh = recontruct_mesh(voxels)
find_sdf(mesh)