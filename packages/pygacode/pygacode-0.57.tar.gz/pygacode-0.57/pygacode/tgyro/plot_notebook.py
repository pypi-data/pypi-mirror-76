#-------------------------------------------------------------
# notebook.py
#
# PURPOSE:
#  Notebook plotter to see tgyro results.
#-------------------------------------------------------------

import os
import wx
import matplotlib
import sys
import numpy as np
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib import rc
from gacodefuncs import *
from data import tgyrodata
from matplotlib.colors import LogNorm
from pygacode import expro

rc('text', usetex=True)
rc('font', size=18)

simdir = sys.argv[1]
units = int(sys.argv[2])
ext = sys.argv[3]
nstr = sys.argv[4]
loc = int(sys.argv[5])

n = int(nstr)

sim = tgyrodata(simdir, verbose=True)

print('Number of ions  : '+str(sim.n_ion))
print('Number of radii : '+str(sim.n_r))
print('Evolution eqns  : '+str(sim.n_evolve))
print('Completed iter  : '+str(sim.n_iterations))

x = sim.data['r/a'][0]
ggb = sim.data['Gamma_GB'][n]
qgb = sim.data['Q_GB'][n]
pgb = sim.data['Pi_GB'][n]

nit = sim.n_iterations+1
nx = sim.n_r-1

n_ion = sim.n_ion

wdir = os.path.realpath(simdir)

if n == -1:
    fin = r'$\mathtt{iter=final}$'
else:
    fin = r'$\mathtt{iter='+nstr+'}$'

init = r'$\mathtt{iter=0}$'


def plot_select(ax, tag):
    if 'flux' in tag:
        plot_flux(ax, tag)
    elif 'z' in tag:
        plot_z(ax, tag)
    elif 'res_' in tag:
        plot_residual(ax, tag)
    else:
        plot_smooth(ax, tag)


def setprof(exp, tag):

    if tag == 'ne':
        y = expro.expro_ne
    elif tag == 'Te':
        y = expro.expro_te
    elif tag == 'Ti_1':
        y = expro.expro_ti[0, :]
    elif tag == 'ni_1':
        y = expro.expro_ni[0, :]
    elif tag == 'ni_2':
        y = expro.expro_ni[1, :]
    elif tag == 'ni_3':
        y = expro.expro_ni[2, :]
    elif tag == 'dlntedr':
        y = expro.expro_dlntedr
    elif tag == 'dlnnedr':
        y = expro.expro_dlnnedr
    elif tag == 'dlntidr_1':
        y = expro.expro_dlntidr[0, :]
    else:
        raise NotImplementedError('Mapping of tag %s has not been implemented'%tag)

    return y


def plot_input_profiles(ax, tag, scale=0):

    # Helper routine to plot data (tag) from input.profiles

    f0 = 'input.profiles.'+str(0)
    fn = 'input.profiles.'+str(n)

    color = 'black'
    width = 5
    alpha = 0.2
    label = 'input.gacode'

    if os.path.isfile(f0):
        expro.expro_read(f0)
    else:
        expro.expro_read('input.gacode')

    xp = expro.expro_rmin

    snorm = max(xp)**scale

    xp = xp/max(xp)

    y = setprof(expro, tag)

    ax.plot(xp,
            y*snorm,
            color=color,
            alpha=alpha,
            linewidth=width,
            label=r'$\mathbf{'+label+'}$')

    if os.path.isfile(fn):
        expro.expro_read(fn)
        y = setprof(expro, tag)

        ax.plot(xp,
                y*snorm,
                color=color,
                alpha=alpha,
                linewidth=width,
                label=r'$\mathbf{'+label+'}$')


