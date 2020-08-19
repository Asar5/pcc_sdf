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

fname_mesh = 'sprayer.STL' #trimesh.primitives.Sphere() '../trimesh/models/Alan_4.stl'
fname_save = 'voxel_sprayer' #'voxel_mold'

save_vox_normals = 'vox_normals_new'

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


########### '-'ve distance if inside the mesh, 
###########'0' on the boundary, 
###########'+'ve distance outside the mesh
@dispatch(trimesh.base.Trimesh)
def find_sdf(mesh):
	points = [[0,0,32]]#[[32,0,32], [32,4,32], [32,8,32], [32,12,32], [32,16,32], [32,20,32], [32,24,32], [32,28,32], [32,32,32], [32,36,32], [32,40,32], [32,44,32], [32,48,32], [32,52,32], [32,56,32], [32,60,32], [32,64,32]]#,[150,75,120],[50,150,150],[0,0,0]]
	points_visual = trimesh.points.PointCloud(points)
	scene = trimesh.Scene([points_visual, mesh])
	(scene).show(smooth=False)

	#points, sdf = sample_sdf_near_surface(mesh, number_of_points=250000)
	#colors = np.zeros(points.shape)
	#colors[:][:] = 1
	#colors[sdf > 0, 0] = 1
	#cloud = pyrender.Mesh.from_points(points)
	#scene.add(cloud)
	#viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

@dispatch(np.ndarray)
def find_sdf(voxels):
	mesh = recontruct_mesh(voxels)
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

#Digital Difference Analyser method
def scan_convert(start_pos, angle, length):
	start_pos[0] = int(start_pos[0])
	start_pos[1] = int(start_pos[1])
	x_new = start_pos[0]
	y_new = start_pos[1]
	new_coords_list = []
	end_pos = [0,0]


	try:
		slope = np.tan(angle)
	except:
		slope = np.inf
	a = length*np.cos(angle)
	end_pos[0] = int(start_pos[0] + a) 
	b = length*np.sin(angle)
	end_pos[1] = int(start_pos[1] + b)

	dx = end_pos[0] - start_pos[0]
	dy = end_pos[1] - start_pos[1]

	steps = 0
	if (abs(dx) > abs(dy)):
		steps = abs(dx)
	else:
		steps = abs(dy)

	Xinc = float(dx)/float(steps)
	Yinc = float(dy)/float(steps)

	for i in range(0, steps):
		x_new = x_new + Xinc
		y_new = y_new + Yinc 
		new_coords_list.append([x_new, y_new])

	return new_coords_list

#def angle_coverage():



def check_for_collision(voxels, new_coords_list):
	z = 32
	#TODO:convert from dist btw stl origin to dist btw sprayer and point
	threshold_min = 0.0 
	threshold_max = 0.2
	distance_coverage = 0.0
	for length in range(len(new_coords_list)):
		x = int(new_coords_list[length][0])
		y = int(new_coords_list[length][1])
		#z = new_coords_list[length][2]
		if (voxels[x][y][z]<threshold_min):
			print ("COLLISION AT", x, y, z, voxels[x][y][z])
			dist_coverage = 0.0

		elif (voxels[x][y][z] > threshold_min and voxels[x][y][z] < threshold_max):
			dist_coverage = -5 * voxels[x][y][z] + 1 #straight line eq (change this maybe?)
		else:
			dist_coverage = 1.0

	return dist_coverage

voxels = save_mesh(fname_mesh, fname_save)
#vox_normals = load_voxel('vox_normals.npy')
voxels = load_voxel(fname_save+'.npy')
####YES OR NO??
##vox_normals = np.reshape(vox_normals, (66,66,66,3))
#print ("vox", voxels.shape, "normal", vox_normals.shape)
start_pos = [32,0]
angle = np.pi/2
length = 5
new_coords = scan_convert(start_pos, angle, length)
print (len(new_coords))
collisions = check_for_collision(voxels, new_coords)
print (collisions)

print ("VOXEL VALUE:", voxels[32][2][32])
mesh = recontruct_mesh(voxels)
print ("Reconstructed voxelised mesh")
find_sdf(mesh)
print ("found sdf for a few points and visualised")



'''print("Loaded voxel")
print ("Voxel 000", voxels[0][0][0])
print ("Voxel 001", voxels[0][0][1])
print ("Voxel 002", voxels[0][0][2])#[30][30][2])'''
#vox_normals = np.load(save_vox_normals+'.npy')
#print (len(vox_normals))
#print (vox_normals[111130], vox_normals[21051], vox_normals[212])