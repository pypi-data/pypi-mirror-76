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

"""This module is part of the Python NavARP library. It defines the functions
for extracting the Fermi level energy."""

__author__ = ["Federico Bisti"]
__license__ = "GPL"
__date__ = "31/03/2017"

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import argrelmin

from lmfit.models import LinearModel, StepModel

import matplotlib.pyplot as plt


def dlog_fit(energies, data, energy_range=None, fit_step=[20, 30],
             plt_out=False, print_out=False):
    """Find fermi level using logaritmic derivative and then fit

    Args:
        energies (ndarray): Energy axis of the analyzer data;
        data (ndarray): The matrix composed by the detector images;
        energy_range (ndarray): Energy range where to find fermi level
            [min, max];
        fit_step ((ndarray, dtype=int), optional): Number of steps, before and
            after the fermi level edge obtained with the logaritmic derivative,
            where to do the fit;
        plt_out (boolean, optional): If True, plot the result of the fermi
            level detection;
        print_out (boolean, optional): If True, print the result of the fermi
            level detection.
    Returns:
        (tuple):
            * **efermi** (float): The fermi level value;
            * **fwhm** (float): The FWHM of the Fermi level obtained
              considering the fermi edge as a step function convoluted with a
              gaussian. The relations between sigma of the logistic function
              (stp_sigma), sigma of the gaussian function (gauss_sigma), and
              FWHM are:

                + gauss_sigma = 1.70*stp_sigma;
                + FWHM = 4.00*stp_sigma;
                + FWHM = 2.355*gauss_sigma.

    """

    if not(np.convolve(energies[3:-3], [1, -2, 1], 'same') /
           (energies[3:-3]*(1+1e-15)) < 1e-10).all():
        print('Energy scale not uniform')

    # check energies axis and list the other ones
    axis_to_sum = np.delete(np.arange(len(data.shape)),
                            np.where(np.array(data.shape) == energies.shape))
    # making the sum over the other axes
    data_s = np.sum(data, axis=tuple(axis_to_sum))

    # first derivative
    denergies = gaussian_filter1d(energies, 10, order=1)
    ddata_s = gaussian_filter1d(data_s, 10, order=1)
    ddata_s_denergies = ddata_s/denergies

    # first logaritmic derivative
    ddata_s_denergies = ddata_s_denergies/np.abs(data_s)

    if energy_range is None:
        crit_i = None
        cicle = 0
        p_min = 0.1
        p_max = 0.95
        range_i = [0, 1]
        efermi = max(energies[range_i])
        while (efermi == max(energies[range_i])) or (cicle < 3):
            p_min = p_min + 0.05
            p_max = p_max - 0.05
            range_i = np.where(
                (energies > (p_min*max(energies) + (1-p_min)*min(energies))) &
                (energies < (p_max*max(energies) + (1-p_max)*min(energies))))
            crit_i = np.argmin(ddata_s_denergies[range_i])
            cicle = cicle + 1
            efermi = energies[range_i][crit_i]
    else:
        # the only criterium is to be inside the energy range
        range_i = np.where((energies >= min(energy_range)) &
                           (energies <= max(energy_range)))
        crit_i = np.argmin(ddata_s_denergies[range_i])

    efermi = energies[range_i][crit_i]
    mean_de = np.abs(np.mean(denergies))
    # fit
    if energy_range is None:
        range_fit, = np.where((energies < efermi+mean_de*fit_step[1]) &
                              (energies >= efermi-mean_de*fit_step[0]))
    else:
        # the only criterium is to be inside the energy range
        range_fit = range_i

    stp = StepModel(form='logistic', prefix='stp_')
    bkg = LinearModel(prefix='bkg_')
    fmodel = stp + bkg

    amplitude = -(max(data_s[range_fit]) - min(data_s[range_fit]))
    pars = fmodel.make_params()
    pars['stp_sigma'].set(0.1, min=0.0001)
    pars['stp_center'].set(efermi-0.1)
    pars['stp_amplitude'].set(amplitude)  # , min=amplitude*0.5)
    pars['bkg_slope'].set(0.0001)
    pars['bkg_intercept'].set(min(data_s[range_fit])-amplitude)

    out = fmodel.fit(data_s[range_fit], pars, x=energies[range_fit])

    efermi = out.best_values['stp_center']
    sigma = out.best_values['stp_sigma']
    fwhm = sigma*4

    if plt_out:
        fig, axfit = plt.subplots(2, sharex=True)
        axfit[0].plot(energies[range_i], data_s[range_i])
        axfit[1].plot(energies[range_i], ddata_s_denergies[range_i])

        axfit[0].axvline(efermi, linewidth=1, color='y')
        axfit[1].plot(energies[range_i][crit_i],
                      ddata_s_denergies[range_i][crit_i], 'yo')

        axfit[0].plot(energies[range_fit], out.best_fit, 'r-')

    if print_out:
        print('Efermi = {0:0.3f} eV'.format(efermi))
        print('Sigma(step, gauss) = ({0:0.2e}, {1:0.2e}) eV'.format(
            sigma, 1.70*sigma))
        print('FWHM = {0:0.2f} meV'.format(fwhm*1000))
    return efermi, fwhm


