# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.measurements import center_of_mass
import pathlib
import vtk
from vtk.util import numpy_support
import os
import tkinter as tk
from tkinter import filedialog
from skimage import measure
import logging
import sys
import gc
sys.path.append('D:/myscripts/bcdi/')
import bcdi.graph.graph_utils as gu
import bcdi.facet_recognition.facet_utils as fu
import bcdi.simulation.simulation_utils as simu
import bcdi.postprocessing.postprocessing_utils as pu

helptext = """
Script for detecting facets on a 3D crytal reconstructed by a phasing algorithm (Bragg CDI) and making some statistics
about strain by facet. The correct threshold for support determination should be given as input,
as well as voxel sizes for a correct calculation of facet angle.

Input: a reconstruction .npz file with fields: 'amp' and 'strain' 
Output: a log file with strain statistics by plane, a VTK file for 3D visualization of detected planes.
"""

scan = 15  # spec scan number
datadir = 'D:/data/P10_isosurface/data/p15_2_{:05d}/pynxraw/'.format(scan)
support_threshold = 0.5  # threshold for support determination
voxel_size = [6, 6, 6]   # tuple of 3 numbers, voxel size of the real-space reconstruction in each dimension
upsampling_factor = 1  # integer, factor for upsampling the reconstruction in order to have a smoother surface
savedir = datadir
reflection = np.array([1, 1, 1])  # measured crystallographic reflection
projection_axis = 1  # the projection will be performed on the equatorial plane perpendicular to that axis (0, 1 or 2)
debug = False  # set to True to see all plots for debugging
smoothing_iterations = 10  # number of iterations in Taubin smoothing, bugs if smoothing_iterations larger than 10
smooth_lamda = 0.33  # lambda parameter in Taubin smoothing
smooth_mu = 0.34  # mu parameter in Taubin smoothing
radius_normals = 0.1  # radius of integration for the calculation of the density of normals
projection_method = 'stereographic'  # 'stereographic' or 'equirectangular'
peak_min_distance = 25  # pixel separation between peaks in corner_peaks()
max_distance_plane = 0.75  # in pixels, maximum allowed distance to the facet plane of a voxel
top_part = False  # if True, will also update logfiles with a support cropped at z_cutoff (remove bottom part)
z_cutoff = 75  # in pixels. If top_pat=True, will set all support pixels below this value to 0
edges_coord = 370  # coordination threshold for isolating edges, 350 seems to work reasonably well
corners_coord = 280  # coordination threshold for isolating corners, 260 seems to work reasonably well
#########################################################
# parameters only used in the stereographic projection #
#########################################################
threshold_south = -250  # background threshold in the stereographic projection from South of the density of normals
threshold_north = -250  # background threshold in the stereographic projection from North of the density of normals
max_angle = 95  # maximum angle in degree of the stereographic projection (should be larger than 90)
stereo_scale = 'linear'  # 'linear' or 'log', scale of the colorbar in the stereographic plot
#########################################################
# parameters only used in the equirectangular projection #
#########################################################
bw_method = 0.03  # bandwidth in the gaussian kernel density estimation
kde_threshold = -0.2  # threshold for defining the background in the density estimation of normals
###############################################################################################
# define crystallographic planes of interest for the stereographic projection (cubic lattice) #
###############################################################################################
planes_south = dict()  # create dictionnary for the projection from the South pole, the reference is +reflection
# planes_south['0 2 0'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([0, 2, 0]))
planes_south['1 1 1'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([1, 1, 1]))
planes_south['1 0 0'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([1, 0, 0]))
planes_south['1 1 0'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([1, 1, 0]))
planes_south['-1 1 0'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([-1, 1, 0]))
planes_south['1 -1 1'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([1, -1, 1]))
planes_south['-1 -1 1'] = simu.angle_vectors(ref_vector=reflection, test_vector=np.array([-1, -1, 1]))

planes_north = dict()  # create dictionnary for the projection from the North pole, the reference is -reflection
# planes_south['0 -2 0'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([0, -2, 0]))
planes_north['-1 -1 -1'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([-1, -1, -1]))
planes_north['-1 0 0'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([-1, 0, 0]))
planes_north['-1 -1 0'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([-1, -1, 0]))
planes_north['-1 1 0'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([-1, 1, 0]))
planes_north['-1 -1 1'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([-1, -1, 1]))
planes_north['-1 1 1'] = simu.angle_vectors(ref_vector=-reflection, test_vector=np.array([-1, 1, 1]))
##########################
# end of user parameters #
##########################

###########################################################
# create directory and initialize error logger #
###########################################################
pathlib.Path(savedir).mkdir(parents=True, exist_ok=True)
logger = logging.getLogger()

###################
# define colormap #
###################
colormap = gu.Colormap()
my_cmap = colormap.cmap

