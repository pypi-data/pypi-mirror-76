# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import hdf5plugin  # for P10, should be imported before h5py or PyTables
import numpy as np
from numpy.fft import fftn, fftshift
from matplotlib import pyplot as plt
from scipy.ndimage.measurements import center_of_mass
import tkinter as tk
from tkinter import filedialog
import xrayutilities as xu
from scipy.interpolate import interp1d
import gc
import sys
import os
sys.path.append('D:/myscripts/bcdi/')
sys.path.append('C:/Users/Jerome/Documents/myscripts/bcdi/')
import bcdi.graph.graph_utils as gu
import bcdi.experiment.experiment_utils as exp
import bcdi.preprocessing.preprocessing_utils as pru
import bcdi.postprocessing.postprocessing_utils as pu
import bcdi.utils.utilities as util

helptext = """
Calculate the resolution of a BCDI reconstruction using the phase retrieval transfer function (PRTF).

The measured diffraction pattern and reconstructions should be in the detector frame, before
phase ramp removal and centering.

For the laboratory frame, the CXI convention is used: z downstream, y vertical, x outboard
For q, the usual convention is used: qx downstream, qz vertical, qy outboard

Supported beamline: ESRF ID01, PETRAIII P10, SOLEIL SIXS, SOLEIL CRISTAL

Path structure: 
    specfile in /root_folder/
    data in /root_folder/S2191/data/
"""

scan = 1301
root_folder = 'C:/Users/Jerome/Documents/data/SIXS_2019/'  # location of the .spec or log file
savedir = 'C:/Users/Jerome/Documents/data/SIXS_2019/'  # PRTF will be saved here, leave it to '' otherwise
sample_name = "S"  # "SN"  #
comment = ""  # should start with _
crop_roi = []  # ROI used if 'center_auto' was True in PyNX, leave [] otherwise
# in the.cxi file, it is the parameter 'entry_1/image_1/process_1/configuration/roi_final'
align_pattern = False  # if True, will align the retrieved diffraction amplitude with the measured one
############################
# beamline parameters #
############################
beamline = 'SIXS_2019'  # name of the beamline, used for data loading and normalization by monitor
# supported beamlines: 'ID01', 'SIXS_2018', 'SIXS_2019', 'CRISTAL', 'P10'
is_series = False  # specific to series measurement at P10
rocking_angle = "inplane"  # "outofplane" or "inplane"
follow_bragg = False  # only for energy scans, set to True if the detector was also scanned to follow the Bragg peak
specfile_name = root_folder + 'alias_dict_2019.txt'
# .spec for ID01, .fio for P10, alias_dict.txt for SIXS_2018, not used for CRISTAL and SIXS_2019
# template for ID01: name of the spec file without '.spec'
# template for SIXS_2018: full path of the alias dictionnary 'alias_dict.txt', typically: root_folder + 'alias_dict.txt'
# template for SIXS_2019: ''
# template for P10: sample_name + '_%05d'
# template for CRISTAL: ''
#############################################################
# define detector related parameters and region of interest #
#############################################################
detector = "Maxipix"    # "Eiger2M" or "Maxipix" or "Eiger4M"
template_imagefile = 'Pt_ascan_mu_%05d.nxs'
# template for ID01: 'data_mpx4_%05d.edf.gz' or 'align_eiger2M_%05d.edf.gz'
# template for SIXS_2018: 'align.spec_ascan_mu_%05d.nxs'
# template for SIXS_2019: 'spare_ascan_mu_%05d.nxs'
# template for Cristal: 'S%d.nxs'
# template for P10: '_master.h5'
################################################################################
# parameters for calculating q values #
################################################################################
sdd = 1  # sample to detector distance in m
energy = 8000   # x-ray energy in eV, 6eV offset at ID01
beam_direction = (1, 0, 0)  # beam along x
sample_inplane = (1, 0, 0)  # sample inplane reference direction along the beam at 0 angles
sample_outofplane = (0, 0, 1)  # surface normal of the sample at 0 angles
pre_binning = (1, 3, 1)  # binning factor applied during preprocessing: rocking curve axis, detector vertical and
# horizontal axis. This is necessary to calculate correctly q values.
phasing_binning = (1, 2, 2)  # binning factor applied during phasing: rocking curve axis, detector vertical and
# horizontal axis.
# If the reconstructed object was further cropped after phasing, it will be automatically padded back to the FFT window
# shape used during phasing (after binning) before calculating the Fourier transform.
###############################
# only needed for simulations #
###############################
simulation = False  # True is this is simulated data, will not load the specfile
bragg_angle_simu = 17.1177  # value of the incident angle at Bragg peak (eta at ID01)
outofplane_simu = 35.3240  # detector delta @ ID01
inplane_simu = -1.6029  # detector nu @ ID01
tilt_simu = 0.0102  # angular step size for rocking angle, eta @ ID01
###########
# options #
###########
normalize_prtf = True  # set to True when the solution is the first mode - then the intensity needs to be normalized
debug = False  # True to show more plots
save = True  # True to save the prtf figure
##########################
# end of user parameters #
##########################

