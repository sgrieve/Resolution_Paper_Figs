import numpy as np
import matplotlib.pyplot as plt
import string
from matplotlib import rcParams
import BoxPlotter

# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 10
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

Locations = {'GM': 'Gabilan Mesa', 'SC': 'Santa Cruz Island',
             'OR': 'Oregon Coast Range'}


def mm_to_inch(mm):
    return mm * 0.0393700787


def LoadCurvData(Prefix, CurvType, InPath):
    """
    Load the data into a 2d array with the column format:

    X_coord, PC2, PC25, Median, Mean, PC75, PC98, Minimum, Maximum
    """
    if (CurvType[:2] == 'LH'):
        name = '_LHResData_new_fix.txt'
        if (len(CurvType) > 2):
            name = name.split('.')[0] + '_variable.txt'
    elif (CurvType[:1] == 'R'):
        name = '_RResData_new_fix.txt'
        if (len(CurvType) > 1):
            name = name.split('.')[0] + '_variable.txt'
    else:
        name = ''

    with open(InPath + Prefix + name, 'r') as f:
        f.readline()
        data = f.readlines()

    no_of_lines = len(data)
    no_of_cols = len(data[0].split())

    Data = np.zeros((no_of_cols, no_of_lines), dtype='float64')

    for i, r in enumerate(data):
        split = r.split()
        for a in range(no_of_cols):
            Data[a][i] = split[a]

    return Data


def LoadPDF(Path, Prefix, CurvType, Res):

    if (CurvType[:2] == 'LH'):
        name = '_Hist_LH_' + str(Res) + '_tues.txt'
        if (len(CurvType) > 2):
            name = name.split('.')[0] + '_variable.txt'
    elif (CurvType[:1] == 'R'):
        name = '_Hist_R_' + str(Res) + '_tues.txt'
        if (len(CurvType) > 1):
            name = name.split('.')[0] + '_variable.txt'
    else:
        name = ''

    filename = Path + Prefix + name
    data = np.genfromtxt(filename, delimiter=' ', skip_header=1)

    pdfs = data[:, 4]
    bin_centers = data[:, 0]

    return pdfs, bin_centers

Resolutions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

labels = list(string.ascii_lowercase)[:4]

ylim_l = [300, 375, 300]
ylim_r = [150, 135, 160]

pdf_expand = [[2.25, 1.6], [1.25, 1.], [3.75, 2.]]

pdf_expand_LH = [2.8, 5., 2.8]
pdf_expand_R = [1.5, 1.9, 2.3]

Path = '/home/s0675405/Len_Figs/lh_r_data/'
CurvType = 6

TitlePad = [0.025, 0, 0]

SubplotLocations = [[1, 2], [3, 4], [5, 6]]

fig = plt.figure()

for i, q in enumerate(['SC', 'GM', 'OR']):

    for j, w in enumerate(['LH', 'R', 'LH_variable', 'R_variable']):

        CurvData = LoadCurvData(q, w, Path)

        Curvs = np.array(CurvData[3])
        Curvs_low = Curvs - np.array(CurvData[2])
        Curvs_high = np.array(CurvData[5]) - Curvs

        ax = plt.subplot(2, 2, j + 1)

        plt.annotate(labels[j], xy=(0.92, 0.98),
                     xycoords='axes fraction', fontsize=12,
                     horizontalalignment='left', verticalalignment='top')

        BoxPlotter.BoxPlot(CurvData[1], CurvData[2], CurvData[3],
                           CurvData[4], CurvData[5], CurvData[6],
                           CurvData[0], 0.4)

        LowWhisk = CurvData[1]
        HighWhisk = CurvData[6]
        plt.ylim(np.min(LowWhisk) * 1.05, np.max(HighWhisk) * 1.05)

        for a in range(1, 11) + range(12, 31, 2):
            pdfs, bin_centers = LoadPDF(Path, q, w, a)

            if (w[:2] == 'LH'):
                pdfs = pdfs * pdf_expand_LH[i]

            if (w[0] == 'R'):
                pdfs = pdfs * pdf_expand_R[i]

            plt.plot(pdfs + a, bin_centers, color='k', linewidth=0.3)
            plt.plot((pdfs * -1.) + a, bin_centers, color='k', linewidth=0.3)

        if (j < 2):
            ax.axes.get_xaxis().set_ticklabels([])

        if (j == 3):
            legend = plt.legend(loc=4, fontsize=8)
            legend.get_frame().set_linewidth(0.)
            ax.text(34, ylim_r[i] / 2., 'Variable channel\nheads', ha='center',
                    va='center', rotation='vertical', size=10)

        if (j == 1):
            ax.text(34, ylim_r[i] / 2., '1m channel\nheads', ha='center',
                    va='center', rotation='vertical', size=10)

        plt.tick_params(axis='x', which='both', top='off', length=2)
        plt.tick_params(axis='y', which='both', right='off', length=2)

        if (j % 2):
            plt.ylim(0, ylim_r[i])
        else:
            plt.ylim(0, ylim_l[i])

        plt.xlim(0.5, 31)

    # x and y axis labels
    fig.text(0.5, 0.03, 'Grid resolution ($m$)', ha='center', va='center',
             size=12)
    fig.text(0.04, 0.5, 'Hillslope length ($m$)', ha='center', va='center',
             rotation='vertical', size=12)
    fig.text(0.51, 0.5, 'Relief ($m$)', ha='center', va='center',
             rotation='vertical', size=12)

    plt.suptitle(Locations[q], y=0.96)

    fig.subplots_adjust(wspace=0.35, bottom=0.125)

    # set the size of the plot to be saved. These are the JGR sizes:
    # quarter page = 95*115
    # half page = 190*115 (horizontal) 95*230 (vertical)
    # full page = 190*230
    fig.set_size_inches(mm_to_inch(190), mm_to_inch(115))

    plt.savefig('lh_r/' + q + '_LH_R.png', dpi=500)
    plt.clf()