#############
# load data #
#############
plt.ion()
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir=datadir, filetypes=[("NPZ", "*.npz")])
npzfile = np.load(file_path)
amp = npzfile['amp']
amp = amp / amp.max()
nz, ny, nx = amp.shape
print("Initial data size: (", nz, ',', ny, ',', nx, ')')
strain = npzfile['strain']

#################
# upsample data #
#################
if upsampling_factor > 1:
    amp, _ = fu.upsample(array=amp, upsampling_factor=upsampling_factor, voxelsizes=voxel_size,
                         title='modulus', debugging=debug)
    strain, voxel_size = fu.upsample(array=strain, upsampling_factor=upsampling_factor, voxelsizes=voxel_size,
                                     title='strain', debugging=debug)
    nz, ny, nx = amp.shape
    print("Upsampled data size: (", nz, ',', ny, ',', nx, ')')
    print("New voxel sizes: ", voxel_size)

#####################################################################
# Use marching cubes to obtain the surface mesh of these ellipsoids #
#####################################################################
vertices_old, faces, _, _ = measure.marching_cubes_lewiner(amp, level=support_threshold, allow_degenerate=False,
                                                           step_size=1)
# vertices_old is a list of 3d coordinates of all vertices points
# faces is a list of facets defined by the indices of 3 vertices_old

# from scipy.io import savemat
# savemat('//win.desy.de/home/carnisj/My Documents/MATLAB/TAUBIN/vertices.mat', {'V': vertices_old})
# savemat('//win.desy.de/home/carnisj/My Documents/MATLAB/TAUBIN/faces.mat', {'F': faces})

# Display mesh before smoothing
if debug:
    gu.plot_3dmesh(vertices_old, faces, (nz, ny, nx), title='Mesh after marching cubes')
    plt.ion()

#######################################
# smooth the mesh using taubin_smooth #
#######################################
vertices_new, normals, _, intensity, faces, _ = \
    fu.taubin_smooth(faces, vertices_old, iterations=smoothing_iterations, lamda=smooth_lamda, mu=smooth_mu,
                     radius=radius_normals, debugging=debug)
del vertices_old
gc.collect()

nb_vertices = vertices_new.shape[0]

# Display smoothed triangular mesh
if debug:
    gu.plot_3dmesh(vertices_new, faces, (nz, ny, nx), title='Mesh after Taubin smoothing')
    plt.ion()