#################################################
# Initialize paths, detector, setup and logfile #
#################################################
kwargs = dict()  # create dictionnary
try:
    kwargs['is_series'] = is_series
except NameError:  # is_series not declared
    pass

detector = exp.Detector(name=detector, datadir='', template_imagefile=template_imagefile, binning=pre_binning, **kwargs)

setup = exp.SetupPreprocessing(beamline=beamline, rocking_angle=rocking_angle, distance=sdd, energy=energy,
                               beam_direction=beam_direction, sample_inplane=sample_inplane,
                               sample_outofplane=sample_outofplane,
                               offset_inplane=0)  # no need to worry about offsets, work relatively to the Bragg peak

print('\nScan', scan)
print('Setup: ', setup.beamline)
print('Detector: ', detector.name)
print('Pixel sizes after pre_binning (vertical, horizontal): ', detector.pixelsize_y, detector.pixelsize_x, '(m)')
print('Scan type: ', setup.rocking_angle)
print('Sample to detector distance: ', setup.distance, 'm')
print('Energy:', setup.energy, 'ev')

if simulation:
    detector.datadir = root_folder
    detector.savedir = root_folder
else:
    if setup.beamline != 'P10':
        homedir = root_folder + sample_name + str(scan) + '/'
        detector.datadir = homedir + "data/"
    else:
        specfile_name = specfile_name % scan
        homedir = root_folder + specfile_name + '/'
        detector.datadir = homedir + 'e4m/'
        template_imagefile = specfile_name + template_imagefile
        detector.template_imagefile = template_imagefile
    if savedir == '':
        detector.savedir = os.path.abspath(os.path.join(detector.datadir, os.pardir))
    else:
        detector.savedir = savedir
    print('Datadir:', detector.datadir)
    print('Savedir:', detector.savedir)
    logfile = pru.create_logfile(setup=setup, detector=detector, scan_number=scan, root_folder=root_folder,
                                 filename=specfile_name)

#############################################
# Initialize geometry for orthogonalization #
#############################################
qconv, offsets = pru.init_qconversion(setup)
detector.offsets = offsets
hxrd = xu.experiment.HXRD(sample_inplane, sample_outofplane, qconv=qconv)  # x downstream, y outboard, z vertical
# first two arguments in HXRD are the inplane reference direction along the beam and surface normal of the sample

###################
# define colormap #
###################
colormap = gu.Colormap()
my_cmap = colormap.cmap

###################################
# load experimental data and mask #
###################################
plt.ion()
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir=detector.savedir, title="Select diffraction pattern",
                                       filetypes=[("NPZ", "*.npz"), ("NPY", "*.npy")])
diff_pattern, _ = util.load_file(file_path)
diff_pattern = diff_pattern.astype(float)

