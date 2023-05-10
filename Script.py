import pymeshlab

# the point cloud down sampling rate
PERCENTAGE = 0.05
# width and height of the texture PNG
DIM = 4096

print("load point cloud and down sampling")
ms = pymeshlab.MeshSet()
ms.load_new_mesh("point_cloud.ply")
samplenum = int(ms.current_mesh().vertex_number() * PERCENTAGE)
ms.generate_simplified_point_cloud(
    samplenum=samplenum
)

print("reconstruct mesh from point cloud")
# emperically, the `smoothiter` can be set to 8
ms.compute_normal_for_point_clouds(k=10, smoothiter=0)
# using Open3D's reconstruction params
ms.generate_surface_reconstruction_screened_poisson(depth=13, scale=1.1)

print("remove redundant faces")
ms.meshing_remove_connected_component_by_face_number()
ms.compute_selection_by_non_manifold_per_vertex()
ms.meshing_remove_selected_vertices_and_faces()

print("generate OBJ file and PNG texture")
ms.compute_texcoord_by_function_per_vertex()
ms.compute_texcoord_transfer_vertex_to_wedge()
# the following line might raise a runtime error with "Inter-Triangle border is too much", 
# which can solved by setting a larger `DIM`
ms.compute_texcoord_parametrization_triangle_trivial_per_wedge(textdim=DIM)
ms.compute_texmap_from_color(textname="mesh.png", textw=DIM, texth=DIM)
ms.save_current_mesh("mesh.obj")