#####################################################################
# 2D projection of normals, peak finding and watershed segmentation #
#####################################################################
nb_normals = normals.shape[0]
if projection_method == 'stereographic':
    labels_top, labels_bottom, stereo_proj, remove_row =\
        fu.stereographic_proj(normals=normals, intensity=intensity, background_south=threshold_south,
                              background_north=threshold_north, min_distance=peak_min_distance, savedir=savedir,
                              save_txt=False, plot_planes=True, planes_south=planes_south, planes_north=planes_north,
                              max_angle=max_angle, voxel_size=voxel_size, projection_axis=projection_axis,
                              scale=stereo_scale, debugging=debug)

    # remove rows containing nan values
    normals = np.delete(normals, remove_row, axis=0)
    faces = np.delete(faces, remove_row, axis=0)

    nb_normals = normals.shape[0]
    numy, numx = labels_top.shape  # identical to labels_bottom.shape
    max_label = max(labels_top.max(), labels_bottom.max())

    if stereo_proj.shape[0] != nb_normals:
        print(projection_method, 'projection output: incompatible number of normals')
        sys.exit()

    # look for potentially duplicated labels (labels crossing the 90 degree circle)
    duplicated_labels = [0]  # do not consider background points when looking for duplicates (label 0 is the background)
    # duplicated_labels stores bottom_labels which are duplicate from top_labels [0 duplicated_labels unique_label ...]
    for label in range(1, labels_top.max()+1, 1):
        label_points = np.argwhere(labels_top == label)
        label_points[:, 0] = (label_points[:, 0] * 2*max_angle / numy) - max_angle  # rescale to [-max_angle max_angle]
        label_points[:, 1] = (label_points[:, 1] * 2*max_angle / numx) - max_angle  # rescale to [-max_angle max_angle]

        label_distances = np.sqrt(label_points[:, 0]**2 + label_points[:, 1]**2)
        if (label_distances <= 90).sum() == label_points.shape[0]:  # all points inside the 90deg border
            continue  # do nothing, the facet is valid
        elif (label_distances > 90).sum() == label_points.shape[0]:  # all points outside the 90deg border
            continue  # do nothing, the facet will be filtered out in next section by distance check
        else:  # some points on the other side of the 90deg border
            print('Label ', str(label), 'is potentially duplicated')
            # look for the corresponding label in the bottom projection
            for idx in range(nb_normals):
                # calculate the corresponding index coordinates
                # by rescaling from [-max_angle max_angle] to [0 numy] or [0 numx]
                u_top = int((stereo_proj[idx, 0] + max_angle) * numx / (2*max_angle))  # u axis horizontal
                v_top = int((stereo_proj[idx, 1] + max_angle) * numy / (2*max_angle))  # v axis vertical
                u_bottom = int((stereo_proj[idx, 2] + max_angle) * numx / (2*max_angle))  # u axis horizontal
                v_bottom = int((stereo_proj[idx, 3] + max_angle) * numy / (2*max_angle))  # v axis vertical

                try:
                    if labels_top[u_top, v_top] == label and \
                            labels_bottom[u_bottom, v_bottom] not in duplicated_labels:
                        # only the first duplicated point will be checked, then the whole bottom_label is changed
                        # to label and there is no need to check anymore
                        duplicated_labels.append(labels_bottom[u_bottom, v_bottom])
                        duplicated_labels.append(label)
                        print('  Corresponding label :', labels_bottom[u_bottom, v_bottom], 'changed to', label)
                        labels_bottom[labels_bottom == labels_bottom[u_bottom, v_bottom]] = label
                except IndexError:
                    # the IndexError exception arises because we are spanning all normals for labels_top, even those
                    # whose stereographic projection is farther than max_angle.
                    continue

        del label_points, label_distances
        gc.collect()

    # reorganize stereo_proj to keep only the projected point which is in the range [-90 90]
    pole_proj = np.zeros((nb_normals, 3), dtype=stereo_proj.dtype)
    # 1st and 2nd columns are coordinates
    # the 3rd column is an indicator for using South or North projected coordinates
    for idx in range(nb_normals):
        if np.sqrt(stereo_proj[idx, 0]**2 + stereo_proj[idx, 1]**2) > 90:
            pole_proj[idx, 0:2] = stereo_proj[idx, 2:]  # use values for the projection from North pole
            pole_proj[idx, 2] = 1  # use values from labels_bottom (projection from North pole)
        else:
            pole_proj[idx, 0:2] = stereo_proj[idx, 0:2]  # use values for the projection from South pole
            pole_proj[idx, 2] = 0  # use values from labels_top (projection from South pole)
    del stereo_proj
    gc.collect()

    # rescale euclidian u axis from [-max_angle max_angle] to [0 numy]
    pole_proj[:, 0] = (pole_proj[:, 0] + max_angle) * numy / (2*max_angle)
    # rescale euclidian v axis from [-max_angle max_angle] to [0 numx]
    pole_proj[:, 1] = (pole_proj[:, 1] + max_angle) * numx / (2*max_angle)
    # change pole_proj to an array of integer indices
    coordinates = pole_proj.astype(int)

    del pole_proj
    gc.collect()

    ##############################################
    # assign back labels to normals and vertices #
    ##############################################
    normals_label = np.zeros(nb_normals, dtype=int)
    vertices_label = np.zeros(nb_vertices, dtype=int)  # the number of vertices is: vertices_new.shape[0]
    for idx in range(nb_normals):
        # check to which label belongs this normal
        if coordinates[idx, 2] == 0:  # use values from labels_top (projection from South pole)
            label_idx = labels_top[coordinates[idx, 0], coordinates[idx, 1]]
        elif coordinates[idx, 2] == 1:  # use values from labels_bottom (projection from North pole)
            label_idx = labels_bottom[coordinates[idx, 0], coordinates[idx, 1]]
        else:
            label_idx = 0  # duplicated facet, set it to the background
        normals_label[idx] = label_idx  # attribute the label to the normal
        vertices_label[faces[idx, :]] = label_idx  # attribute the label to the corresponding vertices

elif projection_method == 'equirectangular':
    labels, longitude_latitude = fu.equirectangular_proj(normals=normals, intensity=intensity, bw_method=bw_method,
                                                         background_threshold=kde_threshold,
                                                         min_distance=peak_min_distance, debugging=debug)
    if longitude_latitude.shape[0] != nb_normals:
        print(projection_method, 'projection output: incompatible number of normals')
        sys.exit()
    numy, numx = labels.shape
    # rescale the horizontal axis from [-pi pi] to [0 numx]
    longitude_latitude[:, 0] = (longitude_latitude[:, 0] + np.pi) * numx / (2 * np.pi)  # longitude
    # rescale the vertical axis from [-pi/2 pi/2] to [0 numy]
    longitude_latitude[:, 1] = (longitude_latitude[:, 1] + np.pi / 2) * numy / np.pi  # latitude
    # change longitude_latitude to an array of integer indices
    coordinates = np.fliplr(longitude_latitude).astype(int)  # put the vertical axis in first position
    duplicated_labels = []
    max_label = labels.max()

    del longitude_latitude
    gc.collect()

    ##############################################
    # assign back labels to normals and vertices #
    ##############################################
    normals_label = np.zeros(nb_normals, dtype=int)
    vertices_label = np.zeros(nb_vertices, dtype=int)  # the number of vertices is: vertices_new.shape[0]
    for idx in range(nb_normals):
        label_idx = labels[coordinates[idx, 0], coordinates[idx, 1]]
        normals_label[idx] = label_idx  # attribute the label to the normal
        vertices_label[faces[idx, :]] = label_idx  # attribute the label to the corresponding vertices

