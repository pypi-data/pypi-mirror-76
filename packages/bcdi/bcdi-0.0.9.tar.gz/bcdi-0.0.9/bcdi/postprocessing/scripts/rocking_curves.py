# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import hdf5plugin  # for P10, should be imported before h5py or PyTables
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage.measurements import center_of_mass
import sys
sys.path.append('D:/myscripts/bcdi/')
import bcdi.experiment.experiment_utils as exp
import bcdi.preprocessing.preprocessing_utils as pru
import bcdi.graph.graph_utils as gu

helptext = """
Open a series of rocking curve data and track the position of the Bragg peak over the series.

Supported beamlines: ESRF ID01, PETRAIII P10, SOLEIL SIXS, SOLEIL CRISTAL, MAX IV NANOMAX.
"""
scans = np.arange(1460, 1475+1, step=3)  # list or array of scan numbers
scans = np.concatenate((scans, np.arange(1484, 1586+1, 3)))
scans = np.concatenate((scans, np.arange(1591, 1633+1, 3)))
scans = np.concatenate((scans, np.arange(1638, 1680+1, 3)))

root_folder = "D:/data/P10_OER/data/"
sample_name = "dewet2_2"  # list of sample names. If only one name is indicated,
# it will be repeated to match the number of scans
savedir = "D:/data/P10_OER/analysis/candidate_12/"
# images will be saved here, leave it to '' otherwise (default to root_folder)
x_axis = []
[x_axis.append(0.740) for _ in range(16)]
[x_axis.append(0.80) for _ in range(10)]
[x_axis.append(-0.05) for _ in range(15)]
[x_axis.append(0.3) for _ in range(15)]
[x_axis.append(0.8) for _ in range(15)]
# values against which the Bragg peak center of mass evolution will be plotted, leave [] otherwise
x_label = 'voltage (V)'  # label for the X axis in plots, leave '' otherwise
comment = '_BCDI_RC'  # comment for the saving filename, should start with _
strain_range = 0.00005  # range for the plot of the q value
peak_method = 'max_com'  # Bragg peak determination: 'max', 'com', 'max_com' (max then com)
debug = False  # set to True to see more plots
###############################
# beamline related parameters #
###############################
beamline = 'P10'  # name of the beamline, used for data loading and normalization by monitor
# supported beamlines: 'ID01', 'SIXS_2018', 'SIXS_2019', 'CRISTAL', 'P10'

custom_scan = False  # True for a stack of images acquired without scan, e.g. with ct in a macro (no info in spec file)
custom_images = np.arange(11353, 11453, 1)  # list of image numbers for the custom_scan
custom_monitor = np.ones(len(custom_images))  # monitor values for normalization for the custom_scan
custom_motors = {"eta": np.linspace(16.989, 18.989, num=100, endpoint=False), "phi": 0, "nu": -0.75, "delta": 36.65}
# ID01: eta, phi, nu, delta
# CRISTAL: mgomega, gamma, delta
# P10: om, phi, chi, mu, gamma, delta
# SIXS: beta, mu, gamma, delta

