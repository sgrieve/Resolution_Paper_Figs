# -*- coding: utf-8 -*-


def mm_to_inch(mm):
    return mm * 0.0393700787


def Process(files):

    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.cm as cmx
    from matplotlib import rcParams
    import raster_plotter_simple as raster
    from raster_plotter_simple import format_ticks_for_UTM_imshow as UTM
    import string

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 8
    rcParams['xtick.direction'] = 'out'
    rcParams['ytick.direction'] = 'out'

    fig = plt.figure()

    labels = list(string.ascii_lowercase)[:6]

    Res = [1, 2, 5, 10, 20, 30]

    for i in range(1, 7):

        ax = plt.subplot(2, 3, i)

        # get data
        hillshade, hillshade_header = raster.read_flt(files[i - 1])

        # ignore nodata values
        hillshade = np.ma.masked_where(hillshade == -9999, hillshade)

        x_max = hillshade_header[0]
        x_min = 0
        y_max = hillshade_header[1]
        y_min = 0

        # plot the hillshade on the axes
        plt.imshow(hillshade, vmin=0, vmax=255, cmap=cmx.gray)

        xmin = 1034 / Res[i - 1]
        xmax = 1198 / Res[i - 1]
        ymin = 2080 / Res[i - 1]
        ymax = 1920 / Res[i - 1]

        plt.plot((xmin, xmax), (ymin, ymin), 'r-')
        plt.plot((xmin, xmax), (ymax, ymax), 'r-')

        plt.plot((xmin, xmin), (ymin, ymax), 'r-')
        plt.plot((xmax, xmax), (ymin, ymax), 'r-')

        # now get the tick marks
        n_target_tics = 4
        xlocs, ylocs, new_x_labels, new_y_labels = UTM(hillshade_header,
                                                       x_max, x_min, y_max,
                                                       y_min, n_target_tics)

        '''
        plt.rc('text', usetex=True)

        new_x_labels = [r'{\fontsize{12pt}{3em}\selectfont{}' + x[:-3] + r'}{\fontsize{8pt}{3em}\selectfont{}' + x[-3:] for x in new_x_labels]
        new_y_labels = [r'{\fontsize{12pt}{3em}\selectfont{}' + y[:-3] + r'}{\fontsize{8pt}{3em}\selectfont{}' + y[-3:] for y in new_y_labels]
        '''

        new_x_labels = ['$' + x + '$' for x in new_x_labels]
        new_y_labels = ['$' + y + '$' for y in new_y_labels]

        # place axis ticks around the outside of each plot
        if (i == 1):  # top left
            ax.xaxis.tick_top()
            plt.tick_params(axis='x', which='both', bottom='off', length=2,
                            pad=0)
            plt.tick_params(axis='y', which='both', right='off', length=2,
                            pad=0)
            ax.axes.get_yaxis().set_ticklabels([])
            plt.xticks(xlocs, new_x_labels, rotation=0)
        if (i == 2):  # middle top
            ax.xaxis.tick_top()
            plt.tick_params(axis='x', which='both', bottom='off', length=2,
                            pad=0)
            plt.tick_params(axis='y', which='both', left='off', right='off',
                            length=2)
            ax.axes.get_yaxis().set_ticklabels([])
            plt.xticks(xlocs, new_x_labels, rotation=0)
        if (i == 3):  # top right
            ax.xaxis.tick_top()
            ax.yaxis.tick_right()
            plt.tick_params(axis='x', which='both', bottom='off', length=2,
                            pad=0)
            plt.tick_params(axis='y', which='both', left='off', length=2, pad=0)
            plt.xticks(xlocs, new_x_labels, rotation=0)
            plt.yticks(ylocs, new_y_labels)
        if (i == 4):  # bottom left
            plt.tick_params(axis='x', which='both', top='off', length=2)
            plt.tick_params(axis='y', which='both', right='off', length=2)
            # create an invisible label to pad for the real label later on
            plt.ylabel('Northing ($m$)', size=10, color='white')
            ax.yaxis.labelpad = 10
            ax.axes.get_yaxis().set_ticklabels([])
            ax.axes.get_xaxis().set_ticklabels([])
        if (i == 5):  # bottom middle
            plt.tick_params(axis='x', which='both', top='off', length=2)
            plt.tick_params(axis='y', which='both', left='off', right='off',
                            length=2)
            ax.axes.get_yaxis().set_ticklabels([])
            ax.axes.get_xaxis().set_ticklabels([])
            plt.xlabel('Easting ($m$)', fontsize=10)
        if (i == 6):  # bottom right
            ax.yaxis.tick_right()
            plt.tick_params(axis='x', which='both', top='off', length=2)
            plt.tick_params(axis='y', which='both', left='off', length=2, pad=0)
            ax.axes.get_xaxis().set_ticklabels([])
            plt.yticks(ylocs, new_y_labels)

        plt.annotate(labels[i - 1], xy=(0.92, 0.96), backgroundcolor='white',
                     xycoords='axes fraction', fontsize=10,
                     horizontalalignment='left', verticalalignment='top')

        x_center = int(x_max / 2.)
        y_center = int(y_max / 2.)

        spacing = 1000 / Res[i - 1]

        plt.xlim(x_center - spacing, x_center + spacing)
        plt.ylim(y_center + spacing, y_center - spacing)

    fig.text(0.025, 0.5, 'Northing ($m$)', ha='center', va='center',
             rotation='vertical', size=10)

    plt.tight_layout()

    fig.subplots_adjust(hspace=0.002, wspace=0.08, bottom=0.075, top=0.95)

    # quarter page = 95*115
    # half page = 190*115 (horizontal) 95*230 (vertical)
    # full page = 190*230
    fig.set_size_inches(mm_to_inch(178), mm_to_inch(120))

    plt.savefig('/home/s0675405/Resolution_Paper_Figs/hillshade_fig/HS_fig.png',
                dpi=500)


def Make_The_Figure():
    """
    All filenames and paths to data are modifed here in this wrapper
    """
    path = '/home/s0675405/Resolution_Paper_Figs/hillshade_fig/'
    Hillshade_files = ['sc1.flt', 'sc2.flt', 'sc5.flt', 'sc10.flt', 'sc20.flt',
                       'sc30.flt']

    Hillshade_files = [path + f for f in Hillshade_files]

    Process(Hillshade_files)


Make_The_Figure()
