"""
Run using:
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

python plot_2D_contour.py
"""

import numpy as np
import matplotlib.pyplot as plt 

arr_list = []

# Read numpy objects
arr_list.append(np.load('2D_contour_decay_volume_2.5_det_radius_1.0.npy', allow_pickle=True))
arr_list.append(np.load('2D_contour_decay_volume_2.0_det_radius_1.0.npy', allow_pickle=True))
arr_list.append(np.load('2D_contour_decay_volume_1.5_det_radius_1.0.npy', allow_pickle=True))
arr_list.append(np.load('2D_contour_decay_volume_1.0_det_radius_1.0.npy', allow_pickle=True))

labels = [
    "decay volume = 2.5 m",
    "decay volume = 2.0 m",
    "decay volume = 1.5 m",
    "decay volume = 1.0 m",
]

# Plotting
for count,arr in enumerate(arr_list):
    plt.plot(arr[:,0],
             arr[:,1],
             label = labels[count],
             linestyle='dashed',
             linewidth=1
    )
plt.text(0.00001, 0.1, 'Detector Radius = 1 m', fontsize=100)
plt.title("Detector Radius = 1 m",      loc='right')
plt.title("LUXE-NPOD work in progress", loc='left', fontweight='bold')
plt.xscale("log")
plt.yscale("log")
plt.xlabel('ALP mass m$_a$ [GeV]',              loc='right', fontsize=12)
plt.ylabel('1/$\Lambda_{a,\phi}$ [GeV$^{-1}$]', loc='top', fontsize=12)
plt.xlim([0.01, 0.50])
plt.ylim([1e-6, 2e-3])
plt.legend(loc='upper right')
plt.show()
