"""
sdf_try.py
----------------

Given a mesh and a point, find the  signed distance function.
OUTSIDE --> NEGETIVE
INSIDE + WITHIN TOLERANCE --> POSITIVE
"""

import trimesh

if __name__ == '__main__':

    mesh = trimesh.load(trimesh.primitives.Sphere())#../trimesh/models/Alan_4.stl')#trimesh.primitives.Sphere()

    # arbitrary indices to test with
    start = [[0,0,0]]#, [0,1,1], [1,1,1]]

    distance = trimesh.proximity.signed_distance(mesh, start)
    print (distance)

    # VISUALIZE RESULT
    # make the sphere transparent-ish
    mesh.visual.face_colors = [100, 100, 100, 100]
    # visualizable two points
    points_visual = trimesh.points.PointCloud(start)
    # create a scene with the mesh, path, and points
    scene = trimesh.Scene([points_visual, mesh])
    (scene).show(smooth=False)
