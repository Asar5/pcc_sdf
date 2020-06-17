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

save_vox_normals = 'vox_normals'

def save_mesh(fname_mesh, fname_save):
	mesh = trimesh.load(fname_mesh) 
	voxels = mesh_to_voxels(mesh, 64, pad=True)
	np.save(fname_save, voxels)
	return voxels #print (voxels)

def load_voxel(fname):
	voxels = np.load(fname)
	return voxels

def recontruct_mesh(voxels):
	vertices, faces, normals, _ = skimage.measure.marching_cubes(voxels, level=0)#_lewiner
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
	points = [[100,10,135],[150,75,120],[50,150,150],[0,0,0]]
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

def calc_gradients(voxels):
	vox_normals = []
	n = len(voxels)
	for i in range(0, len(voxels)):
		for j in range(0, len(voxels[i])):
			for k in range(0, len(voxels[i][j])):
				try:
					grad_x = voxels[i - 1][j][k] - voxels[i + 1][j][k]
				except:
					grad_x = 0

				try:
					grad_y = voxels[i][j - 1][k] - voxels[i][j + 1][k]
				except:
					grad_y = 0

				try:
					grad_z = voxels[i][j][k - 1] - voxels[i][j][k + 1]
				except:
					grad_z = 0

				vox_normals.append((grad_x, grad_y, grad_z))

	np.save(save_vox_normals, vox_normals)

	return vox_normals



#voxels = save_mesh(fname_mesh, fname_save)
#vox_normals = calc_gradients(voxels)
voxels = load_voxel(fname_save+'.npy')
print("Loaded voxel")
print ("Voxel 000", voxels[0][0][0])
print ("Voxel 001", voxels[0][0][1])
print ("Voxel 002", voxels[0][0][2])#[30][30][2])
vox_normals = np.load(save_vox_normals+'.npy')
print (len(vox_normals))
print (vox_normals[111130], vox_normals[21051], vox_normals[212])









#points = [[100,10,135],[150,75,120],[50,150,150],[0,0,0]]
'''mesh = recontruct_mesh(voxels)
print ("Reconstructed voxelised mesh")
print (mesh.vertices.shape)#[0][0])
print(mesh.faces.shape)#[0][0])
print("Normal 1", mesh.vertex_normals[31])#[0][0])
print(mesh.vertex_normals.shape)
find_sdf(mesh)
print ("found sdf for a few points and visualised")'''

