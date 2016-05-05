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

Locations = {'GM': 'Gabilan Mesa', 'SC': 'Santa Cruz\nIsland',
             'OR': 'Oregon Coast\nRange'}


def mm_to_inch(mm):
    return mm * 0.0393700787


def LoadCurvData(Prefix, CurvType, InPath):
    """
    Load the data into a 2d array with the column format:

    X_coord, PC2, PC25, Median, Mean, PC75, PC98, Minimum, Maximum
    """

    if CurvType:
        name = '_CurvatureResData_' + str(CurvType) + '.txt'
    else:
        name = '_ChtResData.txt'

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

    if CurvType:
        name = '_' + str(Res) + '_Hist_' + str(CurvType) + '.txt'
    else:
        name = '_' + str(Res) + '_Hist_CHT.txt'

    filename = Path + Prefix + name
    data = np.genfromtxt(filename, delimiter=' ', skip_header=1)

    pdfs = data[:, 4]
    bin_centers = data[:, 0]

    return pdfs, bin_centers

Resolutions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

labels = [''] + list(string.ascii_lowercase)[:6]

colors = ['b', 'k', 'r']
pdf_expand = [[2.25, 1.6], [1.25, 1.], [3.75, 2.]]

Path = '/home/s0675405/Resolution_Paper_Figs/curve_data/'
CurvType = 6

TitlePad = [0.025, 0, 0]

SubplotLocations = [[1, 2], [3, 4], [5, 6]]

fig = plt.figure()

for i, q in enumerate(['SC', 'GM', 'OR']):

    for j, w in enumerate([3, 6]):

        CurvData = LoadCurvData(q, w, Path)

        Curvs = np.array(CurvData[3])
        Curvs_low = Curvs - np.array(CurvData[2])
        Curvs_high = np.array(CurvData[5]) - Curvs

        ax = plt.subplot(3, 2, SubplotLocations[i][j])

        if (SubplotLocations[i][j] % 2 == 0):
            ax.text(11.25, 0 + TitlePad[i], Locations[q], ha='center',
                    va='center', rotation='vertical', size=12)

        plt.annotate(labels[SubplotLocations[i][j]], xy=(0.96, 0.98),
                     xycoords='axes fraction', fontsize=12,
                     horizontalalignment='left', verticalalignment='top')

        BoxPlotter.BoxPlot(CurvData[1], CurvData[2], CurvData[3],
                           CurvData[4], CurvData[5], CurvData[6],
                           CurvData[0], 0.2)

        LowWhisk = CurvData[1]
        HighWhisk = CurvData[6]
        plt.ylim(np.min(LowWhisk) * 1.05, np.max(HighWhisk) * 1.05)

        for a in range(1, 11):
            pdfs, bin_centers = LoadPDF(Path, q, w, a)
            pdfs = pdfs * pdf_expand[i][j]

            plt.plot(pdfs + a, bin_centers, color='k', linewidth=0.3)
            plt.plot((pdfs * -1.) + a, bin_centers, color='k', linewidth=0.3)

        plt.tick_params(axis='x', which='both', top='off', length=2)
        plt.tick_params(axis='y', which='both', right='off', length=2)

        if q is not 'OR':
            ax.xaxis.set_visible(False)

        if q is 'SC' and j:
            plt.title('$C_{Tan}$')

        if q is 'SC' and not j:
            plt.title('$C_{Total}$')

        if (SubplotLocations[i][j] == 6):
            legend = plt.legend(loc=4)
            legend.get_frame().set_linewidth(0.)

        plt.xlim(0.5, 10.5)

# x and y axis labels
fig.text(0.5, 0.03, 'Grid resolution ($m$)', ha='center', va='center', size=12)
fig.text(0.03, 0.5, 'Curvature ($m^{-1}$)', ha='center', va='center',
         rotation='vertical', size=12)

plt.tight_layout()
fig.subplots_adjust(hspace=0.05, left=0.12, right=0.94, bottom=0.074)

# set the size of the plot to be saved. These are the JGR sizes:
# quarter page = 95*115
# half page = 190*115 (horizontal) 95*230 (vertical)
# full page = 190*230
fig.set_size_inches(mm_to_inch(190), mm_to_inch(230))


plt.savefig('curve_fig/curv_fig.png', dpi=500)