file_path = filedialog.askopenfilename(initialdir=detector.savedir, title="Select mask",
                                       filetypes=[("NPZ", "*.npz"), ("NPY", "*.npy")])
mask, _ = util.load_file(file_path)

# crop the diffraction pattern and the mask to compensate the "auto_center_resize" option used in PyNX.
# The shape will be equal to 'roi_final' parameter of the .cxi file
if len(crop_roi) == 6:
    diff_pattern = diff_pattern[crop_roi[0]:crop_roi[1], crop_roi[2]:crop_roi[3], crop_roi[4]:crop_roi[5]]
    mask = mask[crop_roi[0]:crop_roi[1], crop_roi[2]:crop_roi[3], crop_roi[4]:crop_roi[5]]
elif len(crop_roi) != 0:
    print('Crop_roi should be a list of 6 integers or a blank list!')
    sys.exit()

# bin the diffraction pattern and the mask to compensate the "rebin" option used in PyNX.
# update also the detector pixel sizes to take into account the binning
detector.pixelsize_y = detector.pixelsize_y * phasing_binning[1]
detector.pixelsize_x = detector.pixelsize_x * phasing_binning[2]
final_binning = np.multiply(pre_binning, phasing_binning)
detector.binning = final_binning
print('Pixel sizes after phasing_binning (vertical, horizontal): ', detector.pixelsize_y, detector.pixelsize_x, '(m)')
diff_pattern = pu.bin_data(array=diff_pattern, binning=phasing_binning, debugging=False)
mask = pu.bin_data(array=mask, binning=phasing_binning, debugging=False)

numz, numy, numx = diff_pattern.shape  # this shape will be used for the calculation of q values
print('\nMeasured data shape =', numz, numy, numx, ' Max(measured amplitude)=', np.sqrt(diff_pattern).max())
diff_pattern[np.nonzero(mask)] = 0

z0, y0, x0 = center_of_mass(diff_pattern)
z0, y0, x0 = [int(z0), int(y0), int(x0)]
print("COM of measured pattern after masking: ", z0, y0, x0, ' Number of unmasked photons =', diff_pattern.sum())

fig, _, _ = gu.multislices_plot(np.sqrt(diff_pattern), sum_frames=False, title='3D diffraction amplitude', vmin=0,
                                vmax=3.5, is_orthogonal=False, reciprocal_space=True, slice_position=[z0, y0, x0],
                                scale='log', plot_colorbar=True)

plt.figure()
plt.imshow(np.log10(np.sqrt(diff_pattern).sum(axis=0)), cmap=my_cmap, vmin=0, vmax=3.5)
plt.title('abs(diffraction amplitude).sum(axis=0)')
plt.colorbar()
plt.pause(0.1)

################################################
# calculate the q matrix respective to the COM #
################################################
hxrd.Ang2Q.init_area('z-', 'y+', cch1=int(y0), cch2=int(x0), Nch1=numy, Nch2=numx,
                     pwidth1=detector.pixelsize_y, pwidth2=detector.pixelsize_x, distance=setup.distance)
# first two arguments in init_area are the direction of the detector
if simulation:
    eta = bragg_angle_simu + tilt_simu * (np.arange(0, numz, 1) - int(z0))
    qx, qy, qz = hxrd.Ang2Q.area(eta, 0, 0, inplane_simu, outofplane_simu, delta=(0, 0, 0, 0, 0))
else:
    qx, qz, qy, _ = pru.regrid(logfile=logfile, nb_frames=numz, scan_number=scan, detector=detector,
                               setup=setup, hxrd=hxrd, follow_bragg=follow_bragg)

if debug:
    gu.combined_plots(tuple_array=(qz, qy, qx), tuple_sum_frames=False, tuple_sum_axis=(0, 1, 2),
                      tuple_width_v=None, tuple_width_h=None, tuple_colorbar=True, tuple_vmin=np.nan,
                      tuple_vmax=np.nan, tuple_title=('qz', 'qy', 'qx'), tuple_scale='linear')

