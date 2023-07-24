"""
Example of one file:
/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output/luxe_0850833375_mass_0.199526_distance_2.5_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary/lc_phase_1_primary_li_2.0585400556229296e-06/photon_radius_1.npy

Naming convention:
- luxe_0850833375           --> Just a random number
- mass_0.199526             --> ALP mass [GeV]
- distance_2.5              --> Decay volume length [m]
- targetlength 1.0          --> Dump length [m]
- minenergy_0.5             --> Min energy recorded by the detector [GeV]
- detectorradius_1.0        --> Detector radius [m]
- spectrum_primary          --> Indicates whether all incoming photons or just primary photons are considered in the signal production
/
- lc_phase_1_primar  y      --> No idea, possibly not relevant
- li_2.0585400556229296e-06 --> Photon-ALP coupling
/
- photon_radius_1.npy

'''''''''''''''
Run using:
python plot.py
'''''''''''''''

Mass-couplings points are selected based on:
https://indico.desy.de/event/35797/#12-status-of-npod-activities
"""

import numpy as np
import matplotlib.pyplot as plt 
import pickle
import pandas as pd
import sys, os

def read_file(random_number = '0850833375', mass = '0.199526', decay_volume = '2.5', dump_length = '1.0', min_energy = '0.5', detector_radius = '1.0', spectrum = 'primary', coupling = '2.0585400556229296e-06', variable = 'photon_radius_1'):
    # Build file name
    file_name = "/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output/luxe_{}_mass_{}_distance_{}_targetlength_{}_minenergy_{}_detectorradius_{}_spectrum_{}/lc_phase_1_primary_li_{}/{}.npy".format(
        random_number, mass, decay_volume, dump_length, min_energy, detector_radius, spectrum, coupling, variable)

    # Read numpy object
    arr = np.load(file_name, allow_pickle=True)
    
    # Extract dictionary
    arr_dict = arr[()]

    # Add information for legend
    arr_dict['mass']         = mass
    arr_dict['coupling']     = coupling
    arr_dict['variable']     = variable
    arr_dict['decay_volume'] = decay_volume

    return arr_dict

variables = [
    "decay_distance",
    "decay_vertex",
    "decay_vertex_time",
    "photon_energy_1",
    "photon_energy_2",
    "photon_radius_1",
    "photon_radius_2",
    "photon_radius_max",
    "photons_distance",
    "photon_time_1",
    "photon_time_2",
    # "photon_radius_cumulative",
]

output_directory = "signal_plots"
os.system("mkdir -p {}".format(output_directory))

for norm in (True, False):

    for var in variables: 

        print("Varible: {}".format(var))

        dict_list = []

        # /storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output/luxe_7848588860_mass_0.398107_distance_2.5_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary/lc_phase_1_primary_li_1.7610136077199334e-06/photon_radius_1.npy
        dict_list.append(read_file(random_number = '0850833375', mass = '0.199526', decay_volume = '2.5', dump_length = '1.0', min_energy = '0.5', detector_radius = '1.0', spectrum = 'primary', coupling = '2.0585400556229296e-06', variable = var))
        dict_list.append(read_file(random_number = '1435856215', mass = '0.501187', decay_volume = '2.5', dump_length = '1.0', min_energy = '0.5', detector_radius = '1.0', spectrum = 'primary', coupling = '2.0585400556229296e-06', variable = var))
        dict_list.append(read_file(random_number = '7848588860', mass = '0.398107', decay_volume = '2.5', dump_length = '1.0', min_energy = '0.5', detector_radius = '1.0', spectrum = 'primary', coupling = '1.7610136077199334e-06', variable = var))
        dict_list.append(read_file(random_number = '4745422152', mass = '0.1',      decay_volume = '2.5', dump_length = '1.0', min_energy = '0.5', detector_radius = '1.0', spectrum = 'primary', coupling = '4.493061600600467e-06',  variable = var))
        dict_list.append(read_file(random_number = '4745422152', mass = '0.1',      decay_volume = '2.5', dump_length = '1.0', min_energy = '0.5', detector_radius = '1.0', spectrum = 'primary', coupling = '0.00010197050644580961', variable = var))

        max_y = 0

        # Loop on all histograms
        for arr_dict in dict_list:
        
            print(arr_dict['entries'])
            print(arr_dict['bins'])
            print(arr_dict['xlabel'])
            print(arr_dict['ylabel'])
            print(arr_dict['xrange'])
            print(arr_dict['mass'])
            print(arr_dict['coupling'])
            print(arr_dict['variable'])
            print(arr_dict['decay_volume'])
            
            entries      = arr_dict['entries']
            bins         = arr_dict['bins']
            xlabel       = arr_dict['xlabel']
            ylabel       = arr_dict['ylabel']
            x_range      = arr_dict['xrange']
            mass         = arr_dict['mass']
            coupling     = float(arr_dict['coupling'])
            variable     = arr_dict['variable']
            decay_volume = arr_dict['decay_volume']
            
            # Set y-axis range
            if norm == True:
                y = np.max(entries) / ((bins[1] - bins[0]) * np.trapz(entries))
                if y > max_y : 
                    max_y = y
            else:
                y = np.max(entries)
                if y > max_y : 
                    max_y = y
                
            my_label = "mass = {} - coupling = {} - decay volume = {}".format(mass, round(coupling,8), decay_volume)
        
            plt.hist(bins[:-1], 
                     bins, 
                     range=x_range,
                     weights=entries,
                     density=norm,
                     label=my_label,
                     histtype='step')
                
            plt.ylim([0, 1.5*max_y])
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(variable)
            plt.legend()
            output_name = '{}/{}.png'.format(output_directory, var)
            if norm == True:
                output_name = '{}/{}_normalized.png'.format(output_directory, var)
            plt.savefig(output_name)
        plt.close()

    #     plt.hist(bins[:-1], 
    #              bins, 
    #              range=x_range,
    #              weights=entries,
    #              density=False,
    #              label=my_label,
    #              histtype='step')

    #     plt.ylim([0,max_y])
    #     plt.xlabel(xlabel)
    #     plt.ylabel(ylabel)
    #     plt.title(variable)
    #     plt.legend()
    #     plt.savefig('test_plot_{}.png'.format(var))
    # plt.close()