else:
    print('Invalid value for projection_method')
    sys.exit()

unique_labels = [label for label in np.arange(1, max_label+1) if label not in duplicated_labels[1::2]]
print('\nBackground: ', str((normals_label == 0).sum()), 'normals')
for label in unique_labels:
    print("Facet", str(label), ': ', str((normals_label == label).sum()), 'normals detected')
del normals_label, coordinates, faces
gc.collect()

###############################################
# assign back labels to voxels using vertices #
###############################################
all_planes = np.zeros((nz, ny, nx), dtype=int)
planes_counter = np.zeros((nz, ny, nx), dtype=int)  # check if a voxel is used several times
duplicated_counter = 0
for idx in range(nb_vertices):
    temp_indices = np.rint(vertices_new[idx, :]).astype(int)
    planes_counter[temp_indices[0], temp_indices[1], temp_indices[2]] = \
        planes_counter[temp_indices[0], temp_indices[1], temp_indices[2]] + 1
    # check duplicated voxels and discard them if they belong to different planes
    # it happens when some vertices are close and they give the same voxel after rounding their position to integers
    if planes_counter[temp_indices[0], temp_indices[1], temp_indices[2]] > 1:
        if all_planes[temp_indices[0], temp_indices[1], temp_indices[2]] != vertices_label[idx]:
            # belongs to different labels, therefore it is set as background (label 0)
            all_planes[temp_indices[0], temp_indices[1], temp_indices[2]] = 0
            duplicated_counter = duplicated_counter + 1
    else:  # non duplicated pixel
        all_planes[temp_indices[0], temp_indices[1], temp_indices[2]] = \
                vertices_label[idx]
print('\nRounded vertices belonging to multiple labels = ', duplicated_counter)
del planes_counter, vertices_label, vertices_new
gc.collect()

#####################################################
# define surface gradient using a conjugate support #
#####################################################
# this support is 1 outside, 0 inside so that the gradient points towards exterior
support = np.ones((nz, ny, nx))
support[abs(amp) > support_threshold * abs(amp).max()] = 0
zCOM, yCOM, xCOM = center_of_mass(support)
print("COM at (z, y, x): (", str('{:.2f}'.format(zCOM)), ',', str('{:.2f}'.format(yCOM)), ',',
      str('{:.2f}'.format(xCOM)), ')')
gradz, grady, gradx = np.gradient(support, 1)  # support

############################################
# define the support, surface layer & bulk #
############################################
support = np.zeros(amp.shape)
support[abs(amp) > support_threshold * abs(amp).max()] = 1
coordination_matrix = pu.calc_coordination(support, kernel=np.ones((3, 3, 3)), debugging=False)
surface = np.copy(support)
surface[coordination_matrix > 22] = 0  # remove the bulk 22
bulk = support - surface
del coordination_matrix
gc.collect()

########################################################
# define edges using the coordination number of voxels #
########################################################
edges = pu.calc_coordination(support, kernel=np.ones((9, 9, 9)), debugging=False)
edges[support == 0] = 0
if debug:
    gu.multislices_plot(edges, vmin=0, title='Coordination matrix')
edges[edges > edges_coord] = 0  # remove facets and bulk
edges[np.nonzero(edges)] = 1  # edge support
gu.scatter_plot(array=np.asarray(np.nonzero(edges)).T, markersize=2, markercolor='b', labels=('x', 'y', 'z'),
                title='edges')

########################################################
# define corners using the coordination number of voxels #
########################################################
corners = pu.calc_coordination(support, kernel=np.ones((9, 9, 9)), debugging=False)
corners[support == 0] = 0
if debug:
    gu.multislices_plot(corners, vmin=0, title='Coordination matrix')
corners[corners > corners_coord] = 0  # remove edges, facets and bulk
corners[np.nonzero(corners)] = 1  # corner support
gu.scatter_plot(array=np.asarray(np.nonzero(corners)).T, markersize=2, markercolor='b', labels=('x', 'y', 'z'),
                title='corners')

