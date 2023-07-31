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
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh
python plot_signal_distributions.py
'''''''''''''''

Mass-couplings points are selected based on:
https://indico.desy.de/event/35797/#12-status-of-npod-activities
"""

import numpy as np
import matplotlib.pyplot as plt 
import pickle
import pandas as pd
import sys, os

def read_file(folder_name = "/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_6142550095_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_9.806757216915766e-06/",
              variable = "photon_radius_1"):

    # Split folder name and create full file name
    folder_simplified = folder_name.replace('/', '')
    folder_split = folder_simplified.split("_")

    # folder_split:
    # ['storage9rquishpeluxenpodphase1signalLUXE-NPODoutput', 'condorluxe', '6142550095', 'mass', '0.346737', 'distance', '1.0', 'targetlength', '1.0', 'minenergy', '0.5', 'detectorradius', '0.5', 'spectrum', 'primarylc', 'phase', '1', 'primary', 'li', '9.806757216915766e-06']

    random_number   = folder_split[2]
    mass            = folder_split[4]
    decay_volume    = folder_split[6]
    dump_length     = folder_split[8]
    min_energy      = folder_split[10]
    detector_radius = folder_split[12]
    spectrum        = folder_split[14]
    coupling        = folder_split[19]

    print("random_number   : {}".format(folder_split[2]))
    print("mass            : {}".format(folder_split[4]))
    print("decay_volume    : {}".format(folder_split[6]))
    print("dump_length     : {}".format(folder_split[8]))
    print("min_energy      : {}".format(folder_split[10]))
    print("detector_radius : {}".format(folder_split[12]))
    print("spectrum        : {}".format(folder_split[14]))
    print("coupling        : {}".format(folder_split[19]))

    file_name = folder_name + variable + ".npy"

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
    "photon_radius_cumulative",
]

output_directory = "signal_plots"
os.system("mkdir -p {}".format(output_directory))

for norm in (True, False):
    
    for var in variables: 
        
        print("Varible: {}".format(var))
        
        dict_list = []
        
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2748393110_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_6151305420_mass_0.1_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_1609959775_mass_0.301995_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_2.4063341373555067e-06/", var))

        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_1969891329_mass_0.346737_distance_2.5_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2226503312_mass_0.346737_distance_2.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_5148817684_mass_0.346737_distance_1.5_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2748393110_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))


        max_y = 0

        # Loop on all histograms
        for arr_dict in dict_list:
        
            if var == "photon_radius_cumulative":
                print(arr_dict['frac'])
                print(arr_dict['centers'])
            else :
                print(arr_dict['entries'])
                print(arr_dict['bins'])

            print(arr_dict['xlabel'])
            print(arr_dict['ylabel'])
            print(arr_dict['xrange'])
            print(arr_dict['mass'])
            print(arr_dict['coupling'])
            print(arr_dict['variable'])
            print(arr_dict['decay_volume'])
            
            if var == "photon_radius_cumulative":
                entries      = arr_dict['frac']
                bins         = arr_dict['centers']
            else:
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
        
            
            if var == "photon_radius_cumulative":
                plt.hist(bins, 
                         bins, 
                         range=x_range,
                         weights=entries,
                         density=norm,
                         label=my_label,
                         histtype='step')
            else:
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