rocking_angle = "outofplane"  # "outofplane" or "inplane"
is_series = False  # specific to series measurement at P10
specfile_name = ''
# .spec for ID01, .fio for P10, alias_dict.txt for SIXS_2018, not used for CRISTAL and SIXS_2019
# template for ID01: name of the spec file without '.spec'
# template for SIXS_2018: full path of the alias dictionnary 'alias_dict.txt', typically: root_folder + 'alias_dict.txt'
# template for SIXS_2019: ''
# template for P10: ''
# template for CRISTAL: ''
###############################
# detector related parameters #
###############################
detector = "Eiger4M"    # "Eiger2M" or "Maxipix" or "Eiger4M"
x_bragg = 1387  # horizontal pixel number of the Bragg peak, can be used for the definition of the ROI
y_bragg = 809  # vertical pixel number of the Bragg peak, can be used for the definition of the ROI
roi_detector = [y_bragg-200, y_bragg+200, x_bragg-400, x_bragg+400]  # [Vstart, Vstop, Hstart, Hstop]
# leave it as [] to use the full detector. Use with center_fft='skip' if you want this exact size.
debug_pix = 40  # half-width in pixels of the ROI centered on the Bragg peak
hotpixels_file = ''  # root_folder + 'hotpixels.npz'  #
flatfield_file = ''  # root_folder + "flatfield_8.5kev.npz"  #
template_imagefile = '_master.h5'
# template for ID01: 'data_mpx4_%05d.edf.gz' or 'align_eiger2M_%05d.edf.gz'
# template for SIXS_2018: 'align.spec_ascan_mu_%05d.nxs'
# template for SIXS_2019: 'spare_ascan_mu_%05d.nxs'
# template for Cristal: 'S%d.nxs'
# template for P10: '_master.h5'
####################################
# q calculation related parameters #
####################################
convert_to_q = True  # True to convert from pixels to q values using parameters below
beam_direction = (1, 0, 0)  # beam along z
directbeam_x = 476  # x horizontal,  cch2 in xrayutilities
directbeam_y = 1374  # y vertical,  cch1 in xrayutilities
direct_inplane = -2.0  # outer angle in xrayutilities
direct_outofplane = 0.8
sdd = 1.83  # sample to detector distance in m
energy = 10300  # in eV, offset of 6eV at ID01
##################################
# end of user-defined parameters #
##################################

###################
# define colormap #
###################
bad_color = '1.0'  # white
bckg_color = '0.7'  # grey
colormap = gu.Colormap(bad_color=bad_color)
my_cmap = colormap.cmap

########################################
# check and initialize some parameters #
########################################
print('\n{:d} scans:'.format(len(scans)), scans)
print('\n {:d} x_axis values provided:'.format(len(x_axis)))
if len(x_axis) == 0:
    x_axis = np.arange(len(scans))
assert len(x_axis) == len(scans), 'the length of x_axis should be equal to the number of scans'

if type(sample_name) is list:
    if len(sample_name) == 1:
        sample_name = [sample_name[0] for idx in range(len(scans))]
    assert len(sample_name) == len(scans), 'sample_name and scan_list should have the same length'
elif type(sample_name) is str:
    sample_name = [sample_name for idx in range(len(scans))]
else:
    print('sample_name should be either a string or a list of strings')
    sys.exit()
assert peak_method in ['max', 'com', 'max_com'], 'invalid value for "peak_method" parameter'

int_sum = []  # integrated intensity in the detector ROI
int_max = []  # maximum intensity in the detector ROI
zcom = []  # center of mass for the first data axis
ycom = []  # center of mass for the second data axis
xcom = []  # center of mass for the third data axis
tilt_com = []  # center of mass for the incident rocking angle
q_com = []  # q value of the center of mass
check_roi = []  # a small ROI around the Bragg peak will be stored for each scan, to see if the peak is indeed
# captured by the rocking curve

#################################
# Initialize detector and setup #
#################################
kwargs = dict()  # create dictionnary
kwargs['is_series'] = is_series
detector = exp.Detector(name=detector, datadir='', template_imagefile=template_imagefile, roi=roi_detector, **kwargs)

setup_pre = exp.SetupPreprocessing(beamline=beamline, energy=energy, rocking_angle=rocking_angle,
                                   custom_scan=custom_scan, custom_images=custom_images, custom_monitor=custom_monitor,
                                   custom_motors=custom_motors)

flatfield = pru.load_flatfield(flatfield_file)
hotpix_array = pru.load_hotpixels(hotpixels_file)

print('Setup: ', setup_pre.beamline)
print('Detector: ', detector.name)
print('Pixel number (VxH): ', detector.nb_pixel_y, detector.nb_pixel_x)
print('Detector ROI:', roi_detector)
print('Horizontal pixel size with binning: ', detector.pixelsize_x, 'm')
print('Vertical pixel size with binning: ', detector.pixelsize_y, 'm')
print('Scan type: ', setup_pre.rocking_angle)

if savedir == '':
    savedir = root_folder
detector.savedir = savedir
print('savedir: ', detector.savedir)