######################################
# Initialize log files and .vti file #
######################################
summary_file = open(os.path.join(savedir, "S" + str(scan) + "_planes.dat"), "w")
summary_file.write('{0: <10}'.format('Plane #') + '\t' + '{0: <10}'.format('angle') + '\t' +
                   '{0: <10}'.format('points #') + '\t' + '{0: <10}'.format('<strain>') + '\t' +
                   '{0: <10}'.format('std dev') + '\t' + '{0: <10}'.format('A (x)') + '\t' +
                   '{0: <10}'.format('B (y)') + '\t' + 'C (Ax+By+C=z)' + '\t' + 'normal X' + '\t' +
                   'normal Y' + '\t' + 'normal Z' + '\n')
allpoints_file = open(os.path.join(savedir, "S" + str(scan) + "_strain.dat"), "w")
allpoints_file.write('{0: <10}'.format('Plane #') + '\t' + '{0: <10}'.format('Z') + '\t' + '{0: <10}'.format('Y') +
                     '\t' + '{0: <10}'.format('X') + '\t' + '{0: <10}'.format('strain')+'\n')

# prepare amp for vti file
amp_array = np.transpose(np.flip(amp, 2)).reshape(amp.size)  # VTK axis 2 is flipped
amp_array = numpy_support.numpy_to_vtk(amp_array)
image_data = vtk.vtkImageData()
image_data.SetOrigin(0, 0, 0)
image_data.SetSpacing(voxel_size[0], voxel_size[1], voxel_size[2])
image_data.SetExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)
pd = image_data.GetPointData()
pd.SetScalars(amp_array)
pd.GetArray(0).SetName("amp")
index_vti = 1

##################################################
# save bulk, edges and corners strain to logfile #
##################################################
fu.update_logfile(support=bulk, strain_array=strain, summary_file=summary_file, allpoints_file=allpoints_file,
                  label='bulk', top_part=top_part, z_cutoff=z_cutoff)

fu.update_logfile(support=surface, strain_array=strain, summary_file=summary_file, allpoints_file=allpoints_file,
                  label='surface', top_part=top_part, z_cutoff=z_cutoff)

fu.update_logfile(support=edges, strain_array=strain, summary_file=summary_file, allpoints_file=allpoints_file,
                  label='edges', top_part=top_part, z_cutoff=z_cutoff)

fu.update_logfile(support=corners, strain_array=strain, summary_file=summary_file, allpoints_file=allpoints_file,
                  label='corners', top_part=top_part, z_cutoff=z_cutoff)

del bulk, corners
gc.collect()

