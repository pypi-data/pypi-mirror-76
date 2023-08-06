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

"""This module is part of the Python NavARP library. It defines the main
program for exploring the data."""

__author__ = ["Federico Bisti"]
__license__ = "GPL"
__date__ = "10/08/2016"

from timeit import default_timer as timer   # check cpu time
import sys  # Needed for passing argv to QApplication

import numpy as np

from matplotlib.figure import Figure
from matplotlib import gridspec
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

from utils import navfile, fermilevel, navplt, ktransf, isocut

# GUI
from PyQt5 import QtWidgets  # Import the PyQt5 module
from PyQt5 import QtGui
#if exe-file
#from gui.main import Ui_MainWindow # This file holds the MainWindow
#else
from PyQt5.uic import loadUiType
from PyQt5.uic import loadUi

import os
if os.name == 'nt':  # this is a patch for Windows-Os to show the icon
    import ctypes
    myappid = u'navarp'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QtWidgets.QApplication(sys.argv)

screen = app.primaryScreen()
print('Screen: %s' % screen.name())
size = screen.size()
print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
print('Available: %d x %d' % (rect.width(), rect.height()))

path_navarp = os.path.dirname(__file__)
path_gui = os.path.join(path_navarp, 'gui')
Ui_MainWindow, QtBaseClass = loadUiType(os.path.join(path_gui, 'main.ui'))


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """Class initialization

        Args:
            self
        """

        super().__init__()

        # init main gui
        path_navarp_icon = os.path.join(path_gui, 'icons', 'navarp.svg')
        self.setWindowIcon(QtGui.QIcon(path_navarp_icon))
        self.setupUi(self)  # It sets up layout and widgets that are defined

        # init file
        config_path = os.path.join(os.path.expanduser("~"), '.navarp')
        if os.path.isfile(config_path):
            with open(config_path) as fdat:
                self.file_path = fdat.readline()
        else:
            self.file_path = os.path.expanduser("~")

        self.file_loaded_flag = False
        self.entry = None
        self.qpb_file.clicked.connect(self.openfile)

        # init figure
        self.fig = Figure(facecolor='#FFFFFF', constrained_layout=True)
        gs1 = gridspec.GridSpec(2, 1, figure=self.fig)
        self.axtop = self.fig.add_subplot(gs1[0])
        self.axbot = self.fig.add_subplot(gs1[1])
        self.isovmd_ln = None
        self.isovpd_ln = None
        self.scan_ln = None
        self.angle_ln = None
        self.addmpl()

        # init ColorScalePage
        self.qcb_cmaps.addItems(["binary", "binary_r", "magma_r", "magma",
                                 "viridis", "cividis", "plasma"])

        # init AboutDialog gui
        self.aboutDialog = AboutDialog(parent=self)
        self.openAboutDialogAction.triggered.connect(self.openAboutDialog)

    def openfile(self):
        """ Method for opening a new entry file.

        It use QtWidgets.QFileDialog.getOpenFileName to get the file path

        Args:
            self
        """

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open file',
            self.file_path,
            'ARPES files (*.h5 *.nxs *.txt *.zip *.sp2 *.pxt *.yaml)')

        if file_path:
            # ###############################
            # Load the entry file
            print("Loading ", file_path)
            self.file_path = file_path
            # set file_path note in the gui
            self.qle_file.setText(file_path)

            start_navfile = timer()
            self.entry = navfile.load(file_path)
            print('File loaded in =', timer()-start_navfile)

            # defining energies as of the gui
            if self.entry.scan_type == "hv":
                self.entry0_ekins = np.copy(self.entry.energies)
                self.entry0_hv = np.copy(self.entry.hv)
                self.e_f = self.entry.hv - self.entry.analyzer.work_fun
                [self.energies, self.entry.energies,
                 self.data] = fermilevel.align_to_same_eb(
                             self.e_f, self.entry.energies, self.entry.data)
            else:
                self.e_f = 0
                self.energies = np.copy(self.entry.energies)
                self.data = np.copy(self.entry.data)

            # ###############################
            # set navigation panel
            if self.file_loaded_flag:
                # disonnect navigation panel before changing values
                for qsb_value in [self.qsb_scan, self.qsb_angle,
                                  self.qsb_isov, self.qsb_isod,
                                  self.qsb_ks, self.qsb_kx]:
                    qsb_value.valueChanged.disconnect()
            else:  # connect only once with first file
                # enable and connect hide-lines
                for qcb_value in [self.qcb_bot_lns, self.qcb_iso_lns]:
                    qcb_value.setEnabled(True)
                    qcb_value.clicked.connect(self.hideline)

                # mode selection
                for qpb_mode in [self.qpb_isoe, self.qpb_isoek, self.qpb_isoa]:
                    qpb_mode.clicked.connect(self.select_mode)

            # set qsb_scan
            scans = self.entry.scans
            # scans can be a single value
            if len(scans) == 1:
                self.qsb_scan.setRange(scans, scans)
                self.qsb_scan.setSingleStep(0)
            else:
                self.qsb_scan.setRange(min(scans), max(scans))
                self.qsb_scan.setSingleStep(scans[1]-scans[0])
            self.qsb_scan.setValue((max(scans)+min(scans))*0.5)

            # set qsb_ks and qsb_kx to 0
            self.qsb_ks.setValue(0)
            self.qsb_kx.setValue(0)
            self.qle_kskx_angle.setText('atan2(ks,kx)={:.3f}°'.format(
                    np.rad2deg(np.arctan2(self.qsb_ks.value(),
                                          self.qsb_kx.value()))))

            # set to False hide-lines
            for qcb_value in [self.qcb_bot_lns, self.qcb_iso_lns]:
                qcb_value.setChecked(False)

            # enabling energy functions
            self.qsb_isov.setEnabled(True)
            self.qsb_isod.setEnabled(True)

            # set mode selection
            self.qpb_isoa.setChecked(False)
            self.qpb_isoe.setChecked(True)
            self.qpb_isoek.setChecked(False)

            # connect navigation panel
            for qsb_value, updatevalue in zip(
                    [self.qsb_scan, self.qsb_angle,
                     self.qsb_isov, self.qsb_isod,
                     self.qsb_ks, self.qsb_kx],
                    [self.updatescan, self.updateangle,
                     self.updateisov, self.updateisod,
                     self.updatescan, self.updateangle]):
                qsb_value.valueChanged.connect(updatevalue)

            # ###############################
            # connect ColorScalePage
            if not self.file_loaded_flag:  # connect only once with first file
                # Colorscale color
                self.qcb_cmaps.activated[str].connect(self.set_cmap)
                # Colorscale scale
                self.qcb_cmapscale.activated[str].connect(self.set_cmapscale)
                # Colorscale range
                for qsb_clim in [self.qsb_top_zmin, self.qsb_top_zmax,
                                 self.qsb_bot_zmin, self.qsb_bot_zmax]:
                    qsb_clim.valueChanged.connect(self.set_clim)
                # normalization of each scan in FS
                self.isoe_norm_cbx.clicked.connect(self.updateisov)

            # ###############################
            # set FermiLevelPage
            if self.file_loaded_flag:
                # disonnect FermiLevelPage before changing values
                for qrb_fermi in [self.qrb_ef_no, self.qrb_ef_yes,
                                  self.qrb_ef_val,
                                  self.qrb_range_cursor, self.qrb_range_full,
                                  self.qrb_yes_each_s, self.qrb_no_each_s]:
                    qrb_fermi.disconnect()
            else:  # connect only once with first file
                # connect FermiLevelPage qrb_ef_update
                self.qrb_ef_update.clicked.connect(self.align_fermi)

            # set FermiLevelPage with no Fermi alignment
            self.qrb_ef_no.setChecked(True)
            self.qrb_range_full.setChecked(True)
            if self.entry.scan_type == "hv":
                self.qrb_yes_each_s.setEnabled(False)
                self.qrb_no_each_s.setEnabled(False)
                self.qrb_yes_each_s.setChecked(True)
            else:
                self.qrb_yes_each_s.setEnabled(True)
                self.qrb_no_each_s.setEnabled(True)
                self.qrb_no_each_s.setChecked(True)

            # connect FermiLevelPage
            for qrb_fermi in [self.qrb_ef_no, self.qrb_ef_yes, self.qrb_ef_val,
                              self.qrb_range_cursor, self.qrb_range_full,
                              self.qrb_yes_each_s, self.qrb_no_each_s]:
                qrb_fermi.toggled.connect(self.align_fermi)

            # ###############################
            # set KTransfPage
            # set analyzer
            self.set_analyzer()
            # set qle_hv_ref
            self.qle_hv_ref.setText(str(self.entry.hv[0]))  # set read hv
            # set qle_theta_ref
            self.qle_theta_ref.setText(str(0))  # set qle_theta_ref for Kspace
            # connect KTransfPage
            if not self.file_loaded_flag:  # connect only once with first file
                # For setting the ref-point to the gamma point
                self.qpb_set_ref_gamma.clicked.connect(self.set_ref_gamma)
                # For extracting the ref-point form the cursor
                self.qpb_set_ref_p.clicked.connect(self.set_ref_point)
                # For setting the analyzer from entry
                self.qpb_set_analyzer.clicked.connect(self.set_analyzer)

            # ###############################
            # set FileInfoPage
            self.qte_note.setText(self.entry.file_note)

            # ###############################
            # make the plot
            self.select_mode()

            # ###############################
            # End loading file
            if not self.file_loaded_flag:  # connect only once with first file
                print('Gui connected')
                self.file_loaded_flag = True
            else:
                print('Gui already connected')
        else:
            print("No file selected")

    def select_mode(self):
        """Method switching the plot mode between Iso-Angle Iso-E(ang) Iso-E(k)

        Args:
            self
        """

        for qsb_value in [self.qsb_angle, self.qsb_isov, self.qsb_isod]:
            qsb_value.valueChanged.disconnect()

        angle_range = abs(self.entry.angles.max() - self.entry.angles.min())
        # set qsb_isov and qsb_isod depending on the mode (energy or angle)
        if self.qpb_isoa.isChecked():
            print("Selected mode is Iso-Angle")
            # set qle_angle
            self.ql_angle.setText("Energy")

            # set qsb_isod
            self.qsb_isod.setValue(angle_range*0.005)
            self.qsb_isod.setSingleStep(angle_range*0.005)
            # set qsb_isov
            self.qsb_isov.setSingleStep(self.qsb_isod.value())
            self.qsb_isov.setRange(self.entry.angles.min(),
                                   self.entry.angles.max())
            self.qsb_isov.setValue(self.qsb_angle.value())

            # set qsb_angle
            self.qsb_angle.setSingleStep(self.entry.hv[0]/10000)
            self.qsb_angle.setRange(self.energies.min(),
                                    self.energies.max())
            self.qsb_angle.setValue(
                (self.energies.max() - self.energies.min())*0.7 +
                self.energies.min())

        elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
            if self.qpb_isoe.isChecked():
                print("Selected mode is Iso-E(ang)")
            elif self.qpb_isoek.isChecked():
                print("Selected mode is Iso-E(k)")
            # set qle_angle
            self.ql_angle.setText("Angle")

            # set qsb_isod
            self.qsb_isod.setValue(self.entry.hv[0]/10000)
            self.qsb_isod.setSingleStep(self.entry.hv[0]/10000)
            # set qsb_isov
            self.qsb_isov.setSingleStep(self.qsb_isod.value())
            self.qsb_isov.setRange(self.energies.min(),
                                   self.energies.max())
            self.qsb_isov.setValue(
                (self.energies.max() - self.energies.min())*0.7 +
                self.energies.min())

            # set qsb_angle
            self.qsb_angle.setRange(self.entry.angles.min(),
                                    self.entry.angles.max())
            self.qsb_angle.setSingleStep(angle_range*0.005)
            self.qsb_angle.setValue(self.qsb_angle.value())

        # enabling qsb_scan and qsb_angle functions
        self.qsb_scan.setEnabled(not self.qpb_isoek.isChecked())
        self.qsb_angle.setEnabled(not self.qpb_isoek.isChecked())

        # enabling qsb_kx and qsb_ks functions
        self.qsb_kx.setEnabled(self.qpb_isoek.isChecked())
        self.qsb_ks.setEnabled(self.qpb_isoek.isChecked())

        # enabling values for KSpace transformation
        for qle in [self.qle_kx_ref, self.qle_ky_ref,
                    self.qcb_kph, self.qle_inn_pot,
                    self.qle_theta_ref, self.qle_tilt_ref,
                    self.qle_hv_ref, self.qle_energy_ref,
                    self.qle_tht_ap, self.qle_phi_ap,
                    self.qle_wfa, self.qcb_defl]:
            qle.setEnabled(not self.qpb_isoek.isChecked())

        for qsb_value, updatevalue in zip(
                [self.qsb_angle, self.qsb_isov, self.qsb_isod],
                [self.updateangle, self.updateisov, self.updateisod]):
            qsb_value.valueChanged.connect(updatevalue)

        self.newplot()

    def addmpl(self):
        """Method for adding a new matplotlib-layout widget

        Args:
            self
        """

        self.canvas = FigureCanvas(self.fig)
        self.mpllayout.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwidget, coordinates=True)
        self.mpllayout.addWidget(self.toolbar)
        # mouse navigation with right-click
        self.cidpress = self.canvas.mpl_connect('button_press_event',
                                                self.mpl_mouse_press)
        # mouse navigation with scroll
        self.cidscroll = self.canvas.mpl_connect('scroll_event',
                                                 self.mpl_mouse_scroll)

    def rmvmpl(self):
        """Method for removing the present matplotlib-layout widget

        Args:
            self
        """

        if self.file_loaded_flag:
            self.axtop.lines.remove(self.isovmd_ln)
            self.axtop.lines.remove(self.isovpd_ln)
            self.isovmd_ln = None
            self.isovpd_ln = None
            self.axbot.lines.remove(self.scan_ln)
            self.scan_ln = None
            self.axbot.lines.remove(self.angle_ln)
            self.angle_ln = None

            self.axtop.cla()
            self.axbot.cla()
        self.mpllayout.removeWidget(self.canvas)
        self.canvas.close()
        self.mpllayout.removeWidget(self.toolbar)
        self.toolbar.close()

    def newplot(self):
        """ Method for plotting the self.entry.

        It removes the present matplotlib-layour making a new one.

        Args:
            self
        """

        start_newplot = timer()

        self.rmvmpl()  # remove present plot

        # calculate ztop
        ztop = self.get_ztop()

        # calculate zbot
        zbot = self.get_zbot()

        # calculate xtop, ytop and xbot, ybot
        if self.qpb_isoa.isChecked():
            # new plot in axtop
            xtop = self.entry.angles
            ytop = self.energies

            # new plot in axbot
            xbot = self.energies
            ybot = self.entry.scans

        elif self.qpb_isoe.isChecked():
            # new plot in axtop
            xtop = self.entry.angles
            ytop = self.energies

            # new plot in axbot
            xbot = self.entry.angles
            ybot = self.entry.scans

        elif self.qpb_isoek.isChecked():
            self.get_surface_normal()
            self.entry.kx = self.get_ktransf_kx()
            kx_val, ks_val = self.get_ktransf_kx_ks_vals()
            self.entry.kx_fs, self.entry.ks_fs = self.get_ktransf_fs()

            self.qsb_ks.valueChanged.disconnect()
            self.qsb_kx.valueChanged.disconnect()

            # set kx and ks ranges
            kx_range_emin, ks_range_emin = self.get_ktransf_fs(
                    e_kin_val=self.energies.min()+self.e_f)
            kx_range_emax, ks_range_emax = self.get_ktransf_fs(
                    e_kin_val=self.energies.max()+self.e_f)
            kx_range_min = min(kx_range_emin.min(), kx_range_emax.min())
            kx_range_max = max(kx_range_emin.max(), kx_range_emax.max())
            self.qsb_kx.setRange(kx_range_min, kx_range_max)
            self.qsb_kx.setSingleStep(((kx_range_max - kx_range_min)*0.005))
            ks_range_min = min(ks_range_emin.min(), ks_range_emax.min())
            ks_range_max = max(ks_range_emin.max(), ks_range_emax.max())
            self.qsb_ks.setRange(ks_range_min, ks_range_max)
            self.qsb_ks.setSingleStep(((ks_range_max - ks_range_min)*0.01))

            self.qsb_kx.setValue(float(kx_val))
            self.qsb_ks.setValue(float(ks_val))
            self.qle_kskx_angle.setText('atan2(ks,kx)={:.3f}°'.format(
                    np.rad2deg(np.arctan2(float(ks_val),
                                          float(kx_val)))))

            self.qsb_ks.valueChanged.connect(self.updatescan)
            self.qsb_kx.valueChanged.connect(self.updateangle)

            # axtop kx vs Bind. E.
            xtop = self.entry.kx
            ytop = self.energies

            # axbot Kx vs Scan
            xbot = self.entry.kx_fs
            ybot = self.entry.ks_fs

        self.qmtop = self.get_new_qm(xtop, ytop, ztop, "top")
        self.qmbot = self.get_new_qm(xbot, ybot, zbot, "bot")
        self.set_scan_ln()
        self.set_angle_ln()
        self.set_isov_lns()

        self.addmpl()

        # saving axtop_bkg and axbot_bkg
        self.updatecanvas(clr_axtop=True, draw_axtop=True)
        self.updatecanvas(clr_axbot=True, draw_axbot=True, canvas_update=True)
        self.updatescan()  # needed as patch otherwise axtop glitching

        end_newplot = timer()
        print("newplot time =", end_newplot-start_newplot)

    def get_new_qm(self, x, y, z, panel):
        """Method plotting ax from x, y, z and returning qm.

        Args:
            x (ndarray): Array for the horizontal axis
            y (ndarray): Array for the vertical axis
            z (ndarray): Intensity matrix
            panel (string): "top" or "bot", panel name referring to ax
        Returns:
            The returned value is the object matplotlib.collections.QuadMesh
                from ax.pcolormesh
        """
        if panel == "top":
            ax = self.axtop
            style = self.get_qmtop_style()
            z_range = [float(self.qsb_top_zmin.value()),
                       float(self.qsb_top_zmax.value())]
        elif panel == "bot":
            ax = self.axbot
            style = self.get_qmbot_style()
            z_range = [float(self.qsb_bot_zmin.value()),
                       float(self.qsb_bot_zmax.value())]

        cmap = self.qcb_cmaps.currentText()
        cmapscale = self.qcb_cmapscale.currentText()
        qm = navplt.pimage(
            x, y, z, cmap, ax, z_range, style, cmapscale=cmapscale)
        return qm

    def get_surface_normal(self):
        """Method generating self.tht_an and self.phi_an.

        Args:
            self
        """

        self.entry.analyzer.tht_ap = float(self.qle_tht_ap.text())
        self.entry.analyzer.phi_ap = float(self.qle_phi_ap.text())

        refs_p = {"tht_p": float(self.qle_theta_ref.text()),
                  "hv_p": float(self.qle_hv_ref.text()),
                  "e_kin_p": float(self.qle_energy_ref.text()),
                  "k_along_slit_p": float(self.qle_kx_ref.text()),
                  "p_hv": self.get_p_hv(),
                  "scan_p": float(self.qle_tilt_ref.text()),
                  "ks_p": float(self.qle_ky_ref.text())}

        self.tht_an, self.phi_an, self.scans_0 = ktransf.get_surface_normal(
                self.entry, refs_p)

    def get_ktransf_kx_ks_vals(self):
        """Method returning k-space values.

        Args:
            self
        """
        # get angle_val for kx_val
        angle_val = float(self.qsb_angle.value())
        # get s_val for ks_val
        s_val = float(self.qsb_scan.value())
        # get isov for ktransf
        e_kin_val = self.qsb_isov.value() + self.e_f

        ky_p = float(self.qle_ky_ref.text())
        inn_pot = float(self.qle_inn_pot.text())
        tht_ap = float(self.qle_tht_ap.text())
        phi_ap = float(self.qle_phi_ap.text())
        p_hv = self.get_p_hv()

        if self.entry.scan_type == "hv":
            s_index = np.argmin(abs(self.entry.scans-s_val))

            kx_val = ktransf.get_k_along_slit(
                    e_kin_val[s_index], angle_val, self.tht_an,
                    p_hv=p_hv, hv=s_val, tht_ap=tht_ap)

            ks_val = ktransf.get_k_perp_sample(
                    e_kin_val[s_index], inn_pot, kx_val, ky_p,
                    p_hv=p_hv, hv=s_val, tht_ap=tht_ap, phi_ap=phi_ap,
                    tht_an=self.tht_an, phi_an=self.phi_an)
        else:
            kx_val = ktransf.get_k_along_slit(
                    e_kin_val, angle_val, self.tht_an,
                    p_hv=p_hv, hv=self.entry.hv[0], tht_ap=tht_ap)

            if (self.entry.scan_type == "polar" or
                    self.entry.scan_type == "tilt"):
                phi = 0  # NO DEFLECTOR!
                ks_val = ktransf.get_k_perp_slit(
                    e_kin_val, angle_val, self.tht_an, phi, s_val-self.scans_0,
                    p_hv=p_hv, hv=self.entry.hv[0],
                    tht_ap=tht_ap, phi_ap=phi_ap)
            elif self.entry.scan_type == "deflector":  # DEFLECTOR scan!
                ks_val = ktransf.get_k_perp_slit(
                    e_kin_val, angle_val, self.tht_an,
                    s_val-self.scans_0, self.phi_an,
                    p_hv=p_hv, hv=self.entry.hv[0],
                    tht_ap=tht_ap, phi_ap=phi_ap)
            elif self.entry.scan_type == "azimuth":
                scans_rad = np.radians(s_val-self.scans_0)
                krho = kx_val
                kx_val = np.squeeze(krho * np.cos(scans_rad))
                ks_val = np.squeeze(krho * np.sin(scans_rad))
            else:
                ks_val = s_val

        return kx_val, ks_val

    def get_ktransf_kx(self):
        """Method returning k-space values.

        Args:
            self
        """

        if self.entry.scan_type == "hv":
            s_val = float(self.qsb_scan.value())
            s_index = np.argmin(abs(self.entry.scans-s_val))
            energies_for_kx = self.entry.energies[s_index, :]
            hv_for_kx = self.entry.hv[s_index]
        else:
            energies_for_kx = self.entry.energies
            hv_for_kx = self.entry.hv[0]

        kxs = ktransf.get_k_along_slit(
            energies_for_kx,
            self.entry.angles,
            self.tht_an,
            p_hv=self.get_p_hv(),
            hv=hv_for_kx,
            tht_ap=float(self.qle_tht_ap.text()))

        return kxs

    def get_ktransf_fs(self, e_kin_val=np.array([])):
        """Method returning k-space values.

        Args:
            self
        """
        if e_kin_val.size > 0:
            e_kin_val = e_kin_val
        else:
            e_kin_val = self.qsb_isov.value() + self.e_f

        self.entry.analyzer.tht_ap = float(self.qle_tht_ap.text())
        self.entry.analyzer.phi_ap = float(self.qle_phi_ap.text())

        kx_fs, ks_fs = ktransf.get_k_isoen(
                entry=self.entry,
                e_kin_val=e_kin_val,
                tht_an=self.tht_an,
                phi_an=self.phi_an,
                k_perp_slit_for_kz=float(self.qle_ky_ref.text()),
                inn_pot=float(self.qle_inn_pot.text()),
                p_hv=self.get_p_hv())

        return kx_fs, ks_fs

    def get_p_hv(self):
        """Method returning p_hv from gui values.

        Args:
            p_hv
        """
        kph = self.qcb_kph.currentText()
        if kph == "yes":
            p_hv = True
        elif kph == "no":
            p_hv = False

        return p_hv

    def get_ztop(self):
        """Method returning ztop for gui values.

        Args:
            self
        """
        s_val = float(self.qsb_scan.value())
        dscan = 0
        ztop = isocut.maps_sum(
            s_val, dscan, self.entry.scans, self.data, axis=0)
        ztop = navplt.norm(ztop, mode="all")
        return ztop

    def get_zbot(self):
        """Method returning zbot for gui values.

        Args:
            self
        """
        isov = self.qsb_isov.value()
        isod = self.qsb_isod.value()
        if self.qpb_isoa.isChecked():
            zbot = isocut.maps_sum(
                isov, isod, self.entry.angles, self.data, axis=1)
        elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
            zbot = isocut.maps_sum(
                isov, isod, self.energies, self.data, axis=2)

        if self.isoe_norm_cbx.isChecked():
            zbot = navplt.norm(zbot, mode="each")
        else:
            zbot = navplt.norm(zbot, mode="all")
        return zbot

    def get_qmtop_style(self):
        """Method returning qmbot_style depending on scan_type and plot mode.

        Args:
            qmtop_style
        """
        if self.qpb_isoek.isChecked():  # k-space
            x_label = 'kx'
        else:  # angle-space
            x_label = 'tht'

        if self.qrb_ef_no.isChecked():  # kinetic energy
            if self.entry.scan_type == "hv":
                y_label = 'ekhv'
            else:
                y_label = 'ekin'
        else:  # binding energy
            y_label = 'eef'

        return x_label + '_' + y_label

    def get_qmbot_style(self):
        """Method returning qmbot_style depending on scan_type and plot mode.

        Args:
            self
        """
        if self.qpb_isoa.isChecked():  # angle integration
            if self.qrb_ef_no.isChecked():  # kinetic energy
                x_label = 'ekin'
            else:  # binding energy
                x_label = 'eef'
        elif self.qpb_isoe.isChecked():  # energy integration in angle-space
            x_label = 'tht'
        elif self.qpb_isoek.isChecked():  # energy integration in k-space
            x_label = 'kx'

        if self.entry.scan_type == "hv":
            if self.qpb_isoek.isChecked():  # k-space
                y_label = 'kz'
            else:
                y_label = 'hv'
        else:
            if self.qpb_isoek.isChecked():  # k-space
                y_label = 'ky'
            else:
                y_label = 'phi'

        return x_label + '_' + y_label

    def get_ln_color(self):
        """Method returning line color, depending on cmap used.

        Args:
            self
        """
        # get the line color depending on the cmap used
        if (self.qcb_cmaps.currentText() == 'binary' or
                self.qcb_cmaps.currentText() == 'magma_r'):
            ln_color = 'b'
        else:
            ln_color = 'w'
        return ln_color

    def set_scan_ln(self):
        """Method setting the scan line of axbot.

        Args:
            self
        """

        if self.scan_ln:  # if line already exist then update, else create
            if self.qpb_isoa.isChecked() or self.qpb_isoe.isChecked():
                s_val = float(self.qsb_scan.value())
                self.scan_ln.set_ydata(s_val)
            elif self.qpb_isoek.isChecked():
                if self.entry.scan_type == "hv":
                    s_val = float(self.qsb_scan.value())
                    s_index = np.argmin(abs(self.entry.scans-s_val))
                    self.scan_ln.set_xdata(self.entry.kx_fs[:, s_index])
                    self.scan_ln.set_ydata(self.entry.ks_fs[:, s_index])
                elif (self.entry.scan_type == "polar" or
                        self.entry.scan_type == "tilt" or
                        self.entry.scan_type == "deflector"):
                    s_val = float(self.qsb_scan.value())
                    s_index = np.argmin(abs(self.entry.scans-s_val))
                    self.scan_ln.set_ydata(self.entry.ks_fs[s_index, :])
                elif self.entry.scan_type == "azimuth":
                    s_val = float(self.qsb_scan.value())
                    s_index = np.argmin(abs(self.entry.scans-s_val))
                    self.scan_ln.set_xdata(self.entry.kx_fs[s_index, :])
                    self.scan_ln.set_ydata(self.entry.ks_fs[s_index, :])
                else:
                    ks_val = float(self.qsb_ks.value())
                    self.scan_ln.set_ydata(ks_val)
        else:
            # get the line color depending on the cmap used
            ln_color = self.get_ln_color()

            if self.qpb_isoa.isChecked() or self.qpb_isoe.isChecked():
                s_val = float(self.qsb_scan.value())
                self.scan_ln = self.axbot.axhline(s_val,
                                                  color=ln_color,
                                                  linewidth=1.0)
            elif self.qpb_isoek.isChecked():
                if self.entry.scan_type == "hv":
                    s_val = float(self.qsb_scan.value())
                    s_index = np.argmin(abs(self.entry.scans-s_val))
                    self.scan_ln, = self.axbot.plot(
                            self.entry.kx_fs[:, s_index],
                            self.entry.ks_fs[:, s_index],
                            '-', color=ln_color, linewidth=1.0)
                elif (self.entry.scan_type == "polar" or
                        self.entry.scan_type == "tilt" or
                        self.entry.scan_type == "deflector"):
                    s_val = float(self.qsb_scan.value())
                    s_index = np.argmin(abs(self.entry.scans-s_val))
                    self.scan_ln, = self.axbot.plot(
                            self.entry.kx_fs,
                            self.entry.ks_fs[s_index, :],
                            '-', color=ln_color, linewidth=1.0)
                elif self.entry.scan_type == "azimuth":
                    s_val = float(self.qsb_scan.value())
                    s_index = np.argmin(abs(self.entry.scans-s_val))
                    self.scan_ln, = self.axbot.plot(
                            self.entry.kx_fs[s_index, :],
                            self.entry.ks_fs[s_index, :],
                            '-', color=ln_color, linewidth=1.0)
                else:
                    ks_val = float(self.qsb_ks.value())
                    self.scan_ln = self.axbot.axhline(ks_val,
                                                      color=ln_color,
                                                      linewidth=1.0)

            self.scan_ln.set_visible(not self.qcb_bot_lns.isChecked())

    def set_angle_ln(self):
        """Method setting the angle line of axbot.

        Args:
            self
        """

        if self.qpb_isoa.isChecked():
            val = float(self.qsb_angle.value())
        elif self.qpb_isoe.isChecked():
            val = float(self.qsb_angle.value())
        elif self.qpb_isoek.isChecked():
            val = float(self.qsb_kx.value())

        if self.angle_ln:  # if line already exist then update, else create
            self.angle_ln.set_xdata(val)
        else:
            # get the line color depending on the cmap used
            ln_color = self.get_ln_color()

            self.angle_ln = self.axbot.axvline(val,
                                               color=ln_color,
                                               linewidth=1.0)
            self.angle_ln.set_visible(not self.qcb_bot_lns.isChecked())

    def set_isov_lns(self):
        """Method setting the iso-value lines of axtop.

        Args:
            self
        """

        isov = self.qsb_isov.value()
        isod = self.qsb_isod.value()

        if self.isovmd_ln:  # if line already exist then update, else create
            if self.qpb_isoa.isChecked():
                self.isovmd_ln.set_xdata(isov-isod)
                self.isovpd_ln.set_xdata(isov+isod)
            elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
                self.isovmd_ln.set_ydata(isov-isod)
                self.isovpd_ln.set_ydata(isov+isod)
        else:
            # get the line color depending on the cmap used
            ln_color = self.get_ln_color()

            if self.qpb_isoa.isChecked():
                self.isovmd_ln = self.axtop.axvline(isov-isod,
                                                    color=ln_color,
                                                    linewidth=1.0)
                self.isovpd_ln = self.axtop.axvline(isov+isod,
                                                    color=ln_color,
                                                    linewidth=1.0)
            elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
                self.isovmd_ln = self.axtop.axhline(isov-isod,
                                                    color=ln_color,
                                                    linewidth=1.0)
                self.isovpd_ln = self.axtop.axhline(isov+isod,
                                                    color=ln_color,
                                                    linewidth=1.0)
            self.isovmd_ln.set_visible(not self.qcb_iso_lns.isChecked())
            self.isovpd_ln.set_visible(not self.qcb_iso_lns.isChecked())

    def set_ref_gamma(self):
        """ Method setting the ref-point to the gamma point.

        The ref-point is used in the isoek mode.

        Args:
            self
        """

        self.qle_kx_ref.setText(str(0))
        self.qle_ky_ref.setText(str(0))

    def set_ref_point(self):
        """ Method extracting the ref-point form the cursor.

        The ref-point is used in the isoek mode.

        Args:
            self
        """

        if self.qpb_isoa.isChecked():
            energy_panel = self.qsb_angle.value()
            self.qle_theta_ref.setText(str(self.qsb_isov.value()))
        elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
            energy_panel = self.qsb_isov.value()
            self.qle_theta_ref.setText(str(self.qsb_angle.value()))

        if self.entry.scan_type == "hv":
            s_val = float(self.qsb_scan.value())
            s_index = np.argmin(abs(self.entry.scans-s_val))
            self.qle_hv_ref.setText(str(s_val))
            self.qle_energy_ref.setText(str(energy_panel + self.e_f[s_index]))
            self.qle_tilt_ref.setText(str(0))
        elif (self.entry.scan_type == "polar" or
                self.entry.scan_type == "tilt" or
                self.entry.scan_type == "deflector" or
                self.entry.scan_type == "azimuth"):
            self.qle_energy_ref.setText(str(energy_panel + self.e_f))
            self.qle_tilt_ref.setText(str(self.qsb_scan.value()))
            self.qle_hv_ref.setText(str(self.entry.hv[0]))
        # move cursor in qle_energy_ref and qle_hv_ref for text readability
        self.qle_energy_ref.setCursorPosition(1)
        self.qle_hv_ref.setCursorPosition(1)

    def set_analyzer(self):
        """ Method setting the analyzer from entry.

        The ref-point is used in the isoek mode.

        Args:
            self
        """

        self.qle_tht_ap.setText(str(self.entry.analyzer.tht_ap))
        self.qle_phi_ap.setText(str(self.entry.analyzer.phi_ap))
        self.qle_wfa.setText(str(self.entry.analyzer.work_fun))
        self.qcb_defl.setCurrentIndex(int(self.entry.analyzer.deflector))

    def hideline(self):
        """ Method for hiding the navigation lines of the matplotlib-layout.

        Args:
            self
        """

        self.scan_ln.set_visible(not self.qcb_bot_lns.isChecked())
        self.angle_ln.set_visible(not self.qcb_bot_lns.isChecked())
        self.isovmd_ln.set_visible(not self.qcb_iso_lns.isChecked())
        self.isovpd_ln.set_visible(not self.qcb_iso_lns.isChecked())

        self.updatecanvas(restore_axtop=True, restore_axbot=True,
                          canvas_update=True)

    def set_cmap(self):
        """ Method for changing the color of the maps and lines.

        Args:
            self
        """

        self.qmtop.set_cmap(self.qcb_cmaps.currentText())
        self.qmbot.set_cmap(self.qcb_cmaps.currentText())
        ln_color = self.get_ln_color()
        self.scan_ln.set_color(ln_color)
        self.angle_ln.set_color(ln_color)
        self.isovmd_ln.set_color(ln_color)
        self.isovpd_ln.set_color(ln_color)

        self.updatecanvas(clr_axtop=True, draw_axtop=True,
                          clr_axbot=True, draw_axbot=True,
                          canvas_update=True)

    def set_cmapscale(self):
        """ Method for changing the colormap scale between linear/log/power.

        Args:
            self
        """

        zmin = float(self.qsb_top_zmin.value())
        zmax = float(self.qsb_top_zmax.value())
        norm_top = navplt.get_cmapscale(self.qcb_cmapscale.currentText(),
                                        vmin=zmin, vmax=zmax, clip=False)
        self.qmtop.set_norm(norm_top)

        zmin = float(self.qsb_bot_zmin.value())
        zmax = float(self.qsb_bot_zmax.value())
        norm_bot = navplt.get_cmapscale(self.qcb_cmapscale.currentText(),
                                        vmin=zmin, vmax=zmax, clip=False)
        self.qmbot.set_norm(norm_bot)

        self.updatecanvas(clr_axtop=True, draw_axtop=True,
                          clr_axbot=True, draw_axbot=True,
                          canvas_update=True)

    def set_clim(self):
        """ Method for changing the color scale max and min of the maps.

        Args:
            self
        """

        sender_top = [self.qsb_top_zmin, self.qsb_top_zmax]
        sender_bot = [self.qsb_bot_zmin, self.qsb_bot_zmax]

        if self.sender() in sender_top:
            zmin = float(self.qsb_top_zmin.value())
            if zmin <= 0:
                zmin = 1e-4
            zmax = float(self.qsb_top_zmax.value())
            self.qsb_top_zmin.setRange(1e-4, zmax)
            self.qsb_top_zmax.setRange(zmin, 1)
            self.qmtop.set_clim(zmin, zmax)
            self.updatecanvas(draw_axtop=True, canvas_update=True)
        elif self.sender() in sender_bot:
            zmin = float(self.qsb_bot_zmin.value())
            if zmin <= 0:
                zmin = 1e-4
            zmax = float(self.qsb_bot_zmax.value())
            self.qsb_bot_zmin.setRange(1e-4, zmax)
            self.qsb_bot_zmax.setRange(zmin, 1)
            self.qmbot.set_clim(zmin, zmax)
            self.updatecanvas(draw_axbot=True, canvas_update=True)

    def updatecanvas(self, save_axtop_bkg=True, save_axbot_bkg=True,
                     restore_axtop=False, restore_axbot=False,
                     draw_axtop=False, draw_axbot=False,
                     clr_axtop=False, clr_axbot=False,
                     canvas_update=False, canvas_draw=False):
        """ Method for updating the matplotlib-layout.

        The method saves or restores the background for top or bot axes.
        This avoids to re-draw unmodified part of the matplotlib figure, giving
        high screen refresh rate.

        Args:
            self
            save_axtop_bkg (boolean, optional): If True, save self.axtop_bkg
            save_axbot_bkg (boolean, optional): If True, save self.axbot_bkg
            restore_axtop (boolean, optional): If True, restore the region
                self.axtop_bkg
            restore_axbot (boolean, optional): If True, restore the region
                self.axbot_bkg
            clr_axtop (boolean, optional): If True, draw mesh for cleaning
                axtop
            clr_axbot (boolean, optional): If True, draw mesh for cleaning
                axbot
            draw_axtop (boolean, optional): If True, draw the bot axis
            draw_axbot (boolean, optional): If True, draw the bot axis
            canvas_update (boolean, optional): If True, update the canvas and
                flush_events
            canvas_draw (boolean, optional): If True, draw the canvas
        """
        top_rmv_mesh = None
        bot_rmv_mesh = None

        if draw_axtop or restore_axtop:
            if draw_axtop:
                if clr_axtop:
                    # Create a mesh for cleaning axtop
                    top_rmv_mesh = self.axtop.pcolormesh(
                            np.array(self.axtop.get_xlim()),
                            np.array(self.axtop.get_ylim()),
                            np.zeros((1, 1)), cmap='binary', zorder=-10)
                    self.axtop.draw_artist(top_rmv_mesh)
                self.axtop.draw_artist(self.qmtop)
                if save_axtop_bkg:
                    self.canvas.flush_events()
                    self.axtop_bkg = self.canvas.copy_from_bbox(
                            self.axtop.bbox)
                    self.axtop_bkg_lims = [self.axtop.get_xlim(),
                                           self.axtop.get_ylim()]
            elif restore_axtop:
                flag_get_extents = (self.axtop_bkg.get_extents() ==
                    self.canvas.copy_from_bbox(self.axtop.bbox).get_extents())
                flag_lims = (self.axtop_bkg_lims ==
                             [self.axtop.get_xlim(), self.axtop.get_ylim()])
                if flag_get_extents and flag_lims:
                    self.canvas.restore_region(self.axtop_bkg)
                else:
                    # Create a mesh for cleaning axtop
                    top_rmv_mesh = self.axtop.pcolormesh(
                            np.array(self.axtop.get_xlim()),
                            np.array(self.axtop.get_ylim()),
                            np.zeros((1, 1)), cmap='binary', zorder=-10)
                    self.axtop.draw_artist(top_rmv_mesh)
                    self.axtop.draw_artist(self.qmtop)
                    self.canvas.flush_events()
                    self.axtop_bkg = self.canvas.copy_from_bbox(
                            self.axtop.bbox)
                    self.axtop_bkg_lims = [self.axtop.get_xlim(),
                                           self.axtop.get_ylim()]
            self.axtop.draw_artist(self.isovmd_ln)
            self.axtop.draw_artist(self.isovpd_ln)

        if draw_axbot or restore_axbot:
            if draw_axbot:
                if clr_axbot:
                    # Create a mesh for cleaning axbot
                    bot_rmv_mesh = self.axbot.pcolormesh(
                            np.array(self.axbot.get_xlim()),
                            np.array(self.axbot.get_ylim()),
                            np.zeros((1, 1)), cmap='binary', zorder=-10)
                    self.axbot.draw_artist(bot_rmv_mesh)
                self.axbot.draw_artist(self.qmbot)
                if save_axbot_bkg:
                    self.canvas.flush_events()
                    self.axbot_bkg = self.canvas.copy_from_bbox(
                            self.axbot.bbox)
                    self.axbot_bkg_lims = [self.axbot.get_xlim(),
                                           self.axbot.get_ylim()]
            elif restore_axbot:
                flag_get_extents = (self.axbot_bkg.get_extents() ==
                    self.canvas.copy_from_bbox(self.axbot.bbox).get_extents())
                flag_lims = (self.axbot_bkg_lims ==
                             [self.axbot.get_xlim(), self.axbot.get_ylim()])
                if flag_get_extents and flag_lims:
                    self.canvas.restore_region(self.axbot_bkg)
                else:
                    # Create a mesh for cleaning axbot
                    bot_rmv_mesh = self.axbot.pcolormesh(
                            np.array(self.axbot.get_xlim()),
                            np.array(self.axbot.get_ylim()),
                            np.zeros((1, 1)), cmap='binary', zorder=-10)
                    self.axbot.draw_artist(bot_rmv_mesh)
                    self.axbot.draw_artist(self.qmbot)
                    self.canvas.flush_events()
                    self.axbot_bkg = self.canvas.copy_from_bbox(
                            self.axbot.bbox)
                    self.axbot_bkg_lims = [self.axbot.get_xlim(),
                                           self.axbot.get_ylim()]
            self.axbot.draw_artist(self.scan_ln)
            self.axbot.draw_artist(self.angle_ln)

        if canvas_update:
            self.canvas.update()
            self.canvas.flush_events()

        if top_rmv_mesh:
            top_rmv_mesh.remove()
            top_rmv_mesh = None
            self.canvas.flush_events()
        if bot_rmv_mesh:
            bot_rmv_mesh.remove()
            bot_rmv_mesh = None
            self.canvas.flush_events()

        if canvas_draw:
            self.canvas.draw()

    def updatescan(self, sender=None):
        """ Method for updating the maps after changing the scan value.

        Args:
            self
        """

        ztop = self.get_ztop()

        self.set_scan_ln()
        if (sender == 'mpl_mouse_motion' or
                sender == 'mpl_mouse_release'):
            self.set_angle_ln()  # In the case of navbot_motion, angle changes

        if self.qpb_isoa.isChecked() or self.qpb_isoe.isChecked():
            self.qmtop.set_array(ztop.ravel())
            clr_axtop = False
        elif self.qpb_isoek.isChecked():
            if (sender != 'mpl_mouse_motion' and
                    sender != 'mpl_mouse_release'):
                self.qsb_scan.valueChanged.disconnect()
            kx_val = float(self.qsb_kx.value())
            ks_val = float(self.qsb_ks.value())
            if self.entry.scan_type == "hv":  # new plot because axes changing

                isov = self.qsb_isov.value()
                ky_p = float(self.qle_ky_ref.text())
                inn_pot = float(self.qle_inn_pot.text())
                hv_p_init = float(self.qle_hv_ref.text())
                tht_ap = float(self.qle_tht_ap.text())
                phi_ap = float(self.qle_phi_ap.text())
                work_fun = float(self.qle_wfa.text())
                p_hv = self.get_p_hv()

                s_val = ktransf.get_hv_from_kxyz(
                    isov, work_fun, inn_pot, kx_val, ky_p, ks_val,
                    hv_p_init=hv_p_init,
                    p_hv=p_hv, tht_ap=tht_ap, phi_ap=phi_ap,
                    tht_an=self.tht_an, phi_an=self.phi_an)
                self.qsb_scan.setValue(s_val)

                self.entry.kx = self.get_ktransf_kx()

                xtop = self.entry.kx
                ytop = self.energies

                self.qmtop = self.get_new_qm(xtop, ytop, ztop, "top")

                clr_axtop = True
            else:
                if (self.entry.scan_type == "polar" or
                        self.entry.scan_type == "tilt" or
                        self.entry.scan_type == "deflector"):
                    angle_index = np.argmin(abs(self.entry.kx_fs-kx_val))
                    s_index = np.argmin(
                            abs(self.entry.ks_fs[:, angle_index]-ks_val))
                elif self.entry.scan_type == "azimuth":
                    azim_val = np.arctan2(ks_val, kx_val)
                    a_index_mid = int(self.entry.angles.shape[0]*0.5)
                    azim_diff = np.pi*2
                    s_index = 0
                    for a_index in np.array([0, a_index_mid, -1]):
                        s_index_new = np.argmin(abs(azim_val - np.arctan2(
                            self.entry.ks_fs[:, a_index],
                            self.entry.kx_fs[:, a_index]
                        )))
                        azim_diff_new = abs(azim_val - np.arctan2(
                            self.entry.ks_fs[s_index_new, a_index],
                            self.entry.kx_fs[s_index_new, a_index]
                        ))
                        if azim_diff_new < azim_diff:
                            azim_diff = azim_diff_new
                            s_index = s_index_new
                else:
                    s_index = np.argmin(abs(self.entry.ks_fs-ks_val))
                self.qsb_scan.setValue(self.entry.scans[s_index])
                self.qmtop.set_array(ztop.ravel())
                clr_axtop = True
            if (sender != 'mpl_mouse_motion' and
                    sender != 'mpl_mouse_release'):
                self.qsb_scan.valueChanged.connect(self.updatescan)

        if sender == 'mpl_mouse_motion':
            self.updatecanvas(restore_axbot=True, clr_axtop=clr_axtop,
                              draw_axtop=True, save_axtop_bkg=False,
                              canvas_update=True)
        else:
            self.updatecanvas(restore_axbot=True, clr_axtop=clr_axtop,
                              draw_axtop=True, canvas_update=True)

    def updateangle(self):
        """ Method for updating the maps after changing the angle value.

        Args:
            self
        """

        self.set_angle_ln()

        self.updatecanvas(restore_axbot=True, canvas_update=True)

    def updateisov(self, sender=None):
        """ Method for updating the maps after changing the iso-value.

        Args:
            self
        """

        zbot = self.get_zbot()

        self.set_isov_lns()

        if self.qpb_isoa.isChecked() or self.qpb_isoe.isChecked():
            self.qmbot.set_array(zbot.ravel())
            clr_axbot = False
        elif self.qpb_isoek.isChecked():  # new plot because axes changing
            self.entry.kx_fs, self.entry.ks_fs = self.get_ktransf_fs()

            xbot = self.entry.kx_fs
            ybot = self.entry.ks_fs

            self.qmbot = self.get_new_qm(xbot, ybot, zbot, "bot")

            clr_axbot = True

        if sender == 'mpl_mouse_motion':
            self.updatecanvas(restore_axtop=True, clr_axbot=True,
                              draw_axbot=True, save_axbot_bkg=False,
                              canvas_update=True)
        else:
            self.updatecanvas(restore_axtop=True, clr_axbot=clr_axbot,
                              draw_axbot=True, canvas_update=True)

    def updateisod(self):
        """ Method for updating the maps after changing the iso-value delta.

        Args:
            self
        """

        self.qsb_isov.setSingleStep(self.qsb_isod.value())
        self.updateisov()

    def mpl_mouse_scroll(self, event):
        """ Method for mouse scroll navigation, changing iso-value delta.

        Args:
            self
            event (matplotlib.backend_bases.Event): mouse event description
        """

        if event.button == 'up':
            self.qsb_isod.setValue(self.qsb_isod.value()*2)
        elif event.button == 'down':
            self.qsb_isod.setValue(self.qsb_isod.value()*0.5)

    def mpl_mouse_press(self, event):
        """ Method for mouse right-click navigation, button pressed.

        If right-click in the top panel, iso-value is changed to the mouse
            position.
        If right-click in the bot panel, scan and angle (or energy) are changed
            to the mouse position.

        The method saves the canvans background for speeding up the figure
            updates.

        Args:
            self
            event (matplotlib.backend_bases.Event): mouse event description
        """

        # if it is not the mouse right button then exit
        if event.button != 3:
            return None

        # if the mouse is not in the axis then exit
        if event.inaxes != self.axbot and event.inaxes != self.axtop:
            return None

        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidscroll)

        # Navigation with the cursor in axbot
        if event.inaxes == self.axbot:
            self.qsb_scan.valueChanged.disconnect()
            self.qsb_angle.valueChanged.disconnect()
            self.qsb_ks.valueChanged.disconnect()
            self.qsb_kx.valueChanged.disconnect()

        # Navigation with the cursor in axtop
        elif event.inaxes == self.axtop:
            self.qsb_isov.valueChanged.disconnect()

        # do first step even the mouse is still not moving
        self.mpl_mouse_motion(event)

        # activate mouse navigation with right-click
        # connect for mouse motion
        self.cidmotion = self.canvas.mpl_connect(
                'motion_notify_event', self.mpl_mouse_motion)
        # connect for mouse leaving axes
        self.cidleaveaxis = self.canvas.mpl_connect(
                'axes_leave_event', self.mpl_mouse_release)
        # connect for mouse releasing button
        self.cidrelease = self.canvas.mpl_connect(
                'button_release_event', self.mpl_mouse_release)

    def mpl_mouse_motion(self, event):
        """ Method for mouse right-click navigation, button pressed in motion.

        If right-click motion in the top panel, iso-value is changed following
            to the mouse position.
        If right-click motion in the bot panel, scan and angle (or energy) are
            changed following the mouse position.

        The method updates the figure to the new mouse positions during motion.

        Args:
            self
        """

        # Navigation with the cursor in axbot
        if event.button == 3 and event.inaxes == self.axbot:
            if self.qpb_isoa.isChecked() or self.qpb_isoe.isChecked():
                s_val = event.ydata
                self.qsb_scan.setValue(s_val)
                angle_val = event.xdata
                self.qsb_angle.setValue(angle_val)

            elif self.qpb_isoek.isChecked():
                kx_val = event.xdata
                self.qsb_kx.setValue(kx_val)
                ks_val = event.ydata
                self.qsb_ks.setValue(ks_val)
                self.qle_kskx_angle.setText('atan2(ks,kx)={:.3f}°'.format(
                        np.rad2deg(np.arctan2(ks_val,
                                              kx_val))))

            self.updatescan(sender='mpl_mouse_motion')

        # Navigation with the cursor in axtop
        if event.button == 3 and event.inaxes == self.axtop:
            if self.qpb_isoa.isChecked():
                isov = event.xdata
            elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
                isov = event.ydata
            self.qsb_isov.setValue(isov)

            self.updateisov(sender='mpl_mouse_motion')

    def mpl_mouse_release(self, event):
        """ Method for mouse right-click navigation, button released.

        If right-click in the top panel, iso-value is changed to the mouse
            position.
        If right-click in the bot panel, scan and angle (or energy) are changed
            to the mouse position.

        The method updates the figure to the mouse released position.

        Args:
            self
            event (matplotlib.backend_bases.Event): mouse event description
        """

        # disconnect for mouse motion
        self.canvas.mpl_disconnect(self.cidmotion)
        # disconnect for mouse leaving axes
        self.canvas.mpl_disconnect(self.cidleaveaxis)
        # disconnect for mouse releasing button
        self.canvas.mpl_disconnect(self.cidrelease)

        # Navigation with the cursor in axbot
        if event.button == 3 and event.inaxes == self.axbot:
            self.updatescan(sender='mpl_mouse_release')
            self.qsb_scan.valueChanged.connect(self.updatescan)
            self.qsb_angle.valueChanged.connect(self.updateangle)
            self.qsb_ks.valueChanged.connect(self.updatescan)
            self.qsb_kx.valueChanged.connect(self.updateangle)

        # Navigation with the cursor in axtop
        if event.button == 3 and event.inaxes == self.axtop:
            if self.qpb_isoa.isChecked():
                self.qsb_isov.setValue(event.xdata)
            elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
                self.qsb_isov.setValue(event.ydata)
            self.updateisov(sender='mpl_mouse_release')
            self.qsb_isov.valueChanged.connect(self.updateisov)

        self.canvas.flush_events()
        self.cidpress = self.canvas.mpl_connect('button_press_event',
                                                self.mpl_mouse_press)
        self.cidscroll = self.canvas.mpl_connect('scroll_event',
                                                 self.mpl_mouse_scroll)

    def align_fermi(self):
        """ Method for aligning the energy scale to the fermi level.

        Args:
            self
        """

        scans = self.entry.scans
        if self.sender().isChecked() or self.sender() == self.qrb_ef_update:
            # case for hv scan_type
            if self.entry.scan_type == "hv":
                self.entry.hv = np.copy(self.entry0_hv)
                self.entry.energies = np.copy(self.entry0_ekins)

                if self.qrb_ef_no.isChecked():
                    print('Selected no fermi alignment')

                    self.e_f = self.entry.hv - self.entry.analyzer.work_fun
                    [self.energies, self.entry.energies,
                     self.data] = fermilevel.align_to_same_eb(
                        self.e_f, self.entry.energies, self.entry.data)

                elif self.qrb_ef_yes.isChecked():
                    print('Selected fermi alignment')

                    # get the energy_range
                    if self.qrb_range_full.isChecked():
                        energy_range = None
                    elif self.qrb_range_cursor.isChecked():
                        if self.qpb_isoa.isChecked():
                            isov = self.qsb_angle.value()
                            isod = abs(self.energies.max() -
                                       self.energies.min())*0.05
                        elif (self.qpb_isoe.isChecked() or
                              self.qpb_isoek.isChecked()):
                            isov = self.qsb_isov.value()
                            isod = self.qsb_isod.value()
                        energy_range = (self.e_f[:, None] +
                                        np.array([isov-isod,
                                                  isov+isod])[None, :])

                    self.e_f, _ = fermilevel.dlog_fit_each(
                            scans,
                            self.entry.energies,
                            self.entry.data,
                            energy_range)

                    # Overwrite hv from e_f and analyzer work function
                    self.entry.hv = self.e_f + self.entry.analyzer.work_fun

                    # Align data and energies to same binding energy array
                    [self.energies, self.entry.energies,
                     self.data] = fermilevel.align_to_same_eb(
                        self.e_f, self.entry.energies, self.entry.data)

                    # print info on the fermi alignment
                    fermi_note = 'scan\te_f (eV)\tnew hv (eV)\n'
                    for ef_index in range(self.e_f.shape[0]):
                        fermi_note += '{:.3f}\t{:.3f}\t{:.3f}\n'.format(
                                scans[ef_index],
                                self.e_f[ef_index],
                                self.entry.hv[ef_index])
                    self.qte_fermi.setText(fermi_note)

            # other cases
            else:
                if self.qrb_ef_no.isChecked():
                    print('Selected no fermi alignment')
                    self.e_f = 0
                    self.energies = np.copy(self.entry.energies)
                    self.data = np.copy(self.entry.data)
                    fermi_note = 'e_f = {:.3f} eV\n'.format(self.e_f)

                elif self.qrb_ef_yes.isChecked():
                    print('Selected fermi alignment')
                    # get the energy_range
                    if self.qrb_range_full.isChecked():
                        energy_range = None
                    elif self.qrb_range_cursor.isChecked():
                        if self.qpb_isoa.isChecked():
                            isov = self.qsb_angle.value()
                            isod = abs(self.energies.max() -
                                       self.energies.min())*0.05
                        elif (self.qpb_isoe.isChecked() or
                              self.qpb_isoek.isChecked()):
                            isov = self.qsb_isov.value()
                            isod = self.qsb_isod.value()
                        energy_range = (np.array([isov-isod, isov+isod]) +
                                        self.e_f)

                    # each slice or all fermi level detection
                    if self.qrb_yes_each_s.isChecked():
                        self.ef_val, _ = fermilevel.dlog_fit_each(
                                scans,
                                self.entry.energies,
                                self.entry.data,
                                energy_range)
                        self.data, self.e_f = fermilevel.align_fermi_index(
                                self.ef_val,
                                self.energies,
                                self.entry.data)
                        self.qle_ef_val.setText('array')

                        fermi_note = 'scan\te_f (eV)\n'
                        for ef_index in range(self.ef_val.shape[0]):
                            fermi_note += '{:.3f}\t{:.3f}\n'.format(
                                    scans[ef_index],
                                    self.ef_val[ef_index])

                    elif self.qrb_no_each_s.isChecked():
                        self.data = np.copy(self.entry.data)
                        self.e_f, _ = fermilevel.dlog_fit(
                            self.entry.energies, self.entry.data, energy_range)
                        self.qle_ef_val.setText('{:.3f}'.format(self.e_f))

                        fermi_note = 'e_f = {:.3f} eV\n'.format(self.e_f)

                elif self.qrb_ef_val.isChecked():
                    print('Selected fixed value for fermi alignment')
                    self.data = np.copy(self.entry.data)
                    try:
                        self.e_f = float(self.qle_ef_val.text())
                    except ValueError:
                        self.e_f = 0
                    fermi_note = 'e_f = {:.3f} eV\n'.format(self.e_f)

                elif self.sender() == self.qrb_ef_update:
                    print('Fermi alignment updated')

                # Get the new energy array from e_f
                self.energies = self.entry.energies - self.e_f

                # Overwrite hv from e_f and analyzer work function
                if self.e_f != 0:
                    self.entry.hv[0] = self.e_f + self.entry.analyzer.work_fun
                    fermi_note += 'new hv = {:.3f} eV\n'.format(
                            self.entry.hv[0])

                self.qte_fermi.setText(fermi_note)

            if self.qpb_isoa.isChecked():
                # set qsb_angle where there is now the energy
                self.qsb_angle.setRange(self.energies.min(),
                                        self.energies.max())
                self.qsb_angle.setValue(
                    (self.energies.max() - self.energies.min())*0.7 +
                    self.energies.min())
            elif self.qpb_isoe.isChecked() or self.qpb_isoek.isChecked():
                self.qsb_isov.setRange(self.energies.min(),
                                       self.energies.max())
                self.qsb_isov.setValue(
                    (self.energies.max() - self.energies.min())*0.7 +
                    self.energies.min())

            self.newplot()

    def openAboutDialog(self):
        self.aboutDialog.show()

    def closeEvent(self, event):
        print("Saving configurations before closing")
        config_path = os.path.join(os.path.expanduser("~"), '.navarp')
        config_file = open(config_path, "w")
        config_file.write(self.file_path)
        config_file.close()


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)

        loadUi(os.path.join(path_gui, 'about.ui'), baseinstance=self)


def main():
#    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication

    form = Main()               # Set the form as Main
    form.show()                 # Show the form
#    form.showMaximized()
    screen_height = QtWidgets.QDesktopWidget().screenGeometry(-1).height()
    screen_width = QtWidgets.QDesktopWidget().screenGeometry(-1).width()
    form.setGeometry(int(screen_width*0.03), int(screen_height*0.04),
                     int(screen_height*0.9), int(screen_height*0.9))
#    form.resize(int(screen_width*0.5), int(screen_height*0.9))

    app.exec_()                 # and execute the app


if __name__ == '__main__':  # if running file directly and not importing it
    print(sys.version_info)             # print system version
    main()                              # run the main function
