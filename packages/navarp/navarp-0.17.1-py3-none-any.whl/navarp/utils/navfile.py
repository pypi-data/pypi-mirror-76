#!/usr/bin/env python

##############################################################################
##
# This file is part of NavARP
##
# Copyright 2016 CELLS / ALBA Synchrotron, Cerdanyola del Vallès, Spain
##
# NavARP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# NavARP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##
# You should have received a copy of the GNU General Public License
# along with NavARP.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This module is part of the Python NavARP library. It defines the base
class for the data used in NavARP."""

__author__ = ["Federico Bisti"]
__license__ = "GPL"
__date__ = "21/03/2017"

import numpy as np
import h5py

import os
import glob
import re

import yaml

try:
    import igor.igorpy as igor  # For opening pxt files
except ImportError:
    print("WARNING: igor package not found. " +
          "It is not necessary but, if present, "
          "pxt files can be loaded.\n")


class NavAnalyzer:
    """NavAnalyzer is the class for the analyzer and its geometry

    NavAnalyzer is defined from the NavEntry, and it considers the experimental
    set-ups of Lorea/ALBA(ES), I05/Diamond(GB), SXARPES-ADRESS/PSI(CH) and
    Antares/Soleil(FR).

    Attributes:
        tht_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane of the slit (theta, so the name "tht_ap");
        phi_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane perpendicular to the slit (phi, so the name "phi_ap");
        work_fun (float): analyzer work function;
        deflector (Boolean): if True, the analyzer is using a deflector, so it
            can collect electrons out from the slit plane;
        scan_type (str): acquisition method.

        _set_def_lorea_alba: Set defaul values for Lorea/ALBA(ES)
        _set_def_i05_diamond: Set defaul values for I05/Diamond(GB)
        _set_def_sxarpes_psi: Set defaul values for SXARPES-ADRESS/PSI(CH)
        _set_def_antares_soleil: Set defaul values for Antares/Soleil(FR)
    """

    def __init__(self, tht_ap=50, phi_ap=0, work_fun=4.5, deflector=False):
        self.tht_ap = tht_ap
        self.phi_ap = phi_ap
        self.work_fun = work_fun
        self.deflector = deflector

    def get_attr(self):
        return self.tht_ap, self.phi_ap, self.work_fun, self.deflector

    def set_attr(self, tht_ap, phi_ap, work_fun, deflector):
        self.tht_ap = tht_ap
        self.phi_ap = phi_ap
        self.work_fun = work_fun
        self.deflector = deflector

    def _set_def_lorea_alba(self):
        self.tht_ap = 55
        self.phi_ap = 0
        self.work_fun = 4.6
        self.deflector = True

    def _set_def_i05_diamond(self):
        self.tht_ap = 0
        self.phi_ap = 50
        self.work_fun = 4.5
        self.deflector = False

    def _set_def_sxarpes_psi(self):
        self.tht_ap = -70
        self.phi_ap = 0
        self.work_fun = 4.5
        self.deflector = False

    def _set_def_antares_soleil(self):
        self.tht_ap = 55
        self.phi_ap = 0
        self.work_fun = 4.5
        self.deflector = True

    def _set_def_cassiopee_soleil(self):
        self.tht_ap = 0
        self.phi_ap = 50
        self.work_fun = 4.5
        self.deflector = False


class NavEntry:
    """NavEntry is the class for the data to be explored by NavARP

    Attributes:
        scans (float): scan axis of the acquisition method;
        angles (float): Angular axis of the analyzer;
        energies (float): Kinetic energy axis of the analyzer;
        data (float): The matrix composed by the detector images;
        scan_type (str): acquisition method;
        hv (float): Photon energy;
        defl_angles (float, optional): Deflector angular axis of the analyzer,
            if present;
        analyzer (NavAnalyzer class, optional): analyzer and its geometry;
        file_note (str, optional): Description of experimental condition;
        file_path (str, optional): File path, as from input.

    """

    def __init__(self, scans, angles, energies, data, scan_type, hv,
                 defl_angles=0, analyzer=NavAnalyzer(),
                 file_note="", file_path=""):
        self.scans = scans
        self.angles = angles
        self.energies = energies
        self.data = data
        self.scan_type = scan_type
        self.hv = hv
        self.defl_angles = defl_angles
        self.analyzer = analyzer
        self.file_note = file_note
        self.file_path = file_path

    def get_attr(self):
        return self.scans, self.angles, self.energies, self.data


def load(file_path):
    """The function define NavEntry from file_path.

    The function loads entry from:
        * NXarpes file from LOREA/ALBA(ES) and I05/Diamond(GB);
        * HDF5 file from SXARPES-ADRESS/PSI(CH);
        * NEXUS file from Antares/Soleil(FR);
        * folder with txt-files from Cassiopee/Soleil(FR);
        * zip- or txt-files from Scienta-Omicron SES program;
        * sp2 file from Specs program;
        * pxt file of Igor-pro as saved by Scienta-Omicron SES program;
        * yaml file with dictionary to load files (sp2 or txt Scienta) in a
          folder.
    The type of data is recognized from the file-extension:
        * *.nxs* is considered as NXarpes data if the first group is entry1
          otherwise a NEXUS file from Antares/Soleil(FR) if second group is
          ANTARES
        * *.h5* is considered for from SXARPES-ADRESS/PSI(CH);
        * *.txt* is considered as from Cassiopee/Soleil(FR) if it contains a
          line with 'Location = Cassiopee', otherwise is considered as a
          Scienta-Omicron SES program file is the first line contains '[Info]';
        * *.sp2* is considered as from Specs program;
        * *.pxt* is considered as of Igor-pro as saved by Scienta-Omicron SES
          program;
        * *.yaml* is considered as a dictionary with the complementary
          information for creating a valid NavEntry, here an example:
            file_type: '*.sp2'
            scans:
              start: 121.5
              step: 0.35
            scan_type: 'azimuth'

    Args:
        file_path (str): File path of the file to open as NavEntry.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    error_msg = (
            'Data format error.\n' +
            'Unknown file structure, the only supported data are:\n' +
            '   NXarpes file from LOREA/ALBA(ES) and I05/Diamond(GB);\n' +
            '   HDF5 file from SXARPES-ADRESS/PSI(CH);\n' +
            '   NEXUS file from Antares/Soleil(FR);\n' +
            '   folder with txt-files from Cassiopee/Soleil(FR);\n' +
            '   zip- or txt-files from Scienta-Omicron SES program;\n' +
            '   sp2 file from Specs program.'
            )

    if '.h5' in file_path:
        h5f = h5py.File(file_path, 'r', driver='core')
        return load_sxarpes_adress(h5f, file_path)

    elif '.nxs' in file_path:
        h5f = h5py.File(file_path, 'r', driver='core')
        fst_groups = list(h5f.keys())
        if 'entry1' in fst_groups:
            return load_nxarpes(h5f, file_path)

        elif 'ANTARES' in list(h5f[fst_groups[0]].keys()):
            return load_nxsantares(h5f, file_path)

        else:
            print(error_msg)

    elif '.txt' in file_path:
        # checking if file contains Location= Cassiopee
        with open(file_path) as fdat:
            line = fdat.readline()
            if '[Info]' in line:
                is_scienta_ses_txt = True
            else:
                is_scienta_ses_txt = False

            for line in fdat:
                if "Location" in line:
                    if 'cassiopee' in line.split('=')[1].lower():
                        is_cassiopee = True
                    else:
                        is_cassiopee = False
                    break
                else:
                    is_cassiopee = False

        if is_cassiopee:
            return load_cassiopee(file_path)
        elif is_scienta_ses_txt:
            return load_scienta_ses_txt(file_path)
        else:
            print(error_msg)

    elif '.zip' in file_path:
        entry = load_scienta_ses_zip(file_path)
        if entry:
            return entry
        else:
            print(error_msg)

    elif '.sp2' in file_path:
        entry = load_specs_sp2(file_path)
        if entry:
            return entry
        else:
            print(error_msg)

    elif '.pxt' in file_path:
        entry = load_igorpro_pxt(file_path)
        if entry:
            return entry
        else:
            print(error_msg)

    elif '.yaml' in file_path:
        entry = load_navarp_yaml(file_path)
        if entry:
            return entry
        else:
            print(error_msg)

    else:
        print(error_msg)


