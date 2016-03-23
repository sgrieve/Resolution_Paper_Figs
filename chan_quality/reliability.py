import string
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


def mm_to_inch(mm):
    return mm * 0.0393700787

# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 8
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

Resolutions = [5, 10, 20, 30]
Location = ['Gabilan Mesa', 'Santa Cruz\nIsland', 'Oregon Coast\nRange']

# getting a 1 indexed list so it matches the subplot label
labels = [''] + list(string.ascii_lowercase)[:6]

# Data is in order GM, SC, OR
r_pelletier = ([0.66, 0.65, 0.57, 0.48], [0.81, 0.76, 0.4, 0.5],
               [0.36, 0.48, 0.42, 0.38])

s_pelletier = ([0.51, 0.35, 0.22, 0.14], [0.57, 0.33, 0.04, 0.06],
               [0.5, 0.37, 0.18, 0.11])

r_dreich = ([0.36, 0.19, 0.05, 0.02], [0.63, 0.76, 0.08, 0.03],
            [0.23, 0.24, 0.13, 0.])

s_dreich = ([0.27, 0.1, 0.02, 0.01], [0.41, 0.26, 0.01, 0.],
            [0.31, 0.09, 0.01, 0.])

for a, i in enumerate([1, 3, 5]):
    plt.subplot(3, 2, i)

    if not a:
        plt.title('Geometric')

    plt.plot(Resolutions, r_pelletier[a], 'k-')
    plt.plot(Resolutions, s_pelletier[a], 'k--')
    plt.ylim(0, 1)
    plt.xlim(5, 30)
    plt.tick_params(axis='x', which='both', top='off', length=2)
    plt.tick_params(axis='y', which='both', right='off', length=2)
    plt.annotate(labels[i], xy=(0.03, 0.95), xycoords='axes fraction',
                 fontsize=12, horizontalalignment='left',
                 verticalalignment='top')
    if (i != 5):
        plt.gca().axes.get_xaxis().set_ticklabels([])

for b, j in enumerate([2, 4, 6]):
    plt.subplot(3, 2, j)

    if not b:
        plt.title('DrEICH')

    plt.plot(Resolutions, r_dreich[b], 'k-', label='Reliability')
    plt.plot(Resolutions, s_dreich[b], 'k--', label='Sensitivity')
    plt.ylim(0, 1)
    plt.xlim(5, 30)
    plt.tick_params(axis='x', which='both', top='off', length=2)
    plt.tick_params(axis='y', which='both', right='off', length=2)
    plt.annotate(labels[j], xy=(0.03, 0.95), xycoords='axes fraction',
                 fontsize=12, horizontalalignment='left',
                 verticalalignment='top')
    plt.gca().text(32, 0.5, Location[b], ha='center', va='center',
                   rotation='vertical', size=12)
    if (j != 6):
        plt.gca().axes.get_xaxis().set_ticklabels([])

    plt.gca().axes.get_yaxis().set_ticklabels([])


plt.gcf().text(0.5, 0.03, 'Resolution ($m$)', ha='center', va='center',
               size=12)
plt.gcf().text(0.04, 0.5, 'Index of quality', ha='center', va='center',
               rotation='vertical', size=12)

legend = plt.legend(loc=0)
legend.get_frame().set_linewidth(0.)

plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.11, top=0.95, left=0.1, right=0.92)

# set the size of the plot to be saved. These are the JGR sizes:
# quarter page = 95*115
# half page = 190*115 (horizontal) 95*230 (vertical)
# full page = 190*230
plt.gcf().set_size_inches(mm_to_inch(190), mm_to_inch(115))

plt.savefig('chan_quality/reliability.png', dpi=500)