def plot_z(ax, tag):

    # Gradient scale lengths

    ax.grid(which="major", ls="-", alpha=0.1, linewidth=2)
    ax.grid(which="minor", ls=":", alpha=0.1, linewidth=2)
    ax.set_xlabel('$r/a$')

    if tag == 'zte':
        ax.plot(x, sim.data['a/Lte'][0], color='k', label=init)
        ax.plot(x, sim.data['a/Lte'][n], color='magenta', label=fin)
        ax.set_ylabel('$z_\mathrm{Te} = a/L_\mathrm{Te}$', color='k')
        plot_input_profiles(ax, 'dlntedr', 1)
    elif tag == 'zti':
        ax.plot(x, sim.data['a/Lti1'][0], color='k', label=init)
        ax.plot(x, sim.data['a/Lti1'][n], color='magenta', label=fin)
        ax.set_ylabel('$z_\mathrm{Ti} = a/L_\mathrm{Ti}$', color='k')
        plot_input_profiles(ax, 'dlntidr_1', 1)
    elif tag == 'zne':
        ax.plot(x, sim.data['a/Lne'][0], color='k', label=init)
        ax.plot(x, sim.data['a/Lne'][n], color='magenta', label=fin)
        ax.set_ylabel('$z_\mathrm{ne} = a/L_\mathrm{ne}$', color='k')
        plot_input_profiles(ax, 'dlnnedr', 1)

    ax.set_ylim([0.0, 10.0])
    ax.legend(loc=loc)
    plt.tight_layout


def plot_residual(ax, tag):

    if tag == 'res_tot':
        ax.grid(which="major", ls="-", alpha=0.1, linewidth=2)
        ax.grid(which="minor", ls=":", alpha=0.1, linewidth=2)
        ax.set_yscale('log')
        ze = np.sum(sim.data['E(eflux_e)'][:, 1:], axis=1)/nx
        if max(ze) > 0.0:
            ax.plot(ze, label=r'$R(T_e)$')
        zi = np.sum(sim.data['E(eflux_i)'][:, 1:], axis=1)/nx
        if max(zi) > 0.0:
            ax.plot(zi, label=r'$R(T_i)$')
        ne = np.sum(sim.data['E(pflux_e)'][:, 1:], axis=1)/nx
        if max(ne) > 0.0:
            ax.plot(ne, label=r'$R(n_e)$')
        ax.set_ylabel('$\mathbf{residual}$')
        ax.set_xlabel('$\mathbf{iteration}$')
        ax.set_xlim([0, nit])
        ax.set_ylim([1e-3, 5e0])
        ax.legend(loc=loc)
    else:
        if tag == 'res_te':
            z = sim.data['E(eflux_e)'][:, 1:]
            ax.set_ylabel('$\mathrm{Residual}(T_e)$', color='k')
        elif tag == 'res_ti':
            z = sim.data['E(eflux_i)'][:, 1:]
            ax.set_ylabel('$\mathrm{Residual}(T_i)$', color='k')
        elif tag == 'res_ne':
            z = sim.data['E(pflux_e)'][:, 1:]
            ax.set_ylabel('$\mathrm{Residual}(n_e)$', color='k')

        c = ax.pcolor(z,
                      edgecolors='w',
                      linewidths=1,
                      norm=LogNorm(vmin=1e-3, vmax=1.0),
                      cmap='rainbow')
        plt.colorbar(c, ax=ax)
        ax.set_xlabel('$r/a$')
        ax.set_ylabel('$\mathbf{iteration}$')

    plt.tight_layout


