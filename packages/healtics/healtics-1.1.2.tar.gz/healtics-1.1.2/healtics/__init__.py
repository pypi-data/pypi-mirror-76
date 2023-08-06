from healtics.setup_matplotlib import *
import healpy as hp
import scipy
import scipy.stats
import numpy as np

from matplotlib.projections.geo import GeoAxes

import matplotlib.pylab as plt

class ThetaFormatterShiftPi(GeoAxes.ThetaFormatter):
    """Shifts labelling by pi

    Shifts labelling from -180,180 to 0-360"""
    extrapi=False

    def __init__(self,*a,**aa):
        if 'extrapi' in aa:
            self.extrapi=aa['extrapi']
        del aa['extrapi']
        super(ThetaFormatterShiftPi,self).__init__(*a,**aa)

    def __call__(self, x, pos=None):
        if self.extrapi:
            x+=np.pi
        if x != 0:
            x *= -1
        if x < 0:
            x += 2*np.pi
        return GeoAxes.ThetaFormatter.__call__(self, x, pos)

#def plot_with_ticks(m,vmin=0,vmax=None,cmap="YlOrBr",cmap2="bone",unit="$erg cm^{-2} s^{-1}$",title="",overplot=None):
def plot_with_ticks(m,vmin=0,vmax=None,cmap="YlOrBr",unit="$10^{-7} \mathrm{erg^{}cm^{-2} s^{-1}}$",title="",overplot=[],ilevels=None,ovmin=0.1,ovmax=1,points=[],invra=False,colorbar=True,fig=None,tickfontsize=10):
    if vmax is None:
        vmax=m.max()    

    xsize = 2000
    ysize = int(xsize/2.)
    nside=hp.npix2nside(m.shape[0])
    
    theta = np.linspace(np.pi, 0, ysize)

    if invra:
        phi   = np.linspace(0, 2*np.pi, xsize)
    else:
        phi   = np.linspace(-np.pi, np.pi, xsize)
    longitude = np.radians(np.linspace(-180, 180, xsize))
    latitude = np.radians(np.linspace(-90, 90, ysize))

    # project the map to a rectangular matrix xsize x ysize
    PHI, THETA = np.meshgrid(phi, theta)
    grid_pix = hp.ang2pix(nside, THETA, PHI)
    grid_map = m[grid_pix]


    width=18
# for width in [ 8.8]:
# for width in [18., 12., 8.8]:

    if fig is None:
        fig = plt.figure(figsize=(cm2inch(width), cm2inch(width)/(3./2.)))
    fig.suptitle(title)
    # matplotlib is doing the mollveide projection
    ax = fig.add_subplot(111,projection='mollweide')
    

    # rasterized makes the map bitmap while the labels remain vectorial
    # flip longitude to the astro convention
    image = plt.pcolormesh(longitude[::-1], latitude, grid_map, vmin=vmin, vmax=vmax, rasterized=True, cmap=cmap)

    print("to overplot",len(overplot))
    print("to overplot",overplot)

    for op_set in overplot[0]:
        print("op set",op_set)

        thickness = None
        ls = None

        if len(op_set)==3:
            op,cmapop,onelevel=op_set

        if len(op_set)==4:
            op,cmapop,onelevel,thickness=op_set

        if len(op_set)==5:
            op,cmapop,onelevel,thickness,ls=op_set


        grid_map_op=hp.get_interp_val(op,THETA,PHI)
        print("overplotting",grid_map_op)



        if onelevel is None:
            indices = np.argsort(-grid_map_op)
            region = np.empty(grid_map_op.shape)
            n[indices] = 100 * np.cumsum(grid_map[indices])

            levels=[50,90]

        else:
            try:
                #levels=[l*op.min() for l in onelevel]
                levels=[l for l in onelevel]
            except:
                levels=[onelevel]


        levels=sorted(levels)

        print("levels:",levels)

        if ilevels is not None:
            levels=ilevels
            ovmin=levels.min()
            ovmax=levels.max()

        levels=sorted(levels)

        
        if isinstance(ls,tuple):
            CS=plt.contourf(longitude[::-1], latitude, grid_map_op, colors=cmapop,levels=levels, hatches=['', '/'],extend='both',alpha=0)
        else:
            CS=plt.contour(longitude[::-1], latitude, grid_map_op, colors=cmapop,levels=levels, linestyles=ls)
            if thickness is not None:
                plt.setp(CS.collections, linewidth=thickness)


        #plt.contour(longitude[::-1], latitude, grid_map_op, vmin=ovmin, vmax=ovmax, rasterized=True, cmap=cmapop,levels=levels)
        #image2 = plt.pcolormesh(longitude[::-1], latitude, grid_map, vmin=0.1, vmax=1., rasterized=True, cmap=cmap,alpha=0.3)


        # project the map to a rectangular matrix xsize x ysize
        

    # graticule
    lon_g=ax.set_longitude_grid(60)
    ax.xaxis.set_major_formatter(ThetaFormatterShiftPi(60,extrapi=invra))
    if width < 10:
        lat_g=ax.set_latitude_grid(45)
        lon_g=ax.set_longitude_grid_ends(90)

    for g in ax.xaxis.get_gridlines()+ax.yaxis.get_gridlines():
        g.set_linestyle("dotted")
        g.set_color("black")
        g.set_alpha(0.5)


    # colorbar
    if colorbar:
        cb = fig.colorbar(image, orientation='horizontal', shrink=.6, pad=0.05, ticks=[vmin, vmax])
        cb.ax.xaxis.set_label_text(unit)
        cb.ax.xaxis.labelpad = -8
        # workaround for issue with viewers, see colorbar docstring
        cb.solids.set_edgecolor("face")

    ax.tick_params(axis='x', labelsize=tickfontsize)
    ax.tick_params(axis='y', labelsize=tickfontsize)

    # remove tick labels
#    ax.xaxis.set_ticklabels([])
 #   ax.yaxis.set_ticklabels([])
    # remove grid
  #  ax.xaxis.set_ticks([])
    #ax.yaxis.set_ticks([])

     #remove white space around figure
    spacing = 0.05
    plt.subplots_adjust(bottom=spacing, top=1-spacing, left=spacing, right=1-spacing)

    plt.grid(True)
    return fig,plt

