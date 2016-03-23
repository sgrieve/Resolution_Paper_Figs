import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 14
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'


def mm_to_inch(mm):
    return mm * 0.0393700787


def LoadData(Prefix, InPath):
    """
    Load the data into a 2d array with the column format:

    X_coord, PC2, PC25, Median, Mean, PC75, PC98, Minimum, Maximum
    """

    with open(InPath + Prefix + '_ChtResData_noscaling.txt', 'r') as f:
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

Resolutions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

from uncertainties import unumpy as unp

Locations = {'GM': 'Gabilan Mesa', 'SC': 'Santa Cruz Island',
             'OR': 'Oregon Coast Range'}

Es = [0.000076, 0.00044, 0.0001]
Es_no_errs = [0.000076, 0.00036, 0.0001]

EsHi = [0.000083, 0.00074, 0.00015]
EsLo = [0.000069, 0.00014, 0.00005]

Errs = [0.000007, 0.0003, 0.00005]

Es_uncert = unp.uarray(Es, Errs)

colors = ['b', 'k', 'r']

fig = plt.figure()

for i, q in enumerate(['SC', 'GM', 'OR']):

    CurvData = LoadData(q, '/home/s0675405/Resolution_Paper_Figs/curve_data/')

    CHTs = np.array(CurvData[3])

    Pr = 2.4
    Ps = 1.4

    Ds_u = ((Es_uncert[i] * Pr) / (abs(CHTs) * Ps))
    Ds_no_u = ((Es_no_errs[i] * Pr) / (abs(CHTs) * Ps))

    plt.gca().set_yscale('log', nonposy='clip')
    plt.errorbar(Resolutions, unp.nominal_values(Ds_u), yerr=unp.std_devs(Ds_u),
                 fmt='', color=colors[i], linestyle="None")
    plt.scatter(Resolutions, Ds_no_u, color=colors[i], label=Locations[q])


plt.xlabel("Grid resolution ($m$)")
plt.ylabel("Diffusivity ($m^{2}a^{-1}$)")

plt.tick_params(axis='x', which='both', top='off', length=2)
plt.tick_params(axis='y', which='both', right='off', length=2)

plt.ylim(ymin=0.0005, ymax=1.5)
plt.xlim(xmin=0, xmax=10.5)
legend = plt.legend(scatterpoints=1, fontsize=10)
legend.get_frame().set_linewidth(0.)

fig.subplots_adjust(bottom=0.15)

# set the size of the plot to be saved. These are the JGR sizes:
# quarter page = 95*115
# half page = 190*115 (horizontal) 95*230 (vertical)
# full page = 190*230
fig.set_size_inches(mm_to_inch(190), mm_to_inch(115))

plt.savefig('diff/diff.png', dpi=500)