def plot_flux(ax, tag):

    # Fluxes

    ax.grid(which="major", ls="-", alpha=0.1, linewidth=2)
    ax.grid(which="minor", ls=":", alpha=0.1, linewidth=2)
    ax.set_xlabel('$r/a$')

    tot = r'$\mathbf{total}$'
    tar = r'$\mathbf{target}$'

    if tag == 'eflux_e_target':
        if units == 0:
            ax.plot(x, sim.data['eflux_e_tot'][n], label=tot)
            ax.plot(x, sim.data['eflux_e_target'][n], label=tar)
            ax.set_ylabel('$Q_e/Q_{GB}$', color='k')
        else:
            ax.plot(x, sim.data['eflux_e_tot'][n]*qgb, label=tot)
            ax.plot(x, sim.data['eflux_e_target'][n]*qgb, label=tar)
            ax.set_ylabel('$Q_e [MW/m^2]$', color='k')
    elif tag == 'eflux_i_target':
        if units == 0:
            ax.plot(x, sim.data['eflux_i_tot'][n], label=tot)
            ax.plot(x, sim.data['eflux_i_target'][n], label=tar)
            ax.set_ylabel('$Q_i/Q_{GB}$', color='k')
        else:
            ax.plot(x, sim.data['eflux_i_tot'][n]*qgb, label=tot)
            ax.plot(x, sim.data['eflux_i_target'][n]*qgb, label=tar)
            ax.set_ylabel('$Q_i~[MW/m^2]$', color='k')
    elif tag == 'pflux_e_target':
        if units == 0:
            ax.plot(x, sim.data['pflux_e_tot'][n], label=tot)
            ax.plot(x, sim.data['pflux_e_target'][n], label=tar)
            ax.set_ylabel('$\Gamma_e/\Gamma_{GB}$', color='k')
            if max(abs(sim.data['pflux_e_tot'][n])) < 0.1:
                ax.set_ylim([-0.1, 0.1])
        else:
            ax.plot(x, sim.data['pflux_e_tot'][n]*ggb, label=tot)
            ax.plot(x, sim.data['pflux_e_target'][n]*ggb, label=tar)
            ax.set_ylabel('$\Gamma_e~[10^{19}/m^2/s]$', color='k')
    elif tag == 'mflux_target':
        ax.plot(x, sim.data['mflux_tot'][n], label=tot)
        ax.plot(x, sim.data['mflux_target'][n], label=tar)
        ax.set_ylabel('$\Pi/\Pi_{GB}$', color='k')

    for i in range(n_ion):
        pstr = 'pflux_i'+str(i+1)
        if tag == pstr+'_target':
            if units == 0:
                ax.plot(x, sim.data[pstr+'_tot'][n], label=tot)
                ax.plot(x, sim.data[pstr+'_target'][n], label=tar)
                ax.set_ylabel('$\Gamma_{i'+str(i+1)+'}/\Gamma_{GB}$',
                              color='k')
            else:
                ax.plot(x, sim.data[pstr+'_tot'][n]*ggb, label=tot)
                ax.plot(x, sim.data[pstr+'_target'][n]*ggb, label=tar)
                ax.set_ylabel('$\Gamma_{i'+str(i+1)+'}~[10^{19}/m^2/s]$',
                              color='k')
            break

    ax.legend(loc=loc)
    plt.tight_layout


def plot_smooth(ax, tag):

    # Smooth curves

    ax.grid(which="major", ls="-", alpha=0.1, linewidth=2)
    ax.grid(which="minor", ls=":", alpha=0.1, linewidth=2)
    ax.set_xlabel('$r/a$')

    if tag == 'te':
        xf, pf = smooth_pro(x, sim.data['a/Lte'][0], sim.data['te'][0], 64)
        ax.plot(xf, pf, color='black', label=init)
        xf, pf = smooth_pro(x, sim.data['a/Lte'][n], sim.data['te'][n], 64)
        ax.plot(xf, pf, color='magenta', label=fin)
        ax.set_ylabel(r'$\mathrm{T_e~[keV]}$')
        # Dots
        ax.plot(x, sim.data['te'][0], 'o', color='k')
        ax.plot(x, sim.data['te'][n], 'o', color='k')
        plot_input_profiles(ax, 'Te')
    elif tag == 'ti':
        xf, pf = smooth_pro(x, sim.data['a/Lti1'][0], sim.data['ti1'][0], 64)
        ax.plot(xf, pf, color='black', label=init)
        xf, pf = smooth_pro(x, sim.data['a/Lti1'][n], sim.data['ti1'][n], 64)
        ax.plot(xf, pf, color='magenta', label=fin)
        ax.set_ylabel(r'$\mathrm{T_i~[keV]}$')
        # Dots
        ax.plot(x, sim.data['ti1'][0], 'o', color='k')
        ax.plot(x, sim.data['ti1'][n], 'o', color='k')
        plot_input_profiles(ax, 'Ti_1')
    elif tag == 'ne':
        xf, pf = smooth_pro(x, sim.data['a/Lne'][0], sim.data['ne'][0], 64)
        ax.plot(xf, pf/1e13, color='black', label=init)
        xf, pf = smooth_pro(x, sim.data['a/Lne'][n], sim.data['ne'][n], 64)
        ax.plot(xf, pf/1e13, color='magenta', label=fin)
        ax.set_ylabel(r'$\mathrm{n_e~[10^{19}/m^3]}$')
        # Dots
        ax.plot(x, sim.data['ne'][0]/1e13, 'o', color='k')
        ax.plot(x, sim.data['ne'][n]/1e13, 'o', color='k')
        plot_input_profiles(ax, 'ne')

    for i in range(n_ion):
        if tag == 'ni'+str(i+1):
            xf, pf = smooth_pro(x, sim.data['a/L'+tag][0], sim.data[tag][0],
                                64)
            ax.plot(xf, pf/1e13, color='black', label=init)
            xf, pf = smooth_pro(x, sim.data['a/L'+tag][n], sim.data[tag][n],
                                64)
            ax.plot(xf, pf/1e13, color='magenta', label=fin)
            ax.set_ylabel(r'$\mathrm{n_i~[10^{19}/m^3]}$')
            # Dots
            ax.plot(x, sim.data[tag][0]/1e13, 'o', color='k')
            ax.plot(x, sim.data[tag][n]/1e13, 'o', color='k')
            plot_input_profiles(ax, 'ni_'+str(i+1))
            break

    ax.legend(loc=loc)
    plt.tight_layout