###############################################
# load recursively the scans and update lists #
###############################################
for scan_id in range(len(scans)):

    if setup_pre.beamline != 'P10':
        homedir = root_folder + sample_name[scan_id] + str(scans[scan_id]) + '/'
        detector.datadir = homedir + "data/"
        specfile = specfile_name
    else:
        specfile = sample_name[scan_id] + '_{:05d}'.format(scans[scan_id])
        homedir = root_folder + specfile + '/'
        detector.datadir = homedir + 'e4m/'
        imagefile = specfile + template_imagefile
        detector.template_imagefile = imagefile

    logfile = pru.create_logfile(setup=setup_pre, detector=detector, scan_number=scans[scan_id],
                                 root_folder=root_folder, filename=specfile)

    print('\nScan', scans[scan_id])
    print('Specfile: ', specfile)

    data, mask, frames_logical, monitor = pru.load_bcdi_data(logfile=logfile, scan_number=scans[scan_id],
                                                             detector=detector, setup=setup_pre,
                                                             flatfield=flatfield, hotpixels=hotpix_array,
                                                             normalize=True, debugging=debug)

    tilt, grazing, inplane, outofplane = pru.motor_values(frames_logical=frames_logical, logfile=logfile,
                                                          scan_number=scan_id, setup=setup_pre)

    nbz, nby, nbx = data.shape
    if peak_method == 'max':
        piz, piy, pix = np.unravel_index(data.argmax(), shape=(nbz, nby, nbx))
    elif peak_method == 'com':
        piz, piy, pix = center_of_mass(data)
    else:  # 'max_com'
        max_z, max_y, max_x = np.unravel_index(data.argmax(), shape=data.shape)
        com_z, com_y, com_x = center_of_mass(data[:, int(max_y) - debug_pix:int(max_y) + debug_pix,
                                                  int(max_x) - debug_pix:int(max_x) + debug_pix])
        # correct the pixel offset due to the ROI defined by debug_pix around the max
        piz = com_z  # the data was not cropped along the first axis
        piy = com_y + max_y - debug_pix
        pix = com_x + max_x - debug_pix

    if debug:
        fig, _, _ = gu.multislices_plot(data, sum_frames=True, plot_colorbar=True, cmap=my_cmap,
                                        title='scan'+str(scans[scan_id]), scale='log', is_orthogonal=False,
                                        reciprocal_space=True)
        fig.text(0.60, 0.30, "(piz, piy, pix) = ({:.1f}, {:.1f}, {:.1f})".format(piz, piy, pix), size=12)
        plt.draw()

        if peak_method == 'max_com':
            fig, _, _ = gu.multislices_plot(data[:, int(max_y) - debug_pix:int(max_y) + debug_pix,
                                                 int(max_x) - debug_pix:int(max_x) + debug_pix], sum_frames=True,
                                            plot_colorbar=True, cmap=my_cmap, title='scan'+str(scans[scan_id]),
                                            scale='log', is_orthogonal=False, reciprocal_space=True)
            fig.text(0.60, 0.30, "(com_z, com_y, com_x) = ({:.1f}, {:.1f}, {:.1f})".format(com_z, com_y, com_x),
                     size=12)
            plt.draw()
        print('')
    zcom.append(piz)
    ycom.append(piy)
    xcom.append(pix)
    int_sum.append(data.sum())
    int_max.append(data.max())
    check_roi.append(data[:, :, int(pix) - debug_pix:int(pix) + debug_pix].sum(axis=1))
    interp_tilt = interp1d(np.arange(data.shape[0]), tilt, kind='linear')
    tilt_com.append(interp_tilt(piz))

    ##############################
    # convert pixels to q values #
    ##############################
    if convert_to_q:
        setup_post = exp.SetupPostprocessing(beamline=setup_pre.beamline, energy=setup_pre.energy,
                                             outofplane_angle=outofplane, inplane_angle=inplane, tilt_angle=tilt,
                                             rocking_angle=setup_pre.rocking_angle, grazing_angle=grazing,
                                             distance=setup_pre.distance, pixel_x=detector.pixelsize_x,
                                             pixel_y=detector.pixelsize_y)

        # calculate the position of the Bragg peak in full detector pixels
        bragg_x = detector.roi[2] + pix
        bragg_y = detector.roi[0] + piy

        # calculate the position of the direct beam at 0 detector angles
        x_direct_0 = directbeam_x + setup_post.rotation_direction() * \
            (direct_inplane * np.pi / 180 * sdd / detector.pixelsize_x)  # rotation_direction is +1 or -1
        y_direct_0 = directbeam_y - direct_outofplane * np.pi / 180 * sdd / detector.pixelsize_y
        # outofplane is always clockwise

        # claculate corrected detector angles for the Bragg peak
        bragg_inplane = inplane + setup_post.rotation_direction() * \
            (detector.pixelsize_x * (bragg_x - x_direct_0) / sdd * 180 / np.pi)  # rotation_direction is +1 or -1
        bragg_outofplane = outofplane - detector.pixelsize_y * (bragg_y - y_direct_0) / sdd * 180 / np.pi
        # outofplane always clockwise
        print("Bragg angles before correction = (gam, del): ", str('{:.4f}'.format(inplane)),
              str('{:.4f}'.format(outofplane)))
        print("Bragg angles after correction = (gam, del): ", str('{:.4f}'.format(bragg_inplane)),
              str('{:.4f}'.format(bragg_outofplane)))

        # update setup_post with the corrected detector angles
        setup_post.inplane_angle = bragg_inplane
        setup_post.outofplane_angle = bragg_outofplane

        ##############################################################
        # wavevector transfer calculations (in the laboratory frame) #
        ##############################################################
        kin = 2 * np.pi / setup_post.wavelength * np.asarray(beam_direction)
        # in lab frame z downstream, y vertical, x outboard
        kout = setup_post.exit_wavevector()  # in lab.frame z downstream, y vertical, x outboard
        q = (kout - kin) / 1e10  # convert from 1/m to 1/angstrom
        q_com.append(np.linalg.norm(q))
        print("Wavevector transfer of Bragg peak: ", q, str('{:.4f}'.format(np.linalg.norm(q))))