qxCOM = qx[z0, y0, x0]
qyCOM = qy[z0, y0, x0]
qzCOM = qz[z0, y0, x0]
print('COM[qx, qy, qz] = ', qxCOM, qyCOM, qzCOM)
distances_q = np.sqrt((qx - qxCOM)**2 + (qy - qyCOM)**2 + (qz - qzCOM)**2)  # if reconstructions are centered
#  and of the same shape q values will be identical
del qx, qy, qz
gc.collect()

if distances_q.shape != diff_pattern.shape:
    print('\nThe shape of q values and the shape of the diffraction pattern are different: check binning parameters!')
    sys.exit()

if debug:
    gu.multislices_plot(distances_q, sum_frames=False, plot_colorbar=True, cmap=my_cmap,
                        title='distances_q', scale='linear', vmin=np.nan, vmax=np.nan,
                        reciprocal_space=True)

#############################
# load reconstructed object #
#############################
file_path = filedialog.askopenfilename(initialdir=detector.savedir, title="Select reconstructions (prtf)",
                                       filetypes=[("NPZ", "*.npz"), ("NPY", "*.npy"),
                                                  ("CXI", "*.cxi"), ("HDF5", "*.h5")])

obj, extension = util.load_file(file_path)
print('Opening ', file_path)

if extension == '.h5':
    comment = comment + '_mode'

# check if the shape of the real space object is the same as the measured diffraction pattern
# the real space object may have been further cropped to a tight support, to save memory space.
if obj.shape != diff_pattern.shape:
    print('Reconstructed object shape = ', obj.shape, 'different from the experimental diffraction pattern: crop/pad')
    obj = pu.crop_pad(array=obj, output_shape=diff_pattern.shape, debugging=False)

# calculate the retrieved diffraction amplitude
phased_fft = fftshift(fftn(obj)) / (np.sqrt(numz)*np.sqrt(numy)*np.sqrt(numx))  # complex amplitude
del obj
gc.collect()

if debug:
    plt.figure()
    plt.imshow(np.log10(abs(phased_fft).sum(axis=0)), cmap=my_cmap, vmin=0, vmax=3.5)
    plt.colorbar()
    plt.title('abs(retrieved amplitude).sum(axis=0) before alignment')
    plt.pause(0.1)

if align_pattern:
    # align the reconstruction with the initial diffraction data
    phased_fft, _ = pru.align_diffpattern(reference_data=diff_pattern, data=phased_fft, method='registration',
                                          combining_method='subpixel')

plt.figure()
plt.imshow(np.log10(abs(phased_fft).sum(axis=0)), cmap=my_cmap, vmin=0, vmax=3.5)
plt.title('abs(retrieved amplitude).sum(axis=0)')
plt.colorbar()
plt.pause(0.1)

phased_fft[np.nonzero(mask)] = 0  # do not take mask voxels into account
print('Max(retrieved amplitude) =', abs(phased_fft).max())
print('COM of the retrieved diffraction pattern after masking: ', center_of_mass(abs(phased_fft)))
del mask
gc.collect()

gu.combined_plots(tuple_array=(diff_pattern, phased_fft), tuple_sum_frames=False, tuple_sum_axis=(0, 0),
                  tuple_width_v=None, tuple_width_h=None, tuple_colorbar=False, tuple_vmin=(-1, -1),
                  tuple_vmax=np.nan, tuple_title=('measurement', 'phased_fft'), tuple_scale='log')

#########################
# calculate the 3D PRTF #
#########################
diff_pattern[diff_pattern == 0] = np.nan  # discard zero valued pixels
prtf_matrix = abs(phased_fft) / np.sqrt(diff_pattern)

gu.multislices_plot(prtf_matrix, sum_frames=False, plot_colorbar=True, cmap=my_cmap,
                    title='prtf_matrix', scale='linear', vmin=0, vmax=1.1,
                    reciprocal_space=True)