#-------------------------------------------------------------------------------------


class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.figure = plt.Figure()
        self.figure.subplots_adjust(left=0.07, right=0.95)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self, tag):
        plot_select(self.ax, tag)


#-------------------------------------------------------------------------------------


class DemoFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          'TGYRO plotting notebook -- '+wdir,
                          size=(1100, 600))
        panel = wx.Panel(self)

        notebook = wx.Notebook(panel)

        tab = TabPanel(notebook)
        tab.draw('eflux_e_target')
        notebook.AddPage(tab, '*eflux_e')

        tab = TabPanel(notebook)
        tab.draw('eflux_i_target')
        notebook.AddPage(tab, '*eflux_i')

        tab = TabPanel(notebook)
        tab.draw('pflux_e_target')
        notebook.AddPage(tab, '*pflux_e')

        tab = TabPanel(notebook)
        tab.draw('mflux_target')
        notebook.AddPage(tab, '*mflux')

        for i in range(n_ion):
            tab = TabPanel(notebook)
            tab.draw('pflux_i'+str(i+1)+'_target')
            notebook.AddPage(tab, '*pflux_i'+str(i+1))

        tab = TabPanel(notebook)
        tab.draw('te')
        notebook.AddPage(tab, 'Te')

        tab = TabPanel(notebook)
        tab.draw('ti')
        notebook.AddPage(tab, 'Ti')

        tab = TabPanel(notebook)
        tab.draw('ne')
        notebook.AddPage(tab, 'ne')

        for i in range(n_ion):
            tab = TabPanel(notebook)
            tab.draw('ni'+str(i+1))
            notebook.AddPage(tab, 'ni'+str(i+1))

        tab = TabPanel(notebook)
        tab.draw('zte')
        notebook.AddPage(tab, 'zTe')

        tab = TabPanel(notebook)
        tab.draw('zti')
        notebook.AddPage(tab, 'zTi')

        tab = TabPanel(notebook)
        tab.draw('zne')
        notebook.AddPage(tab, 'zne')

        tab = TabPanel(notebook)
        tab.draw('res_te')
        notebook.AddPage(tab, 'R(Te)')

        tab = TabPanel(notebook)
        tab.draw('res_ti')
        notebook.AddPage(tab, 'R(Ti)')

        tab = TabPanel(notebook)
        tab.draw('res_ne')
        notebook.AddPage(tab, 'R(ne)')

        tab = TabPanel(notebook)
        tab.draw('res_tot')
        notebook.AddPage(tab, 'Rtot')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()


#-------------------------------------------------------------------------------------

if __name__ == "__main__":

    if ext == 'screen':

        # On-screen wxpython notebook

        app = wx.App(False)
        frame = DemoFrame()
        app.MainLoop()

    else:

        # Generate plots

        list = ['eflux_e_target', 'eflux_i_target', 'pflux_e_target']
        for i in range(n_ion):
            list.append('pflux_i'+str(i+1)+'_target')
        list = list+['te', 'ti', 'ne']
        for i in range(n_ion):
            list.append('ni'+str(i+1)+'_target')
        list = list+['zte', 'zti', 'zne']

        for xlist in list:
            figure = plt.figure(figsize=(9, 6))
            figure.subplots_adjust(left=0.12, right=0.95, bottom=0.16)
            ax = figure.add_subplot(111)
            plot_select(ax, xlist)
            pfile = 'out.'+xlist+'.'+ext
            plt.savefig(pfile)
            print('INFO: (notebook.py) Wrote '+pfile)
