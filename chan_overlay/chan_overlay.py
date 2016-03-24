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
    import shapefile as shp

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 8
    rcParams['xtick.direction'] = 'out'
    rcParams['ytick.direction'] = 'out'

    fig = plt.figure()

    labels = list(string.ascii_lowercase)[:6]
    Res = ['1', '5', '10', '20', '30']
    prefix = [''] + ['sc', 'gm', 'or'] * 2
    method = [''] + ['d'] * 3 + ['p'] * 3
    colors = ['b', 'limegreen', 'r', 'y', 'm']

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
        xll = hillshade_header[2]
        yll = hillshade_header[3]

        # plot the hillshade on the axes
        plt.imshow(hillshade, vmin=0, vmax=255, cmap=cmx.gray)

        for g, r in enumerate(Res):

            # load channels
            data_path = '/home/s0675405/Resolution_Paper_Figs/chan_overlay/shapefiles/'
            sf = shp.Reader(data_path + prefix[i] + '_' + Res[g]
                            + '_' + method[i] + '_clip.shp')

            for shape in sf.shapes():
                x = []
                y = []
                for point in shape.points:
                    x.append(point[0] - xll)
                    y.append((-1 * point[1]) + yll + hillshade_header[1])
                plt.plot(x, y, c=colors[g], linewidth=0.75)

        # now get the tick marks
        n_target_tics = 4
        xlocs, ylocs, new_x_labels, new_y_labels = UTM(hillshade_header,
                                                       x_max, x_min, y_max,
                                                       y_min, n_target_tics)

        new_x_labels = ['$' + x + '$' for x in new_x_labels]
        new_y_labels = ['$' + y + '$' for y in new_y_labels]

        # place axis ticks around the outside of each plot
        if (i == 1):  # top left
            ax.xaxis.tick_top()
            plt.tick_params(axis='x', which='both', bottom='off', length=2,
                            pad=0)
            plt.tick_params(axis='y', which='both', right='off', length=2,
                            pad=0)
            plt.yticks(ylocs, new_y_labels)
            plt.xticks(xlocs, new_x_labels, rotation=0)
            plt.xlabel('Santa Cruz Island', fontsize=10)
            ax.xaxis.set_label_position("top")
            # ax.xaxis.labelpad = 15
        if (i == 2):  # middle top
            ax.xaxis.tick_top()
            plt.tick_params(axis='x', which='both', bottom='off', length=2,
                            pad=0)
            plt.tick_params(axis='y', which='both', left='off', right='off',
                            length=2)
            ax.axes.get_yaxis().set_ticklabels([])
            plt.xticks(xlocs, new_x_labels, rotation=0)
            plt.xlabel('Gabilan Mesa', fontsize=10)
            ax.xaxis.set_label_position("top")
        if (i == 3):  # top right
            ax.xaxis.tick_top()
            ax.yaxis.tick_right()
            plt.tick_params(axis='x', which='both', bottom='off', length=2,
                            pad=0)
            plt.tick_params(axis='y', which='both', left='off', length=2, pad=0)
            plt.xticks(xlocs, new_x_labels, rotation=0)
            plt.ylabel('DrEICH method', fontsize=10)
            ax.yaxis.set_label_position("right")
            ax.axes.get_yaxis().set_ticklabels([])
            plt.xlabel('Oregon Coast Range', fontsize=10)
            ax.xaxis.set_label_position("top")
        if (i == 4):  # bottom left
            plt.tick_params(axis='x', which='both', top='off', length=2)
            plt.tick_params(axis='y', which='both', right='off', length=2,
                            pad=0)
            # create an invisible label to pad for the real label later on
            plt.ylabel('Northing ($m$)', size=10, color='white')

            plt.yticks(ylocs, new_y_labels)
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
            ax.axes.get_yaxis().set_ticklabels([])
            plt.ylabel('Geometric method', fontsize=10)
            ax.yaxis.set_label_position("right")

            # make fake data for our legend
            for v in range(5):
                plt.plot((1, 1), (1, 2), c=colors[v], label=Res[v] + ' m')

            legend = plt.legend(bbox_to_anchor=(1.1, 0), fontsize=8, ncol=3)
            legend.get_frame().set_linewidth(0.)

        plt.annotate(labels[i - 1], xy=(0.92, 0.96), backgroundcolor='white',
                     xycoords='axes fraction', fontsize=10,
                     horizontalalignment='left', verticalalignment='top')

        x_center = int(x_max / 2.)
        y_center = int(y_max / 2.)

        spacing = 900

        plt.xlim(x_center - spacing, x_center + spacing)
        plt.ylim(y_center + spacing, y_center - spacing)

    fig.text(0.025, 0.5, 'Northing ($m$)', ha='center', va='center',
             rotation='vertical', size=10)

    plt.tight_layout()
    fig.subplots_adjust(hspace=0.002, wspace=0.08, bottom=0.095, top=0.915)

    # quarter page = 95*115
    # half page = 190*115 (horizontal) 95*230 (vertical)
    # full page = 190*230
    fig.set_size_inches(mm_to_inch(190), mm_to_inch(130))

    plt.savefig('/home/s0675405/Resolution_Paper_Figs/chan_overlay/Chan_over.png',
                dpi=500)


def Make_The_Figure():
    """
    All filenames and paths to data are modifed here in this wrapper
    """
    path = '/home/s0675405/Resolution_Paper_Figs/chan_overlay/hs/'
    Hillshade_files = ['sc_hs.flt', 'gm_hs.flt', 'or_hs.flt'] * 2

    Hillshade_files = [path + f for f in Hillshade_files]

    Process(Hillshade_files)


Make_The_Figure()