def dlog_fit_each(scans, energies, data,
                  energy_range=None, fit_step=[20, 30],
                  plt_out=False, print_out=False):
    """Find fermi level dlog_fit for each detector image along the scans

    Args:
        energies (ndarray): Energy axis of the analyzer data;
        scans (ndarray): Scan axis of the data acquisition;
        data (ndarray): The matrix composed by the detector images, the matrix
            must be ordered as data[scans, angles, energies];
        data0 (ndarray): The matrix composed by the detector images, the matrix
            must be ordered as data[scans, angles, energies];
        energy_range (ndarray): Energy range where to find fermi level
            [min, max];
        fit_step ((ndarray, dtype=int), optional): Number of steps, before and
            after the fermi level edge obtained with the logaritmic derivative,
            where to do the fit;
        plt_out (boolean, optional): If True, plot the result of the fermi
            level detection;
        print_out (boolean, optional): If True, print the result of the fermi
            level detection.
    Returns:
        (tuple):
            * **efermis** (ndarray): The fermi level values for each detector
              image;
            * **fwhms** (ndarray): Each FWHM of the fermi level obtained
              considering the fermi edge as a step function convoluted with a
              gaussian. The relations between sigma of the logistic function
              (stp_sigma), sigma of the gaussian function (gauss_sigma), and
              FWHM are:

                + gauss_sigma = 1.70*stp_sigma;
                + FWHM = 4.00*stp_sigma;
                + FWHM = 2.355*gauss_sigma.

    """

    scans_ax = np.argmin(abs(np.array(data.shape) - scans.shape))
    if len(energies.shape) == 2:
        energies_ax = np.argmin(abs(np.array(data.shape) - energies.shape[1]))
    elif len(energies.shape) == 1:
        energies_ax = np.argmin(abs(np.array(data.shape) - energies.shape))

    if scans_ax == 0 and energies_ax == 2:
        efermis = np.zeros(scans.shape[0])
        fwhms = np.zeros(scans.shape[0])
        for i in range(scans.shape[0]):
            if len(energies.shape) == 2:
                energies_i = energies[i, :]
                if energy_range is not None:
                    energy_range_i = energy_range[i, :]
                else:
                    energy_range_i = energy_range
            elif len(energies.shape) == 1:
                energies_i = energies
                energy_range_i = energy_range

            efermis[i], fwhms[i] = dlog_fit(
                        energies_i, data[i, :, :], energy_range_i, fit_step,
                        plt_out, print_out)
        return efermis, fwhms
    else:
        print("Error: data not ordered as data[scans, angles, energies]")
        return None, None


