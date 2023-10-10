"""
Example of one file:
/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_6142550095_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/events_lcphase_1_primary.txt

txt file structure:
[mass, li, gagg, ctau, L_eff_pb, nevents]

We are interested in:
- mass ([0])
- gagg ([2])
- nevents ([5])

Naming convention:
- luxe_0850833375           --> Just a random number
- mass_0.199526             --> ALP mass [GeV]
- distance_2.5              --> Decay volume length [m]
- targetlength 1.0          --> Dump length [m]
- minenergy_0.5             --> Min energy recorded by the detector [GeV]
- detectorradius_1.0        --> Detector radius [m]
- spectrum_primary          --> Indicates whether all incoming photons or just primary photons are considered in the signal production
/
- separation_0.05           --> Minimum separation between photons resolved by the "detector"
- lc_phase_1_primar  y      --> No idea, possibly not relevant
- li_2.0585400556229296e-06 --> Photon-ALP coupling
/
- photon_radius_1.npy

'''''''''''''''
Run using:
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

python plot_limits.py --decay_volume 2.5 --radius 1.0 --excl_list 2550818117
python plot_limits.py --decay_volume 2.0 --radius 1.0
python plot_limits.py --decay_volume 1.5 --radius 1.0
python plot_limits.py --decay_volume 1.0 --radius 1.0

python plot_limits.py --decay_volume 2.5 --radius 0.5
python plot_limits.py --decay_volume 2.0 --radius 0.5
python plot_limits.py --decay_volume 1.5 --radius 0.5
python plot_limits.py --decay_volume 1.0 --radius 0.5
'''''''''''''''
"""

import numpy as np
import matplotlib.pyplot as plt 
import pickle
import pandas as pd
import sys, os
argv = sys.argv
sys.argv = argv[:1]

import optparse

def read_file(file_name = "/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_6142550095_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/events_lcphase_1_primary.txt"):
    """
    Return expected events for a mass point and all inspected coupling values.

    Given the txt file name, the function extracts the expected number of
    events for a single ALP mass value, scanning all the inspected
    coupling values.
    The output is a dictionary with a single entry:
    - The key is the mass value in GeV.
    - The value is a list of expected events, one for each 
        coupling value.
    """

    # Read python file
    with open(file_name) as f:
        lines = f.readlines()
        
    coupling_list = []

    for line in lines:
        words = line.replace(",","").split()
        mass     = words[0]
        # coupling = words[2]
        nevents  = words[5]
        coupling_list.append(float(nevents))

    output_dict = {float(mass) : coupling_list}

    return output_dict


# def coupling_list(file_name = "/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_6142550095_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/events_lcphase_1_primary.txt"):
def coupling_list(file_name = "/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_3757385365_mass_0.020893_distance_2.5_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.05/events_lcphase_1_primary.txt"):
    """
    Return the list of inspected coupling values.

    
    Given the txt file name, the function extracts the values of
    all the inspected coupling values.
    The output is a standard python list.
    """
    
    # Read python file
    with open(file_name) as f:
        lines = f.readlines()
        
    coupling_list = []
    for line in lines:
        words = line.replace(",","").split()
        coupling = words[2]
        coupling_list.append(float(coupling))
        
    return coupling_list


# Actual script
if __name__ == '__main__':
   
    # Read input parameters
    sys.argv = argv

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--decay_volume',  dest='decay_volume',  help='decay_volume_length',                                                    default='DEFAULT')
    parser.add_option('--radius',        dest='radius',        help='detector_radius',                                                        default='DEFAULT')
    parser.add_option('--minseparation', dest='minseparation', help='minimum photons separation',                                             default='DEFAULT')
    parser.add_option('--excl_list',     dest='excl_list',     help='individual directory to exclude, based on the random identifier number', default=None)
 
    (opt, args) = parser.parse_args()

    print(f"Decay volume:              {opt.decay_volume}")
    print(f"Radius:                    {opt.radius}")
    print(f"Excluded points:           {opt.excl_list}")
    print(f"Minimum photon separation: {opt.minseparation}")

    # Value Errors in case input parameters are missing
    if opt.decay_volume == 'DEFAULT' :
        raise ValueError("Please specify the decay volume")
    decay_volume = opt.decay_volume

    if opt.radius == 'DEFAULT' :
        raise ValueError("Please specify the radius")
    radius = opt.radius

    # if opt.minseparation == 'DEFAULT' :
        # raise ValueError("Please specify the minimum photons separation")
    minseparation = opt.minseparation

    excl_list = []
    if opt.excl_list is not None:
        print("Not None!")
        excl_list = opt.excl_list.split(",")

    dict_tot = {}

    # Create list of all directories
    directories = os.listdir('/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/')

    # Select the specific experimental layout
    for directory in directories:
        if f"distance_{decay_volume}"    not in directory: continue
        if f"detectorradius_{radius}"    not in directory: continue
        if minseparation == "DEFAULT" and "separation" in directory: continue
        if minseparation != "DEFAULT" and f"separation_{minseparation}" not in directory: continue

        skip = 0
        for exclude in excl_list:
            if f"luxe_{exclude}" in directory: skip = 1
        if skip == 1: continue
        
        # Create a dictionary, merging all dictionaries from each mass point
        dict_list = read_file('/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/' + directory + '/events_lcphase_1_primary.txt')
        for key, value in dict_list.items():
            dict_tot[key] = value
        
    # Create and sort the coupling values
    all_couplings = coupling_list()
    all_couplings.sort()

    # Create and sort the mass values
    mass_list = []
    for key in dict_tot:
        mass_list.append(key)
    mass_list.sort()

    # Create grid of mass and coupling points, needed to create contour plots
    X, Y = np.meshgrid(mass_list, all_couplings)
    print(X,Y)

    # Create matrix of expected number of events, needed to create contour plots
    list_of_list = []
    for mass in mass_list:
        list_of_list.append(dict_tot[mass])

    print("All couplings: ", all_couplings)
    print()
    print("Mass list: ", mass_list)

    my_matrix = np.matrix(list_of_list)

    # Create contour plot
    cs = plt.contour(X,Y, my_matrix.transpose(), [3])
    limit_2D = cs.collections[0].get_paths()[0].vertices
    plt.xscale("log")
    plt.yscale("log")
    print(limit_2D)
    
    output_name = f"2D_contour_decay_volume_{decay_volume}_det_radius_{radius}_separation_{minseparation}.npy"
    if minseparation == "DEFAULT":
        output_name = f"2D_contour_decay_volume_{decay_volume}_det_radius_{radius}.npy"
    np.save(output_name, limit_2D)