##############################################################################################
# fit points by a plane, exclude points far away, loof for the surface layer, refine the fit #
##############################################################################################
for label in unique_labels:
    print('\nPlane', label)
    # raw fit including all points
    plane = np.copy(all_planes)
    plane[plane != label] = 0
    plane[plane == label] = 1
    if plane[plane == 1].sum() == 0:  # no points on the plane
        print('Raw fit: no points for plane', label)
        continue
    # Why not using direclty the centroid to find plane equation?
    # Because it does not distinguish pixels coming from different but parallel facets
    coeffs,  plane_indices, errors, stop = fu.fit_plane(plane=plane, label=label, debugging=debug)
    if stop == 1:
        print('No points remaining after raw fit for plane', label)
        continue

    # update plane by filtering out pixels too far from the fit plane
    plane, stop = fu.distance_threshold(fit=coeffs, indices=plane_indices, shape=plane.shape,
                                        max_distance=max_distance_plane)
    grown_points = plane[plane == 1].sum().astype(int)
    if stop == 1:  # no points on the plane
        print('Refined fit: no points for plane', label)
        continue
    else:
        print('Plane', label, ', ', str(grown_points), 'points after checking distance to plane')
    plane_indices = np.nonzero(plane == 1)

    if debug:

        gu.scatter_plot(array=np.asarray(plane_indices).T, labels=('x', 'y', 'z'),
                        title='Plane' + str(label) + ' after raw fit')

    ##########################################################################################################
    # Look for the surface: correct for the offset between plane equation and the outer shell of the support #
    # Effect of meshing/smoothing: the meshed support is smaller than the initial support #
    #############################################################################################
    # crop the support to a small ROI included in the plane box
    surf0, surf1, surf2 = fu.surface_indices(surface=surface, plane_indices=plane_indices, margin=3)

    plane_normal = np.array([coeffs[0], coeffs[1], -1])  # normal is [a, b, c] if ax+by+cz+d=0

    dist = np.zeros(len(surf0))
    for point in range(len(surf0)):
        dist[point] = (coeffs[0]*surf0[point] + coeffs[1]*surf1[point] - surf2[point] + coeffs[2]) \
               / np.linalg.norm(plane_normal)
    mean_dist = dist.mean()
    print('Mean distance of plane ', label, ' to outer shell = ' + str('{:.2f}'.format(mean_dist)) + 'pixels')

    dist = np.zeros(len(surf0))
    for point in range(len(surf0)):
        dist[point] = (coeffs[0]*surf0[point] + coeffs[1]*surf1[point] - surf2[point]
                       + (coeffs[2] - mean_dist / 2)) / np.linalg.norm(plane_normal)
    new_dist = dist.mean()
    step_shift = 0.25  # will scan by half pixel through the crystal in order to not miss voxels
    # these directions are for a mesh smaller than the support
    if mean_dist*new_dist < 0:  # crossed the support surface
        step_shift = np.sign(mean_dist) * step_shift
    elif abs(new_dist) - abs(mean_dist) < 0:
        step_shift = np.sign(mean_dist) * step_shift
    else:  # going away from surface, wrong direction
        step_shift = -1 * np.sign(mean_dist) * step_shift

    step_shift = -1*step_shift  # added JCR 24082018 because the direction of normals was flipped

    common_previous = 0
    found_plane = 0
    nbloop = 1
    crossed_surface = 0
    shift_direction = 0
    while found_plane == 0:
        common_points = 0
        # shift indices
        plane_newindices0, plane_newindices1, plane_newindices2 =\
            fu.offset_plane(indices=plane_indices, offset=nbloop*step_shift, plane_normal=plane_normal)

        for point in range(len(plane_newindices0)):
            for point2 in range(len(surf0)):
                if plane_newindices0[point] == surf0[point2] and plane_newindices1[point] == surf1[point2]\
                        and plane_newindices2[point] == surf2[point2]:
                    common_points = common_points + 1

        if debug:
            tempcoeff2 = coeffs[2] - nbloop * step_shift
            dist = np.zeros(len(surf0))
            for point in range(len(surf0)):
                dist[point] = (coeffs[0] * surf0[point] + coeffs[1] * surf1[point] - surf2[point] + tempcoeff2) \
                              / np.linalg.norm(plane_normal)
            temp_mean_dist = dist.mean()
            plane = np.zeros(surface.shape)
            plane[plane_newindices0, plane_newindices1, plane_newindices2] = 1

            # plot plane points overlaid with the support
            gu.scatter_plot_overlaid(arrays=(np.concatenate((plane_newindices0[:, np.newaxis],
                                                             plane_newindices1[:, np.newaxis],
                                                             plane_newindices2[:, np.newaxis]), axis=1),
                                             np.concatenate((surf0[:, np.newaxis],
                                                             surf1[:, np.newaxis],
                                                             surf2[:, np.newaxis]), axis=1)),
                                     markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                     title='Plane' + str(label) + ' after shifting facet - iteration' + str(nbloop))

            print('(while) iteration ', nbloop, '- Mean distance of the plane to outer shell = ' +
                  str('{:.2f}'.format(temp_mean_dist)) + '\n pixels - common_points = ', common_points)

        if common_points != 0:
            if common_points >= common_previous:
                found_plane = 0
                common_previous = common_points
                print('(while) iteration ', nbloop, ' - ', common_previous, 'points belonging to the facet for plane ',
                      label)
                nbloop = nbloop + 1
                crossed_surface = 1
            elif common_points < grown_points / 5:  # try to keep enough points for statistics, half step back
                found_plane = 1
                print('Exiting while loop after threshold reached - ', common_previous,
                      'points belonging to the facet for plane ', label, '- next step common points=', common_points)
            else:
                found_plane = 0
                common_previous = common_points
                print('(while) iteration ', nbloop, ' - ', common_previous, 'points belonging to the facet for plane ',
                      label)
                nbloop = nbloop + 1
                crossed_surface = 1
        else:
            if crossed_surface == 1:  # found the outer shell, which is 1 step before
                found_plane = 1
                print('Exiting while loop - ', common_previous, 'points belonging to the facet for plane ', label,
                      '- next step common points=', common_points)
            elif nbloop < 5:
                print('(while) iteration ', nbloop, ' - ', common_previous, 'points belonging to the facet for plane ',
                      label)
                nbloop = nbloop + 1
            else:
                if shift_direction == 1:  # already unsuccessful in the other direction
                    print('No point from support is intersecting the plane ', label)
                    stop = 1
                    break
                else:  # distance to support metric not reliable, start again in the other direction
                    shift_direction = 1
                    print('Shift scanning direction')
                    step_shift = -1 * step_shift
                    nbloop = 1

    if stop == 1:  # no points on the plane
        print('Intersecting with support: no points for plane', label)
        continue

    # go back one step
    coeffs[2] = coeffs[2] - (nbloop-1)*step_shift
    # shift indices
    plane_newindices0, plane_newindices1, plane_newindices2 = \
        fu.offset_plane(indices=plane_indices, offset=(nbloop-1)*step_shift, plane_normal=plane_normal)

    plane = np.zeros(surface.shape)
    plane[plane_newindices0, plane_newindices1, plane_newindices2] = 1

    # use only pixels belonging to the outer shell of the support
    plane = plane * surface

    if debug:
        # plot plane points overlaid with the support
        plane_indices = np.nonzero(plane == 1)
        gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                         np.concatenate((surf0[:, np.newaxis],
                                                         surf1[:, np.newaxis],
                                                         surf2[:, np.newaxis]), axis=1)),
                                 markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                 title='Plane' + str(label) + ' after finding the surface\n' +
                                       'Points number=' + str(len(plane_indices[0])))

    if plane[plane == 1].sum() == 0:  # no point belongs to the support
        print('Plane ', label, ' , no point belongs to support')
        continue

    #######################################
    # grow again the facet on the surface #
    #######################################
    print('Growing the facet at the surface')
    iterate = 0
    while stop == 0:
        previous_nb = plane[plane == 1].sum()
        plane, stop = fu.grow_facet(fit=coeffs, plane=plane, label=label, support=support,
                                    max_distance=1.5*max_distance_plane, debugging=False)
        # here the distance threshold is larger in order to reach voxels missed by the first plane fit
        # when rounding vertices to integer. Anyway we intersect it with the surface therefore it can not go crazy.
        plane_indices = np.nonzero(plane)
        iterate = iterate + 1
        plane = plane * surface  # use only pixels belonging to the outer shell of the support
        if plane[plane == 1].sum() == previous_nb:
            break
    grown_points = plane[plane == 1].sum().astype(int)
    print('Plane ', label, ', ', str(grown_points), 'points after growing facet at the surface')

    if debug:
        plane_indices = np.nonzero(plane == 1)
        surf0, surf1, surf2 = fu.surface_indices(surface=surface, plane_indices=plane_indices, margin=3)
        gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                         np.concatenate((surf0[:, np.newaxis],
                                                         surf1[:, np.newaxis],
                                                         surf2[:, np.newaxis]), axis=1)),
                                 markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                 title='Plane' + str(label) + ' after 1st growth at the surface\n iteration' +
                                       str(iterate) + '- Points number=' + str(len(plane_indices[0])))

    ################################################################
    # refine plane fit, now we are sure that we are at the surface #
    ################################################################
    coeffs, plane_indices, errors, stop = fu.fit_plane(plane=plane, label=label, debugging=debug)
    if stop == 1:
        print('No points remaining after refined fit for plane', label)
        continue

    if debug:
        surf0, surf1, surf2 = fu.surface_indices(surface=surface, plane_indices=plane_indices, margin=3)
        gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                         np.concatenate((surf0[:, np.newaxis],
                                                         surf1[:, np.newaxis],
                                                         surf2[:, np.newaxis]), axis=1)),
                                 markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                 title='Plane' + str(label) + ' after refined fit at surface\n iteration' +
                                       str(iterate) + '- Points number=' + str(len(plane_indices[0])))

    # update plane by filtering out pixels too far from the fit plane
    plane, stop = fu.distance_threshold(fit=coeffs, indices=plane_indices, shape=plane.shape,
                                        max_distance=max_distance_plane)
    if stop == 1:  # no points on the plane
        print('Refined fit: no points for plane', label)
        continue
    print('Plane', label, ', ', str(plane[plane == 1].sum()), 'points after refined fit')
    plane_indices = np.nonzero(plane)

    if debug:
        surf0, surf1, surf2 = fu.surface_indices(surface=surface, plane_indices=plane_indices, margin=3)
        gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                         np.concatenate((surf0[:, np.newaxis],
                                                         surf1[:, np.newaxis],
                                                         surf2[:, np.newaxis]), axis=1)),
                                 markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                 title='Plane' + str(label) + ' after distance threshold at surface\n' +
                                       'Points number=' + str(len(plane_indices[0])))

    ############################################
    # final growth of the facet on the surface #
    ############################################
    print('Final growth of the facet')
    iterate = 0
    while stop == 0:
        previous_nb = plane[plane == 1].sum()
        plane, stop = fu.grow_facet(fit=coeffs, plane=plane, label=label, support=support,
                                    max_distance=1.5*max_distance_plane, debugging=debug)
        plane = plane * surface  # use only pixels belonging to the outer shell of the support
        iterate = iterate + 1
        if plane[plane == 1].sum() == previous_nb:
            break
    grown_points = plane[plane == 1].sum().astype(int)
    # plot plane points overlaid with the support
    print('Plane ', label, ', ', str(grown_points), 'points after the final growth of the facet')

    if debug:
        plane_indices = np.nonzero(plane)
        surf0, surf1, surf2 = fu.surface_indices(surface=surface, plane_indices=plane_indices, margin=3)
        gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                         np.concatenate((surf0[:, np.newaxis],
                                                         surf1[:, np.newaxis],
                                                         surf2[:, np.newaxis]), axis=1)),
                                 markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                 title='Plane' + str(label) + ' final growth at the surface\nPoints number='
                                       + str(len(plane_indices[0])))

    #####################################
    # remove point belonging to an edge #
    #####################################
    plane[np.nonzero(edges)] = 0
    plane_indices = np.nonzero(plane)
    surf0, surf1, surf2 = fu.surface_indices(surface=surface, plane_indices=plane_indices, margin=3)
    gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                     np.concatenate((surf0[:, np.newaxis],
                                                     surf1[:, np.newaxis],
                                                     surf2[:, np.newaxis]), axis=1)),
                             markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                             title='Plane' + str(label) + ' after edge removal\nPoints number='
                                   + str(len(plane_indices[0])))
    print('Plane ', label, ', ', str(len(plane_indices[0])), 'points after removing edges')

    #################################################################
    # calculate quantities of interest and update log and VTK files #
    #################################################################
    # calculate mean gradient
    mean_gradient = np.zeros(3)
    ind_z = plane_indices[0]
    ind_y = plane_indices[1]
    ind_x = plane_indices[2]
    for point in range(len(plane_indices[0])):
        mean_gradient[0] = mean_gradient[0] + (ind_z[point] - zCOM)
        mean_gradient[1] = mean_gradient[1] + (ind_y[point] - yCOM)
        mean_gradient[2] = mean_gradient[2] + (ind_x[point] - xCOM)

    if np.linalg.norm(mean_gradient) == 0:
        print('gradient at surface is 0, cannot determine the correct direction of surface normal')
    else:
        mean_gradient = mean_gradient / np.linalg.norm(mean_gradient)

    # check the correct direction of the normal using the gradient of the support
    plane_normal = np.array([coeffs[0], coeffs[1], -1])  # normal is [a, b, c] if ax+by+cz+d=0
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    if np.dot(plane_normal, mean_gradient) < 0:  # normal is in the reverse direction
        print('Flip normal direction plane', str(label))
        plane_normal = -1 * plane_normal
    # correct plane_normal for anisotropic voxel size
    plane_normal = np.array([plane_normal[0] * 2 * np.pi / voxel_size[0],
                             plane_normal[1] * 2 * np.pi / voxel_size[1],
                             plane_normal[2] * 2 * np.pi / voxel_size[2]])
    plane_normal = plane_normal / np.linalg.norm(plane_normal)

    # check where is the measurement direction
    if projection_axis == 0:  # q aligned along the 1st axis
        ref_axis = np.array([1, 0, 0])
    elif projection_axis == 1:  # q aligned along the 2nd axis
        ref_axis = np.array([0, 1, 0])
    elif projection_axis == 2:  # q aligned along the 3rd axis
        ref_axis = np.array([0, 0, 1])
    else:
        print('projection_axis should be a basis axis of the reconstructed array')
        sys.exit()

    # calculate the angle of the plane normal to the measurement direction, which is aligned along projection_axis
    angle_plane = 180 / np.pi * np.arccos(np.dot(ref_axis, plane_normal))

    # update the log files
    fu.update_logfile(support=plane, strain_array=strain, summary_file=summary_file, allpoints_file=allpoints_file,
                      label=label, angle_plane=angle_plane, plane_coeffs=coeffs, plane_normal=plane_normal,
                      top_part=False)

    # update vti file
    PLANE = np.transpose(np.flip(plane, 2)).reshape(plane.size)  # VTK axis 2 is flipped
    plane_array = numpy_support.numpy_to_vtk(PLANE)
    pd.AddArray(plane_array)
    pd.GetArray(index_vti).SetName("plane_"+str(label))
    pd.Update()
    index_vti = index_vti + 1

##########################
# update and close files #
##########################
summary_file.write('\n'+'Isosurface value'+'\t' '{0: <10}'.format(str(support_threshold)))
allpoints_file.write('\n'+'Isosurface value'+'\t' '{0: <10}'.format(str(support_threshold)))
summary_file.close()
allpoints_file.close()

# update vti file with edges
EDGES = np.transpose((np.flip(edges, 2))).reshape(edges.size)
edges_array = numpy_support.numpy_to_vtk(EDGES)
pd.AddArray(edges_array)
pd.GetArray(index_vti).SetName("edges")
pd.Update()

# export data to file
writer = vtk.vtkXMLImageDataWriter()
writer.SetFileName(os.path.join(savedir, "S" + str(scan) + "_refined planes.vti"))
writer.SetInputData(image_data)
writer.Write()
print('\nEnd of script')
plt.ioff()
plt.show()