def align_to_same_eb(efermis, energies, data):
    """ Align each detector image to the same binding energy axis from efermis.

    Args:
        efermis (float): The fermi level values for each detector image;
        energies (ndarray): Energy axis of the analyzer data;
        data (ndarray): The matrix composed by the detector images, the matrix
            must be ordered as data[scans, angles, energies];
    Returns:
        (tuple):
            * **e_bins** (ndarray): Unified binding energy axis;
            * **energies_algn** (ndarray): Each kinetic energy axis aligned to
              e_bins;
            * **data_algn** (ndarray): Each detector image are aligned to
              e_bins.
    """
    e_bins_all = energies - efermis[:, None]
    e_bins_means = e_bins_all.mean(axis=1)
    i_en_algn = np.argmin(abs(e_bins_means - e_bins_means.mean()))
    e_bins = e_bins_all[i_en_algn, :]

    half_len = int(energies.shape[1]*0.5)
    en_ref = e_bins[half_len]
    i_ref = half_len

    data_algn = np.copy(data)
    energies_algn = np.copy(energies)

    delta_i_min = 0
    delta_i_max = 0

    for i in range(energies.shape[0]):
        delta_i = (np.argmin(abs(en_ref-e_bins_all[i, :])) - i_ref)
        if delta_i > 0:
            data_algn[i, :, :-delta_i] = data_algn[i, :, delta_i:]
            energies_algn[i, :-delta_i] = energies_algn[i, delta_i:]
            if delta_i > delta_i_max:
                delta_i_max = delta_i
        elif delta_i < 0:
            data_algn[i, :, -delta_i:] = data_algn[i, :, :delta_i]
            energies_algn[i, -delta_i:] = energies_algn[i, :delta_i]
            if delta_i < delta_i_min:
                delta_i_min = delta_i

    # reduce the size to eliminate border
    delta_i_min = delta_i_min - 1
    e_bins = e_bins[delta_i_max:delta_i_min]
    energies_algn = energies_algn[:, delta_i_max:delta_i_min]
    data_algn = data_algn[:, :, delta_i_max:delta_i_min]

    return e_bins, energies_algn, data_algn


def align_fermi_index(efermis, energies, data):
    """ Align each detector image to the fermi level.

    Args:
        energies (ndarray): Energy axis of the analyzer data;
        scans (ndarray): Scan axis of the data acquisition;
        data0 (ndarray): The matrix composed by the detector images, the matrix
            must be ordered as data[scans, angles, energies];
    Returns:
        (tuple):
            * **energies_algn** (ndarray): Unified energy axis for data;
            * **data_algn** (ndarray): Each detector image aligned to the same
              fermi level.
    """

    efermi = efermis.mean()
    i_ef_0 = np.argmin(abs(energies - efermi))
    data_algn = np.copy(data)

    for i in range(data_algn.shape[0]):
        delta_i_ef = (np.argmin(abs(efermis[i]-energies)) - i_ef_0)
        if delta_i_ef > 0:
            data_algn[i, :, :-delta_i_ef] = data_algn[i, :, delta_i_ef:]
        elif delta_i_ef < 0:
            data_algn[i, :, -delta_i_ef:] = data_algn[i, :, :delta_i_ef]
    return data_algn, efermi


def dlog(energies, data, energy_range=None, plt_out=False):
    """Find fermi level using logaritmic derivative

    Args:
        energies (ndarray): Energy axis of the analyzer data;
        data (ndarray): The matrix composed by the detector images;
        energy_range (ndarray): Energy range where to find fermi level
            [min, max];
        plt_out (boolean, optional): If True, plot the result of the fermi
            level detection;
    Returns:
        (float): The fermi level value
    """
    if not(np.convolve(energies[3:-3], [1, -2, 1], 'same') /
           (energies[3:-3]*(1+1e-15)) < 1e-10).all():
        print('Energy scale not uniform')

    # check energies axis and list the other ones
    axis_to_sum = np.delete(np.arange(len(data.shape)),
                            np.where(np.array(data.shape) == energies.shape))
    # making the sum over the other axes
    data_s = np.sum(data, axis=tuple(axis_to_sum)).astype(float)

    # first derivative
    denergies = gaussian_filter1d(energies, 10, order=1)
    ddata_s = gaussian_filter1d(data_s, 10, order=1)
    ddata_s_denergies = ddata_s/denergies

    # first logaritmic derivative
    ddata_s_denergies = ddata_s_denergies/np.abs(data_s)

    if energy_range is None:
        crit_i = None
        cicle = 0
        p_min = 0.1
        p_max = 0.95
        range_i = [0, 1]
        efermi = max(energies[range_i])
        while (efermi == max(energies[range_i])) or (cicle < 3):
            p_min = p_min + 0.05
            p_max = p_max - 0.05
            range_i = np.where(
                (energies > (p_min*max(energies) + (1-p_min)*min(energies))) &
                (energies < (p_max*max(energies) + (1-p_max)*min(energies))))
            crit_i = np.argmin(ddata_s_denergies[range_i])
            cicle = cicle + 1
            efermi = energies[range_i][crit_i]
    else:
        # the only criterium is to be inside the energy range
        range_i = np.where((energies >= min(energy_range)) &
                           (energies <= max(energy_range)))
        crit_i = np.argmin(ddata_s_denergies[range_i])

    efermi = energies[range_i][crit_i]

    if plt_out:
        fig, axfit = plt.subplots(2, sharex=True)
        axfit[0].plot(energies[range_i], data_s[range_i])
        axfit[1].plot(energies[range_i], ddata_s_denergies[range_i])

        axfit[0].plot(efermi, data_s[range_i][crit_i], 'o')
        axfit[1].plot(efermi, ddata_s_denergies[range_i][crit_i], 'o')

        axfit[0].plot(energies-efermi, data_s)

    return efermi