def load_sxarpes_adress(h5f, file_path):
    """Load data from SXARPES-ADRESS/PSI(CH)

    Args:
        h5f: The HDF5 file-object from h5py.File.
        h5f_matrix_path: The path location of the data (matrix).

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    # analyzer
    analyzer = NavAnalyzer()
    analyzer._set_def_sxarpes_psi()

    # deflector angles
    if not analyzer.deflector:
        defl_angles = 0

    # data
    h5f_data = h5f["/Matrix"]
    data = np.zeros(h5f_data.shape, dtype='float32')
    h5f_data.read_direct(data)

    # get wavescale and wavenote
    wavescale = h5f["/Matrix"].attrs["IGORWaveScaling"]
    wavenote = h5f["/Matrix"].attrs["IGORWaveNote"]
    wavenote = wavenote.decode("utf-8")
    try:
        waveunits = h5f["/Matrix"].attrs["IGORWaveUnits"]
    except KeyError:
        print("Attention, can't find attribute IGORWaveUnits")

    # closing h5f-file
    h5f.close()

    # angles
    angles = np.arange(
        wavescale[1][1],
        wavescale[1][1]+wavescale[1][0]*data.shape[0],
        wavescale[1][0])[0:data.shape[0]]

    # binding energies
    e_bins = np.arange(
        wavescale[2][1],
        wavescale[2][1]+wavescale[2][0]*data.shape[1],
        wavescale[2][0])[0:data.shape[1]]

    # scans and scan_type
    if len(data.shape) == 3:
        if wavescale[3][0] == 0:
            # special case where the slice are repeated
            scans = np.arange(0, data.shape[2], 1)
            scan_type = "repeated"
        else:
            scans = np.arange(
                wavescale[3][1],
                wavescale[3][1] + wavescale[3][0]*(data.shape[2]),
                wavescale[3][0])
            scan_unit = waveunits[0, 3].decode("utf-8")
            if scan_unit == 'degree':
                scan_type = "tilt"
            elif scan_unit == 'eV':
                scan_type = "hv"
            else:
                scan_type = "unknown"
                print("Error loading h5 file, unknown scan parameter")
        data = np.transpose(data, (2, 0, 1))
    elif len(data.shape) == 2:
        scans = np.array([0])
        scan_type = "single"
        data = np.tile(data, (1, 1, 1))
    else:
        print("Error loading H5 file, no 3d or 2d matrix.")

    # reading hv from wavenote
    try:
        hv_note = (wavenote[wavenote.find('=')+1:wavenote.find('\n')])
        if 'ones' in hv_note:
            # in the special case with 'ones', just replace with np.ones
            # code to be enval is similar to: 450*np.ones((1,5))
            code = (hv_note[:hv_note.find('ones')] + 'np.ones(' +
                    hv_note[hv_note.find('('):hv_note.find(')') + 1] +
                    hv_note[hv_note.find(')'):])
            hv = eval(code)
            hv = hv.ravel()
            print('Special case with ones')
            print('hv=', hv)
        else:
            hv_note = hv_note.lstrip(' [')
            hv_note = hv_note.rstrip(']')
            if ':' in hv_note:
                hv = scans
            else:
                hv_note = str.split(hv_note)
                hv = np.zeros(len(hv_note))
                for i in range(0, len(hv_note), 1):
                    hv[i] = float(hv_note[i])
        hv = hv
    except ValueError:
        hv = np.array([333])
        print("Attention, can't find photon energy (hv).")
        print("Used a default value of hv = 333 eV.")

    # get kinetic energies from e_bins, hv and work function as:
    #   e_kins = hv[:, None] - work_fun + e_bins[None, :]
    if scan_type == "hv" or scan_type == "repeated":
        energies = (hv[:, None] - analyzer.work_fun + e_bins[None, :])
    else:
        energies = hv - analyzer.work_fun + e_bins

    file_note = wavenote
    file_note = ("scan_type = {}\n".format(scan_type) + file_note)

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_nxarpes(h5f, file_path):
    """Load NXARPES data from LOREA/ALBA(ES) and I05/Diamond(GB)

    Args:
        h5f: The HDF5 file-object from h5py.File.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    # analyzer
    analyzer = NavAnalyzer()
    instrument_name = h5f["entry1/instrument/name"][()]
    print("instrument_name =", instrument_name)
    if "lorea" in instrument_name:
        analyzer._set_def_lorea_alba()
    elif "i05" in instrument_name:
        analyzer._set_def_i05_diamond()
    elif "simulated" in instrument_name:
        entry = load_nxarpes_simulated(h5f, file_path)
        return entry
    else:
        entry = load_nxarpes_generic(h5f, file_path)
        return entry

    # deflector angles
    if not analyzer.deflector:
        defl_angles = 0

    pol = h5f[("entry1/instrument/insertion_device/beam/" +
               "final_polarisation_label")][()]

    # hv and slit
    hv = h5f["entry1/instrument/monochromator/energy"][()]
    slit = h5f["entry1/instrument/monochromator/exit_slit_size"][()]
    slit = slit*1000  # from mm to microns

    mode = h5f["entry1/instrument/analyser/lens_mode"][()]
    epass = h5f["entry1/instrument/analyser/pass_energy"][()]
    t_frame = h5f["entry1/instrument/analyser/time_for_frames"][()]
    t_ch = h5f["entry1/instrument/analyser/time_per_channel"][()]

    # angles
    angles = h5f["entry1/instrument/analyser/angles"][()]

    # energies
    energies = h5f["entry1/instrument/analyser/energies"][()]

    # data
    h5f_data = h5f["entry1/instrument/analyser/data"]
    data = np.zeros(h5f_data.shape, dtype='float32')
    h5f_data.read_direct(data)

    saazimuth = h5f["entry1/instrument/manipulator/saazimuth"][()]
    sapolar = h5f["entry1/instrument/manipulator/sapolar"][()]
    satilt = h5f["entry1/instrument/manipulator/satilt"][()]

    # scans and scan_type
    if data.shape[0] == 1:
        scan_type = "single"
        scans = sapolar
    else:
        if len(sapolar) == data.shape[0]:
            scans = sapolar
            scan_type = "polar"
        elif len(satilt) == data.shape[0]:
            scans = satilt
            scan_type = "tilt"
        elif len(saazimuth) == data.shape[0]:
            scans = saazimuth
            scan_type = "azimuth"
        elif len(hv) == data.shape[0]:
            scans = hv
            scan_type = "hv"
        else:
            scans = np.arange(data.shape[0])
            scan_type = "unknown"
            print("Error loading NXS file, unknown scan parameter")

    # ################ IMPORTANT DATA MODIFICATION ########################
    # Modification of the data for the particular case of I05
    if "i05" in instrument_name:
        print("Reducing image pixels because of beamline I05 Diamond")
        angles = angles[100:-100]
        energies = energies[:-200]
        data = data[:, 100:-100, :-200]
        print('data', data.shape,
              ', angles', angles.shape,
              ', energies', energies.shape)
    # End Modification of the data for the particular case of I05
    # #####################################################################

    if len(sapolar) > 1:
        sapolar_note = '{:.2f}'.format(min(sapolar))+"\
        :"+'{:.2f}'.format(max(sapolar))+"\
        :"+'{:.2f}'.format((np.diff(sapolar)[0]))
        sapolar_note = sapolar_note.replace(" ", "")
    else:
        sapolar_note = '{:6.2f}'.format(min(sapolar))

    if len(satilt) > 1:
        satilt_note = '{:6.2f}'.format(min(satilt))+"\
        :"+'{:6.2f}'.format(max(satilt))+"\
        :"+'{:6.2f}'.format((np.diff(satilt)[0]))
        satilt_note = satilt_note.replace(" ", "")
    else:
        satilt_note = '{:6.2f}'.format(min(satilt))

    if len(saazimuth) > 1:
        saazimuth_note = '{:6.2f}'.format(min(saazimuth))+"\
        :"+'{:6.2f}'.format(max(saazimuth))+"\
        :"+'{:6.2f}'.format((np.diff(saazimuth)[0]))
    else:
        saazimuth_note = '{:6.2f}'.format(min(saazimuth))

    if len(hv) > 1:
        hv_note = '{:6.2f}'.format(min(hv))+"\
        :"+'{:6.2f}'.format(max(hv))+"\
        :"+'{:6.2f}'.format((np.diff(hv)[0]))
        hv_note = hv_note.replace(" ", "")
    else:
        hv_note = '{:6.2f}'.format(min(hv))

    file_note = "\
        sample = " + str(h5f["entry1/sample/name"][()]) + " \n\
        temperature = " + str(h5f["entry1/sample/temperature"][()]) + " \n\
        hv      = " + hv_note + " \n\
        pol     = " + str(pol) + " \n\
        slit    = " + str(slit[0]) + " \n\
        epass   = " + str(epass[0]) + " \n\
        polar   = " + sapolar_note.strip() + " \n\
        tilt    = " + satilt_note + " \n\
        azimuth = " + saazimuth_note + " \n\
        t frame = " + str(t_frame[0]) + " \n\
        t channel = " + str(min(t_ch)) + ":" + str(max(t_ch)) + "\n\
        mode    = " + str(mode) + " \n\
        "
    file_note = ("scan_type = {}\n".format(scan_type) + file_note)

    # closing h5f-file
    h5f.close()

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_nxarpes_simulated(h5f, file_path):
    """Load NXARPES example

    Args:
        h5f: The HDF5 file-object from h5py.File.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    analyzer = NavAnalyzer()
    analyzer._set_def_lorea_alba()

    # hv and slit
    hv = h5f["entry1/instrument/monochromator/energy"][()]
    if hv.shape == ():  # if scalar ndarray, def a array ndarray
        hv = np.array([hv])

    # scans
    defl_angles = h5f["entry1/instrument/analyser/defl_angles"][()]
    scans = defl_angles
    scan_type = "deflector"

    # angles
    angles = h5f["entry1/instrument/analyser/angles"][()]

    # energies
    energies = h5f["entry1/instrument/analyser/energies"][()]

    # data
    h5f_data = h5f["entry1/instrument/analyser/data"]
    data = np.zeros(h5f_data.shape, dtype='float32')
    h5f_data.read_direct(data)

    hv_note = '{:6.2f}'.format(hv[0])

    file_note = "\
        sample = " + str(h5f["entry1/sample/name"][()]) + " \n\
        temperature = " + str(h5f["entry1/sample/temperature"][()]) + " \n\
        hv      = " + hv_note + " \n\
        "
    file_note = ("scan_type = {}\n".format(scan_type) + file_note)

    # closing h5f-file
    h5f.close()

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_nxarpes_generic(h5f, file_path):
    """Load generic NXARPES as saved by save_nxarpes_generic

    Args:
        h5f: The HDF5 file-object from h5py.File.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """
    analyzer = NavAnalyzer()

    # get scan_type from experiment_description
    exp_descrip = h5f['entry1/experiment_description'][()]
    try:
        exp_descrip = exp_descrip.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    if 'scan_type' in exp_descrip:
        scan_type = exp_descrip.split('=')[1].strip()

    # get nxdata from attrs default of entry1
    nxdata = h5f['entry1'][h5f['entry1'].attrs['default']]

    # scans
    scans = nxdata["scans"][()]

    # defl_angles
    if scan_type == "deflector":
        defl_angles = scans
    else:
        defl_angles = 0

    # hv
    if scan_type == "hv":
        hv = scans
    else:
        hv = h5f["entry1/instrument/monochromator/energy"][()]
        if hv.shape == ():  # if scalar ndarray, def a array ndarray
            hv = np.array([hv])

    # angles
    angles = nxdata["angles"][()]

    # energies
    energies = nxdata["energies"][()]

    # data
    h5f_data = nxdata["data"]
    data = np.zeros(h5f_data.shape, dtype='float32')
    h5f_data.read_direct(data)

    hv_note = '{:6.2f}'.format(hv[0])
    file_note = ("hv      = " + hv_note + " \n")
    file_note = ("scan_type = {}\n".format(scan_type) + file_note)

    # closing h5f-file
    h5f.close()

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_nxsantares(h5f, file_path):
    """Load NEXUS file from Antares/Soleil(FR)

    Args:
        h5f: The HDF5 file-object from h5py.File.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    # analyzer
    analyzer = NavAnalyzer()
    analyzer._set_def_antares_soleil()

    fst_grp = list(h5f.keys())[0]

    # deflector angles
    if not analyzer.deflector:
        defl_angles = 0
    else:
        defl_angles = h5f[fst_grp+"/scan_data/actuator_1_1"][()]

    # scans and scan_type
    scans = defl_angles
    scan_type = "deflector"

    hv = h5f[fst_grp+"/ANTARES/Monochromator/energy/data"][()]
    en_res = h5f[fst_grp+"/ANTARES/Monochromator/resolution/data"][()]

    mbs_grp = [key for key in h5f[fst_grp+"/ANTARES"] if "MBSAcq" in key][0]
    mode = h5f[fst_grp+"/ANTARES/"+mbs_grp+"/LensMode/data"][()]
    epass = h5f[fst_grp+"/ANTARES/"+mbs_grp+"/PASSENERGY/data"][()]
    mode = mode.decode("utf-8")
    epass = epass.decode("utf-8")

    angle_min = h5f[fst_grp+"/scan_data/data_04"][()][0]
    angle_mult = h5f[fst_grp+"/scan_data/data_05"][()][0]
    angle_max = h5f[fst_grp+"/scan_data/data_06"][()][0]
    # angle array includes the angle_max so
    angles = np.arange(angle_min,
                       angle_max+angle_mult*0.5,
                       angle_mult)

    energy_min = h5f[fst_grp+"/scan_data/data_01"][()][0]
    energy_mult = h5f[fst_grp+"/scan_data/data_02"][()][0]
    energy_max = h5f[fst_grp+"/scan_data/data_03"][()][0]
    # energies array includes the energies_max so
    energies = np.arange(energy_min,
                         energy_max+energy_mult*0.5,
                         energy_mult)

    h5f_data = h5f[fst_grp+"/scan_data/data_09"]
    data = np.zeros(h5f_data.shape, dtype='float32')
    h5f_data.read_direct(data)

    # Modification of the data
    #   filtering spikes on data
    filter_mask = (data > data.max()*0.5)
    n_filter_mask = np.sum(filter_mask)
    n_scans = scans.shape[0]
    if n_filter_mask < n_scans*4:
        print("{0:} points (over {1:} ".format(n_filter_mask, n_scans) +
              "scans) set to zeros, because interepreted as spikes.")
        data[filter_mask] = 0
    # End Modification

    if len(hv) > 1:
        hv_note = '{:6.2f}'.format(min(hv))+"\
        :"+'{:6.2f}'.format(max(hv))+"\
        :"+'{:6.2f}'.format((np.diff(hv)[0]))
        hv_note = hv_note.replace(" ", "")
    else:
        hv_note = '{:6.2f}'.format(min(hv))

    file_note = "\
                sample = " + fst_grp + " \n\
                hv      = " + hv_note + " \n\
                en_res  = " + str(en_res[0]) + " \n\
                epass   = " + epass + " \n\
                mode    = " + mode + " \n\
                deflector   = scan along tilt \n\
                "
    file_note = ("scan_type = {}\n".format(scan_type) + file_note)

    # closing h5f-file
    h5f.close()

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_cassiopee(file_path):
    """Load ARPES data from Cassiopee/Soleil(FR)

    Args:
        path: file path of a ROI-file in the folder.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    # analyzer
    analyzer = NavAnalyzer()
    analyzer._set_def_cassiopee_soleil()

    # deflector angles
    if not analyzer.deflector:
        defl_angles = 0

    if 'ROI1' in file_path:
        file_dir = os.path.abspath(os.path.dirname(file_path))

        info_file_dir = os.path.join(file_dir, 'info_files')
        if not os.path.isdir(info_file_dir):
            info_file_dir = file_dir

        file_ROIs = os.path.join(file_dir, '*_ROI1_*.txt')
        file_paths = glob.glob(file_ROIs)
        file_paths = sorted(file_paths, key=lambda file_path: int(
                re.search("[0-9]*_ROI1", file_path).group().split("_")[0]))

        hv = np.genfromtxt(file_paths[0], skip_header=15,
                           max_rows=1, usecols=2)[None]

        entry = np.genfromtxt(file_paths[0], skip_header=44)
        data = np.zeros((len(file_paths), entry.shape[1]-1, entry.shape[0]))
        e_kin = np.zeros((len(file_paths), entry.shape[0]))
        angles = np.zeros((len(file_paths), entry.shape[1]-1))
        params = {}
        pol_dict = {"0": "LV", "1": "LH", "2": "AV", "3": "AH", "4": "CR"}

        for i, file_path in enumerate(file_paths):
            entry = np.genfromtxt(file_path, skip_header=44)

            data[i, :, :] = np.transpose(entry[:, 1:])
            e_kin[i, :] = entry[:, 0]
            angles[i, :] = np.genfromtxt(file_path, skip_header=11, max_rows=1,
                                         usecols=range(3, data.shape[1]+3))

            file_name = os.path.basename(file_path)
            info_file_name= (file_name[:re.search("ROI", file_name).start()] +
                             "i.txt")

            info_file = os.path.join(info_file_dir, info_file_name)

            with open(info_file) as fdat:
                for line in fdat:
                    if "SAMPLE" in line:
                        for line in fdat:
                            line_split = line.split(" :")
                            if len(line_split) < 2:
                                break
                            if i == 0:
                                params[line_split[0]] = [line_split[1]]
                            else:
                                params[line_split[0]].append(line_split[1])

                    if "MONOCHROMATOR" in line:
                        for line in fdat:
                            line_split = line.split(" :")
                            if len(line_split) < 2:
                                break
                            if i == 0:
                                params[line_split[0]] = [line_split[1]]
                            else:
                                params[line_split[0]].append(line_split[1])

                    if "Polarisation [0:LV, 1:LH, 2:AV, 3:AH, 4:CR]" in line:
                        if i == 0:
                            params["Polarisation"] = [pol_dict[line[-2]]]
                        else:
                            params["Polarisation"].append(pol_dict[line[-2]])
                        break

        # WARNING: it should be checked if angles is the same in each scan-step
        angles = np.copy(angles[0, :])

        file_note = ""
        for key in params:
            try:
                params[key] = np.array(params[key]).astype(float)
                x0 = params[key][0]
                change_flag = not(all(abs((x-x0)/x) < 0.001
                                      for x in params[key]))
                if change_flag:
                    if 'theta (deg)' in key:
                        scan_type = "polar"
                        scans = np.array(params[key])
                        energies = np.copy(e_kin[0, :])
                    elif 'phi (deg)' in key:
                        scan_type = "azimuth"
                        scans = np.array(params[key])
                        energies = np.copy(e_kin[0, :])
                    elif 'hv (eV)' in key:
                        scan_type = "hv"
                        scans = np.array(params[key])
                        hv = scans
                        energies = np.copy(e_kin)

                    file_note += "{} = [{}:{:1g}:{}]\n".format(
                            key, params[key][0], params[key][1]-params[key][0],
                            params[key][-1])
                else:
                    file_note += "{} = {}\n".format(key, params[key][0])
            except ValueError:
                params[key] = np.array(params[key])
                file_note += "{} = {}".format(key, params[key][0])
        file_note = ("scan_type = {}\n".format(scan_type) + file_note)

        return NavEntry(
            scans, angles, energies, data, scan_type, hv, defl_angles,
            analyzer, file_note, file_path)
    else:
        return load_scienta_ses_txt(file_path)


def load_scienta_ses_zip(file_path):
    """Load zip-file from Scienta-Omicro SES program.

    Args:
        path: file path of the zip-file.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """

    # analyzer
    analyzer = NavAnalyzer(tht_ap=50, phi_ap=0, work_fun=4.5, deflector=True)

    # Load the zip file
    entry_zip = np.load(file_path)

    # find Region Name
    pattern = "Spectrum_(.*?).ini"
    spectrum_found = False
    for key in entry_zip:
        re_match = re.match(pattern, key)
        if re_match:
            region_name = re_match.group(1)
            spectrum_found = True

    # if no "Spectrum_(.*?).ini" is in the zip-file, exit without entry
    if not spectrum_found:
        return None

    # extract meta data from '{}.ini'.format(region_name)
    key_region_name = '{}.ini'.format(region_name)
    strings = entry_zip[key_region_name].decode("utf-8").split('\r\n')
    params = {}
    for string in strings:
        if '=' in string:
            string_split = string.split('=')
            params[string_split[0]] = string_split[1]
    hv = np.array([float(params['Excitation Energy'].replace(',', '.'))])

    # extract meta data from 'Spectrum_{}.ini'.format(region_name)
    key_sp = 'Spectrum_{}.ini'.format(region_name)
    strings = entry_zip[key_sp].decode("utf-8").split('\r\n')
    par_sp = {}
    for string in strings:
        if '=' in string:
            string_split = string.split('=')
            try:
                par_val = float(string_split[1].replace(',', '.'))
            except ValueError:
                par_val = string_split[1]
            par_sp[string_split[0]] = par_val

    angles = np.arange(
        par_sp['heightoffset'],
        par_sp['heightoffset']+par_sp['height']*par_sp['heightdelta'],
        par_sp['heightdelta']
    )

    energies = np.arange(
        par_sp['widthoffset'],
        par_sp['widthoffset']+par_sp['width']*par_sp['widthdelta'],
        par_sp['widthdelta']
    )

    defl_angles = np.arange(
        par_sp['depthoffset'],
        par_sp['depthoffset']+par_sp['depth']*par_sp['depthdelta'],
        par_sp['depthdelta']
    )

    scans = defl_angles
    scan_type = 'deflector'

    # extract data from 'Spectrum_{}.bin'.format(region_name)
    key_data = 'Spectrum_{}.bin'.format(region_name)
    data_unshaped = np.frombuffer(entry_zip[key_data], dtype=np.uint32)
    data = data_unshaped.reshape(
        (len(scans), len(angles), len(energies))).astype(np.float32)

    file_note = "scan_type = {}\n".format(scan_type)
    for key in params:
        file_note += "{} = {}\n".format(key, params[key])

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_scienta_ses_txt(file_path):
    """Load txt-file from Scienta-Omicro SES program.

    Args:
        path: file path of the txt-file.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """
    # analyzer
    analyzer = NavAnalyzer(tht_ap=50, phi_ap=0, work_fun=4.5, deflector=False)

    # Load the txt-file
    params = {}
    with open(file_path) as fdat:
        for line in fdat:
            if '=' in line:
                string_split = line.replace('\n', '').split('=')
                params[string_split[0]] = string_split[1]
            elif "[Data 1]" in line:
                entry = np.genfromtxt(fdat)
                data = entry[:, 1:]
                e_kin = entry[:, 0]
                break

    scans = np.array([1])
    angles = np.array(
        params["Dimension 2 scale"].replace(',', '.').split()).astype(np.float)
    energies = e_kin
    data = np.tile(np.transpose(data), (1, 1, 1))

    scan_type = 'single'

    hv = np.array([float(params['Excitation Energy'].replace(',', '.'))])

    defl_angles = 0

    file_note = "scan_type = {}\n".format(scan_type)
    for key in params:
        if "Dimension " not in key:
            file_note += "{} = {}\n".format(key, params[key])

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_specs_sp2(file_path):
    """Load sp2-file from Specs program.

    Args:
        path: file path of the sp2-file.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """
    # analyzer
    analyzer = NavAnalyzer(tht_ap=50, phi_ap=0, work_fun=4.5, deflector=False)

    # Load the sp2-file
    params = {}
    with open(file_path) as fdat:
        for line in fdat:
            if line[0] == '#':  # check if header started
                break

        for line in fdat:
            if line[0] != '#':  # check if header ended
                break
            elif '=' in line:
                string_split = line[2:].replace('\n', '').split('=')
                params[string_split[0].strip()] = string_split[1][1:]

        data_shape = np.fromstring(line, dtype=int, sep=' ')
        pts_num = data_shape[0]*data_shape[1]
        data = np.genfromtxt(fdat, max_rows=pts_num).reshape(
            (data_shape[1], data_shape[0]))

    scans = np.array([1])
    angles_range = np.fromstring(
        params["aRange"].split('#')[0], dtype=float, sep=' ')
    angles = np.linspace(angles_range[0], angles_range[1], data_shape[1])
    energies_range = np.fromstring(
        params["ERange"].split('#')[0], dtype=float, sep=' ')
    energies = np.linspace(energies_range[0], energies_range[1], data_shape[0])

    data = np.tile(data, (1, 1, 1))

    scan_type = 'single'

    hv = np.array([123])

    defl_angles = 0

    file_note = "scan_type = {}\n".format(scan_type)
    for key in params:
        if "Dimension " not in key:
            file_note += "{} = {}\n".format(key, params[key])

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_igorpro_pxt(file_path):
    """Load pxt-file of Igor-pro as saved from Scienta-Omicro SES program.

    Args:
        path: file path of the pxt-file.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """
    # analyzer
    analyzer = NavAnalyzer(tht_ap=50, phi_ap=0, work_fun=4.5, deflector=False)

    # Load the pxt-file
    pxt_file = igor.load(file_path)
    pxt_file_folder = pxt_file.children[0]

    angle_min = pxt_file_folder.axis[1][-1]
    angle_step = pxt_file_folder.axis[1][0]
    angle_len = pxt_file_folder.axis[1].shape[0]
    angle_max = angle_min+(angle_len)*angle_step
    angles = np.arange(angle_min, angle_max, angle_step)

    energy_min = pxt_file_folder.axis[0][-1]
    energy_step = pxt_file_folder.axis[0][0]
    energy_len = pxt_file_folder.axis[0].shape[0]
    energy_max = energy_min+(energy_len)*energy_step
    energies = np.arange(energy_min, energy_max, energy_step)

    data = np.transpose(pxt_file_folder.data)

    data = np.tile(data, (1, 1, 1))

    # extract meta data from '{}.ini'.format(region_name)
    strings = pxt_file_folder.notes.decode("utf-8").split('\r')
    params = {}
    for string in strings:
        if '=' in string:
            string_split = string.split('=')
            params[string_split[0]] = string_split[1]
    hv = np.array([float(params['Excitation Energy'].replace(',', '.'))])

    scans = np.array([1])

    scan_type = 'single'

    defl_angles = 0

    file_note = "scan_type = {}\n".format(scan_type)
    for key in params:
        if "Dimension " not in key:
            file_note += "{} = {}\n".format(key, params[key])

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def load_navarp_yaml(file_path):
    """Load files in a folder using yaml-file.

    Args:
        path: file path of the yaml-file.

    Returns:
        NavEntry (class): the class for the data to be explored by NavARP.
    """
    with open(file_path) as file_info:
        entry_info = yaml.safe_load(file_info)

    # Load data from each file
    file_yaml_dir = os.path.dirname(file_path)
    file_data_path = os.path.normpath(
        os.path.join(file_yaml_dir, entry_info['file_type']))

    file_data_dir = os.path.abspath(os.path.dirname(file_data_path))
    file_list = os.listdir(file_data_dir)

    file_type = os.path.basename(file_data_path).replace('*', '(.*?)')
    file_names = [fname for fname in file_list if re.search(file_type, fname)]
    file_names = sorted(
        file_names,
        key=lambda file_name: int(re.match(file_type, file_name).group(1)))

    file_paths = [os.path.join(file_data_dir, fname) for fname in file_names]

    if os.path.splitext(file_type)[1] == '.sp2':
        file_loader = load_specs_sp2
    elif os.path.splitext(file_type)[1] == '.txt':
        with open(file_path) as fdat:
            line = fdat.readline()
            if '[Info]' in line:
                file_loader = load_scienta_ses_txt
    elif os.path.splitext(file_type)[1] == '.pxt':
        file_loader = load_igorpro_pxt
    else:
        return None

    data = None
    for i, file_path in enumerate(file_paths):
        entry_i = file_loader(file_path)
        if data is not None:
            data[i, :, :] = entry_i.data
        else:
            data_0 = entry_i.data
            data = np.zeros(
                (len(file_paths), data_0.shape[1], data_0.shape[2]))

    # scans from yaml-file
    scans_info = entry_info['scans']
    if 'step' in scans_info:
        scans = np.arange(
            scans_info['start'],
            scans_info['start'] + (len(file_paths) - 0.5)*scans_info['step'],
            scans_info['step']
        )
    elif 'stop' in scans_info:
        scans = np.linspace(
            scans_info['start'], scans_info['stop'], len(file_paths))

    angles = entry_i.angles
    energies = entry_i.energies

    # scan type from yaml-file
    scan_type = entry_info['scan_type']

    # photon energy from yaml-file if present
    if 'hv' in entry_info:
        hv = np.array([entry_info['hv']])
    else:
        hv = entry_i.hv

    # analyzer from yaml-file if present
    if 'analyzer' in entry_info:
        analyzer_info = entry_info['analyzer']

        if 'tht_ap' in analyzer_info:
            tht_ap = analyzer_info['tht_ap']
        else:
            tht_ap = 50

        if 'phi_ap' in analyzer_info:
            phi_ap = analyzer_info['phi_ap']
        else:
            phi_ap = 0

        if 'work_fun' in analyzer_info:
            work_fun = analyzer_info['work_fun']
        else:
            work_fun = 4.5

        if 'deflector' in analyzer_info:
            deflector = analyzer_info['deflector']
        else:
            deflector = False

        analyzer = NavAnalyzer(tht_ap, phi_ap, work_fun, deflector)
    else:
        analyzer = NavAnalyzer(
            tht_ap=50, phi_ap=0, work_fun=4.5, deflector=False)

    if scan_type == 'deflector':
        defl_angles = scans
    else:
        defl_angles = 0

    file_note = entry_i.file_note

    return NavEntry(scans, angles, energies, data, scan_type, hv, defl_angles,
                    analyzer, file_note, file_path)


def save_nxarpes_generic(entry, file_path_nxs, instrument_name=r"unknow"):
    """The function saves NavEntry into file_path as generic NXARPES.

    Args:
        entry (NavEntry class): entry to be saved.
        file_path_nxs (str): File path for the nxs-file to be saved.
        instrument_name (string, optional): name of the instrument where the
            data are from (e.g.: beamline or laboratory name).
    """

    f = h5py.File(file_path_nxs, "w")  # create the HDF5 NeXus file
    f.attrs[u"default"] = u"entry1"

    nxentry = f.create_group(u"entry1")
    nxentry.attrs[u"NX_class"] = u"NXentry"
    nxentry.attrs[u"default"] = u"data"
    nxentry.create_dataset(u"definition", data=b"NXarpes")
    nxentry.create_dataset(u"experiment_description",
                           data="scan_type = {}".format(entry.scan_type))

    # instrument --------------------------------------------------------------
    nxinstrument = nxentry.create_group(u"instrument")
    nxinstrument.attrs[u"NX_class"] = u"NXinstrument"
    nxinstrument.create_dataset(u"name", data=instrument_name)

    # instrument/analyser -----------------------------------------------------
    nxdetector = nxinstrument.create_group(u"analyser")
    nxdetector.attrs[u"NX_class"] = u"NXdetector"

    # store the data in the NXdetector group
    angles_nx = nxdetector.create_dataset(u"angles", data=entry.angles)
    angles_nx.attrs[u"units"] = u"degrees"
    angles_nx.attrs[u"axis"] = 2
    angles_nx.attrs[u"primary"] = 1

    energies_nx = nxdetector.create_dataset(u"energies", data=entry.energies)
    energies_nx.attrs[u"units"] = u"eV"
    energies_nx.attrs[u"axis"] = 3
    energies_nx.attrs[u"primary"] = 1

    data_nx = nxdetector.create_dataset(u"data",
                                        data=entry.data,
                                        compression='gzip',
                                        chunks=(5, entry.angles.shape[0], 50))
    data_nx.attrs[u"units"] = u"counts"

    # instrument/monochromator ------------------------------------------------
    nxinstrument.create_group(u"monochromator")
    nxinstrument[u"monochromator"].attrs[u"NX_class"] = u"NXmonochromator"
    nxinstrument[u"monochromator"].create_dataset(u"energy",
                                                  data=entry.hv)
    nxinstrument[u"monochromator/energy"].attrs[u"units"] = u"eV"

    # data --------------------------------------------------------------------
    # data: create the NXdata group to define the default plot
    nxdata = nxentry.create_group(u"data")
    nxdata.attrs[u"NX_class"] = u"NXdata"
    nxdata.attrs[u"signal"] = u"data"
    nxdata.attrs[u"axes"] = [u"scans", u"angles", u"energies"]

    # store generic scans
    scans_nx = nxdata.create_dataset(u"scans", data=entry.scans)
    scans_nx.attrs[u"units"] = u"degrees"
    scans_nx.attrs[u"axis"] = 1
    scans_nx.attrs[u"primary"] = 1

    ## Create link in NXdata
    source_addr = u"/entry1/instrument/analyser/angles"  # existing data
    target_addr = u"/entry1/data/angles"                 # new location
    angles_nx.attrs[u"target"] = source_addr  # NeXus API convention for links
    f[target_addr] = f[source_addr]           # hard link
    # nxdata._id.link(source_addr, target_addr, h5py.h5g.LINK_HARD)

    source_addr = u"/entry1/instrument/analyser/energies"   # existing data
    target_addr = u"/entry1/data/energies"                  # new location
    energies_nx.attrs[u"target"] = source_addr  # NeXus API convention for link
    f[target_addr] = f[source_addr]             # hard link
    # # nxdata._id.link(source_addr, target_addr, h5py.h5g.LINK_HARD)

    source_addr = u"/entry1/instrument/analyser/data"  # existing data
    target_addr = u"/entry1/data/data"                 # new location
    data_nx.attrs[u"target"] = source_addr    # NeXus API convention for links
    f[target_addr] = f[source_addr]           # hard link
    # nxdata._id.link(source_addr, target_addr, h5py.h5g.LINK_HARD)

    f.close()   # be CERTAIN to close the file
    print("Saved file as: \n\t{}".format(file_path_nxs))
