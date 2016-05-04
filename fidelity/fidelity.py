import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 8
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'


def mm_to_inch(mm):
    return mm * 0.0393700787


def Fidelity(omega, deltaX):

    left = (2. / (deltaX * deltaX))

    right = np.sqrt(1. - 2. * np.cos(omega * deltaX) +
                    (np.cos(omega * deltaX) * np.cos(omega * deltaX)))

    return (left * right) / (omega * omega)


L = 10.
Omega = (2 * np.pi) / L
DeltaX = np.arange(0.001, 5, 0.001)

plt.plot(DeltaX / L, Fidelity(Omega, DeltaX), 'k')
plt.ylim(0.4, 1.0)
plt.tick_params(axis='x', which='both', top='off', length=2)
plt.tick_params(axis='y', which='both', right='off', length=2)
plt.xlabel('Dimensionless wavenumber, $\Delta x/L$')
plt.ylabel('Fidelity, $F(\omega; \Delta x)$')

# set the size of the plot to be saved. These are the JGR sizes:
# quarter page = 95*115
# half page = 190*115 (horizontal) 95*230 (vertical)
# full page = 190*230
plt.gcf().set_size_inches(mm_to_inch(95), mm_to_inch(95))

plt.savefig('fidelity/fidelity.png', dpi=500)