def dderiv(energies, data, energy_range=None, print_out=False):
    """Find fermi level using first derivative and intensity criteria

    Args:
        energies (ndarray): Energy axis of the analyzer data;
        data (ndarray): The matrix composed by the detector images;
        energy_range (ndarray): Energy range where to find fermi level
            [min, max];
        plt_out (boolean, optional): If True, plot the result of the fermi
            level detection;
    Returns:
        (float): The fermi level value
    """
    if not(np.convolve(energies[3:-3], [1, -2, 1], 'same') /
           (energies[3:-3]*(1+1e-15)) < 1e-10).all():
        print('Energy scale not uniform')

    # check energy axis and list the other ones
    axis_to_sum = np.delete(np.arange(len(data.shape)),
                            np.where(np.array(data.shape) == energies.shape))
    # making the sum over the other axes
    data_s = np.sum(data, axis=tuple(axis_to_sum)).astype(float)

    # first derivative
    denergies = gaussian_filter1d(energies, 10, order=1)
    ddata_s = gaussian_filter1d(data_s, 10, order=1)
    ddata_s_denergies = ddata_s/denergies

    # find local minimums
    lm_i = argrelmin(ddata_s_denergies, axis=0, order=1, mode='clip')

    if energy_range is None:
        # filtering the local minimums by 2 criteria:
        # 1- intensity higher than 1% over the background, at Ek > hv-W0
        # 2- first derivative higher than 1.5 times of coefficient of a line
        #      from (min(energies), max(M_int)) to (max(energies), min(M_int))

        # instead of taking the absolute min value of M_int, it is taken
        # the mean value of the points with higher energy
        # the range is for energy higher than 85% of the highest energy
        perc = 0.85
        ebkg_i = np.where(energies > (perc*max(energies) +
                                      (1-perc)*min(energies)))
        data_s_min = np.mean(data_s[ebkg_i])
        data_s_max = max(data_s)

        # coefficient line
        coeff_line = 1.5*(data_s_min-data_s_max)/(max(energies)-min(energies))

        # here the two criteria
        crit_i = np.where(
            ((data_s[lm_i]-data_s_min) > (data_s_max-data_s_min)*0.01) &
            (ddata_s_denergies[lm_i] < coeff_line))
    else:
        # the only criterium is to be inside the energy range
        crit_i = np.where((energies[lm_i] >= min(energy_range)) &
                          (energies[lm_i] <= max(energy_range)))

    # energies[lm_i][crit_i] are the possible energies satisfing the criteria
    # that can be also empy so in the case the function return 0
    if not energies[lm_i][crit_i].any():
        efermi = 0
    else:
        # fermi level is the highest energy satisfing the criteria
        efermi = max(energies[lm_i][crit_i])

    if print_out:
        print('Efermi = ', efermi, ' eV')

    return efermi