##########################################################
# plot the ROI centered on the Bragg peak for each scan  #
##########################################################
plt.ion()

# plot maximum 7x7 ROIs per figure
nb_fig = 1 + len(scans) // 49
if nb_fig == 1:
    nb_rows = np.floor(np.sqrt(len(scans)))
    nb_columns = np.ceil(len(scans) / nb_rows)
else:
    nb_rows = 7
    nb_columns = 7

scan_counter = 0
for fig_idx in range(nb_fig):
    fig = plt.figure(figsize=(12, 9))
    for idx in range(min(49, len(scans)-scan_counter)):
        axis = plt.subplot(nb_rows, nb_columns, idx+1)
        axis.imshow(np.log10(check_roi[scan_counter]))
        axis.set_title('S{:d}'.format(scans[scan_counter]))
        scan_counter = scan_counter + 1
    plt.tight_layout()
    plt.pause(0.1)
    fig.savefig(savedir + 'check-roi' + str(fig_idx+1) + comment + '.png')

##########################################################
# plot the evolution of the center of mass and intensity #
##########################################################
fig, ((ax0, ax1, ax2), (ax3, ax4, ax5)) = plt.subplots(nrows=2, ncols=3, figsize=(12, 9))
ax0.plot(scans, x_axis, '-o')
ax0.set_xlabel('Scan number')
ax0.set_ylabel(x_label)
ax1.scatter(x_axis, int_sum, s=24, c=scans, cmap=my_cmap)
ax1.set_xlabel(x_label)
ax1.set_ylabel('Integrated intensity')
ax1.set_facecolor(bckg_color)
ax2.scatter(x_axis, int_max, s=24, c=scans, cmap=my_cmap)
ax2.set_xlabel(x_label)
ax2.set_ylabel('Maximum intensity')
ax2.set_facecolor(bckg_color)
ax3.scatter(x_axis, xcom, s=24, c=scans, cmap=my_cmap)
ax3.set_xlabel(x_label)
if peak_method in ['com', 'max_com']:
    ax3.set_ylabel('xcom (pixels)')
else:  # 'max'
    ax3.set_ylabel('xmax (pixels)')
