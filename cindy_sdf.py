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

fname_mesh = '../trimesh/models/Alan_4.stl' #trimesh.primitives.Sphere() '../trimesh/models/Alan_4.stl'
fname_save = 'voxel_mold'

def save_mesh(fname_mesh, fname_save):
	mesh = trimesh.load(fname_mesh) 
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
	'''start = [[0,0,0]]
	mesh.visual.face_colors = [100, 100, 100, 100]
	# visualizable two points
	points_visual = trimesh.points.PointCloud(start)
	# create a scene with the mesh, path, and points
	scene = trimesh.Scene([points_visual, mesh])
	(scene).show(smooth=False)'''
	return mesh

@dispatch(trimesh.base.Trimesh)
def find_sdf(mesh):
	points = [[30,30,2],[0,0,1],[0,0,2],[0,0,0]]
	points_visual = trimesh.points.PointCloud(points)
	#points, sdf = sample_sdf_near_surface(mesh, number_of_points=250000)
	#colors = np.zeros(points.shape)
	#colors[:][:] = 1
	#colors[sdf > 0, 0] = 1

	#cloud = pyrender.Mesh.from_points(points)
	scene = trimesh.Scene([points_visual, mesh])
	(scene).show(smooth=False)
	#scene.add(cloud)
	#viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

@dispatch(np.ndarray)
def find_sdf(voxels):
	mesh = recontruct_mesh(voxels)
	#points, sdf = sample_sdf_near_surface(mesh, number_of_points=250000)
	#colors = np.zeros(points.shape)
	#colors[sdf < 0, 2] = 1
	#colors[sdf > 0, 0] = 1
	cloud = pyrender.Mesh.from_points([0,0,0])
	scene = pyrender.Scene()
	scene.add(cloud)
	viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

voxels = save_mesh(fname_mesh, fname_save)
voxels = load_voxel(fname_save+'.npy')

print (voxels[30][30][2])
mesh = recontruct_mesh(voxels)
print (mesh.vertices[0][0])
print(mesh.faces[0][0])
print(mesh.vertex_normals[0][0])
find_sdf(mesh)