#################################
# average over spherical shells #
#################################
print('Distance max:', distances_q.max(), ' (1/A) at: ', np.unravel_index(abs(distances_q).argmax(), distances_q.shape))
nb_bins = numz // 3
prtf_avg = np.zeros(nb_bins)
dq = distances_q.max() / nb_bins  # in 1/A
q_axis = np.linspace(0, distances_q.max(), endpoint=True, num=nb_bins+1)  # in 1/A

for index in range(nb_bins):
    logical_array = np.logical_and((distances_q < q_axis[index+1]), (distances_q >= q_axis[index]))
    temp = prtf_matrix[logical_array]
    prtf_avg[index] = temp[~np.isnan(temp)].mean()
q_axis = q_axis[:-1]

if normalize_prtf:
    print('Normalizing the PRTF to 1 ...')
    prtf_avg = prtf_avg / prtf_avg[~np.isnan(prtf_avg)].max()  # normalize to 1

#############################
# plot and save the 1D PRTF #
#############################
defined_q = 10 * q_axis[~np.isnan(prtf_avg)]

# create a new variable 'arc_length' to predict q and prtf parametrically (because prtf is not monotonic)
arc_length = np.concatenate((np.zeros(1),
                             np.cumsum(np.diff(prtf_avg[~np.isnan(prtf_avg)])**2 + np.diff(defined_q)**2)),
                            axis=0)  # cumulative linear arc length, used as the parameter
arc_length_interp = np.linspace(0, arc_length[-1], 10000)
fit_prtf = interp1d(arc_length, prtf_avg[~np.isnan(prtf_avg)], kind='linear')
prtf_interp = fit_prtf(arc_length_interp)
idx_resolution = [i for i, x in enumerate(prtf_interp) if x < 1/np.e]  # indices where prtf < 1/e

fit_q = interp1d(arc_length, defined_q, kind='linear')
q_interp = fit_q(arc_length_interp)

plt.figure()
plt.plot(prtf_avg[~np.isnan(prtf_avg)], defined_q, 'o', prtf_interp, q_interp, '.r')
plt.xlabel('PRTF')
plt.ylabel('q (1/nm)')

try:
    q_resolution = q_interp[min(idx_resolution)]
except ValueError:
    print('Resolution limited by the 1 photon counts only (min(prtf)>1/e)')
    print('min(PRTF) = ', prtf_avg[~np.isnan(prtf_avg)].min())
    q_resolution = 10 * q_axis[len(prtf_avg[~np.isnan(prtf_avg)])-1]
print('q resolution =', str('{:.5f}'.format(q_resolution)), ' (1/nm)')
print('resolution d= ' + str('{:.3f}'.format(2*np.pi / q_resolution)) + 'nm')

fig = plt.figure()
plt.plot(defined_q, prtf_avg[~np.isnan(prtf_avg)], 'or')  # q_axis in 1/nm
plt.title('PRTF')
plt.xlabel('q (1/nm)')
plt.plot([defined_q.min(), defined_q.max()], [1/np.e, 1/np.e], 'k.', lw=1)
plt.xlim(defined_q.min(), defined_q.max())
plt.ylim(0, 1.1)
if save:
    plt.savefig(detector.savedir + 'S' + str(scan) + '_prtf' + comment + '.png')
fig.text(0.15, 0.25, "Scan " + str(scan) + comment, size=14)
fig.text(0.15, 0.20, "q at PRTF=1/e: " + str('{:.5f}'.format(q_resolution)) + '(1/nm)', size=14)
fig.text(0.15, 0.15, "resolution d= " + str('{:.3f}'.format(2*np.pi / q_resolution)) + 'nm', size=14)
if save:
    plt.savefig(detector.savedir + 'S' + str(scan) + '_prtf_comments' + comment + '.png')
plt.ioff()
plt.show()