ax3.set_facecolor(bckg_color)
ax4.scatter(x_axis, ycom, s=24, c=scans, cmap=my_cmap)
ax4.set_xlabel(x_label)
if peak_method in ['com', 'max_com']:
    ax4.set_ylabel('ycom (pixels)')
else:  # 'max'
    ax4.set_ylabel('ymax (pixels)')
ax4.set_facecolor(bckg_color)
plt5 = ax5.scatter(x_axis, zcom, s=24, c=scans, cmap=my_cmap)
gu.colorbar(plt5, scale='linear', numticks=min(len(scans), 20), label='scan #')
ax5.set_xlabel(x_label)
if peak_method in ['com', 'max_com']:
    ax5.set_ylabel('zcom (pixels)')
else:  # 'max'
    ax5.set_ylabel('zmax (pixels)')
ax5.set_facecolor(bckg_color)
plt.tight_layout()
plt.pause(0.1)
fig.savefig(savedir + 'summary' + comment + '.png')

############################################
# plot the evolution of the incident angle #
############################################
tilt_com = np.asarray(tilt_com)
x_axis = np.asarray(x_axis)
uniq_xaxis = np.unique(x_axis)
mean_tilt = np.empty(len(uniq_xaxis))
std_tilt = np.empty(len(uniq_xaxis))
for idx in range(len(uniq_xaxis)):
    mean_tilt[idx] = np.mean(tilt_com[x_axis == uniq_xaxis[idx]])
    std_tilt[idx] = np.std(tilt_com[x_axis == uniq_xaxis[idx]])

fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(12, 9))
ax0.plot(scans, tilt_com, '-o')
ax0.set_xlabel('Scan number')
ax0.set_ylabel('Bragg angle (deg)')
ax1.errorbar(uniq_xaxis, mean_tilt, yerr=std_tilt, elinewidth=2, capsize=6, capthick=2, linestyle='',
             marker='o', markersize=6, markerfacecolor='w')
ax1.set_xlabel(x_label)
ax1.set_ylabel('Bragg angle (deg)')
plt2 = ax2.scatter(x_axis, tilt_com, s=24, c=scans, cmap=my_cmap)
gu.colorbar(plt2, scale='linear', numticks=min(len(scans), 20), label='scan #')
ax2.set_xlabel(x_label)
ax2.set_ylabel('Bragg angle (deg)')
ax2.set_facecolor(bckg_color)
plt.tight_layout()
plt.pause(0.1)
fig.savefig(savedir + 'Bragg angle' + comment + '.png')

##############################################
# plot the evolution of the diffusion vector #
##############################################
if convert_to_q:
    q_com = np.asarray(q_com)
    mean_q = np.empty(len(uniq_xaxis))
    std_q = np.empty(len(uniq_xaxis))
    for idx in range(len(uniq_xaxis)):
        mean_q[idx] = np.mean(q_com[x_axis == uniq_xaxis[idx]])
        std_q[idx] = np.std(q_com[x_axis == uniq_xaxis[idx]])

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(12, 9))
    ax0.plot(scans, q_com, '-o')
    ax0.set_xlabel('Scan number')
    ax0.set_ylabel('q (1/A)')
    ax1.errorbar(uniq_xaxis, mean_q, yerr=std_q, elinewidth=2, capsize=6, capthick=2, linestyle='',
                 marker='o', markersize=6, markerfacecolor='w')
    ax1.set_xlabel(x_label)
    ax1.set_ylabel('q (1/A)')
    plt2 = ax2.scatter(x_axis, q_com, s=24, c=scans, cmap=my_cmap)
    gu.colorbar(plt2, scale='linear', numticks=min(len(scans), 20), label='scan #')
    ax2.set_xlabel(x_label)
    ax2.set_ylabel('q (1/A)')
    ax2.set_ylim(bottom=min(q_com)-strain_range, top=max(q_com)+strain_range)
    ax2.set_facecolor(bckg_color)
    plt.tight_layout()
    plt.pause(0.1)
    fig.savefig(savedir + 'diffusion vector' + comment + '.png')

plt.ioff()
plt.show()
