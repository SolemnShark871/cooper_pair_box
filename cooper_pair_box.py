"""
File: cooper_pair_box.py
Author: <a href="mailto:omar.essilfie-quaye@kcl.ac.uk">Omar Essilfie-Quaye</a>
Date: 02-Feb-2019

Plot the Eigen Values of the Hamiltonian that represents the cooper pair box
as they change with respect to the gate induced charge
"""

import os
WINDOWS = True

try:
    directory = os.environ['WINDIR']
except:
    WINDOWS = False

if WINDOWS:
    import matplotlib
    matplotlib.use('qt5agg')

    import matplotlib.pyplot as plt
    plt.switch_backend('agg')
else:
    import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import numpy as np


def hamiltonian(charging_energy, tunneling_energy, n=0, states=5):
    """Function to calculate the Hamiltonian matrix for a cooper pair box with
    a given charging energy and tunneling energy.

    Args:
        charging_energy (float): The energy required to either subtract or add
        a cooper pair to the system

        tunneling_energy (float): The energy required for a cooper pair to
        transition from one energy level to another.

        n (int): The gate induced charge for the cooper pair box

        states (int): The number of states the cooper pair box can take

    Returns:
        A square numpy.matrix containing the Hamiltonian.
    """
    ec = charging_energy
    ej = tunneling_energy
    matrix = []

    for y in range(states):
        row = []
        for x in range(states):
            if(x == y):
                row.append(ec * (states - x - n)**2)
            elif(x == (y + 1) or y == (x + 1)):
                row.append(-.5 * ej)
            else:
                row.append(0)
        matrix.append(row)

    return np.matrix(matrix)

if(__name__ == '__main__'):
    states = [[70, 0],
              [70, 10],
              [20, 10],
              [5, 10]]

    c_patch = ["orange", "purple", "blue", "green", "red"]
    r_patch = mpatches.Patch(color=c_patch[0], label='|0>')
    g_patch = mpatches.Patch(color=c_patch[1], label='|1>')
    b_patch = mpatches.Patch(color=c_patch[2], label='|2>')
    p_patch = mpatches.Patch(color=c_patch[3], label='|3>')
    o_patch = mpatches.Patch(color=c_patch[4], label='|4>')
    patches = [o_patch, p_patch, b_patch, g_patch, r_patch]

    num_eigen_vals = 5
    xx = np.linspace(0, num_eigen_vals, 10 * num_eigen_vals + 1)
    for s in states:
        state = s

        values = []
        for n in xx:
            h = hamiltonian(state[0], state[1], n, num_eigen_vals)
            eig = np.linalg.eig(h)
            eigen_values = np.sort(eig[0])
            values.append(eigen_values)

        plot_vals = []
        for i in range(num_eigen_vals):
            current = []
            for n in range(len(values)):
                current.append(values[n][i])
            plot_vals.append(current)

        for i in range(num_eigen_vals):
            plt.ylim(-10, 100)
            if(i < len(c_patch)):
                plt.plot(xx, plot_vals[i], color=c_patch[i])
            else:
                plt.plot(xx, plot_vals[i])

        plot_title = "Eigen Values Ec:" + str(state[0]) + " Ej:" + str(state[1])
        plot_file = "eigen_values_ec_" + str(state[0]) + "_ej_" + str(state[1])
        plot_file += ".png"

        plt.title(plot_title)
        plt.ylabel("Eigen Values")
        plt.xlabel("Gate Induced Charge")
        plt.legend(handles=patches, bbox_to_anchor=(1.05, 1),
                   loc=2, borderaxespad=0.)
        plt.savefig(plot_file, bbox_inches='tight')
        plt.cla()
        plt.clf()

        print("Graph Saved in \"" + plot_file + "\".")
        xx = np.linspace(0, num_eigen_vals, 20 * num_eigen_vals + 1)
