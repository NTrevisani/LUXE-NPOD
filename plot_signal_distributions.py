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

    # Check if we are considering files with minumum separation between photons
    global separation
    separation = 0
    if "separation" in folder_name:
        separation = 1

    print(f"Separation: {separation}")

    # Split folder name and create full file name
    folder_simplified = folder_name.replace('/', '_')
    folder_split = folder_simplified.split("_")

    ###############
    # folder_split:
    ###############

    # Without separation: ['', 'storage', '9', 'rquishpe', 'luxe', 'npod', 'phase1', 'signal', 'LUXE-NPOD', 'output', 'condor', 'luxe', '6142550095', 'mass', '0.346737', 'distance', '1.0', 'targetlength', '1.0', 'minenergy', '0.5', 'detectorradius', '0.5', 'spectrum', 'primary', 'lc', 'phase', '1', 'primary', 'li', '9.80675716915766e-06', '']

    # With separation: ['', 'storage', '9', 'rquishpe', 'luxe', 'npod', 'phase1', 'signal', 'LUXE-NPOD', 'output', 'condor', 'luxe', '0129369347', 'mass', '0.346737', 'distance', '1.0', 'targetlength', '1.0', 'minenergy', '0.5', 'detectorradius', '1.0', 'spectrum', 'primary', 'separation', '0.0', 'lc', 'phase', '1', 'primary', 'li', '5.252172519661923e-06', '']

    min_separation  = ''
    random_number   = folder_split[12]
    mass            = folder_split[14]
    decay_volume    = folder_split[16]
    dump_length     = folder_split[18]
    min_energy      = folder_split[20]
    detector_radius = folder_split[22]
    spectrum        = folder_split[24]
    coupling        = folder_split[30]
    if separation == 1:
        min_separation = folder_split[26]
        coupling       = folder_split[32]

    print("random_number   : {}".format(folder_split[12]))
    print("mass            : {}".format(folder_split[14]))
    print("decay_volume    : {}".format(folder_split[16]))
    print("dump_length     : {}".format(folder_split[18]))
    print("min_energy      : {}".format(folder_split[20]))
    print("detector_radius : {}".format(folder_split[22]))
    if separation == 1:
        print("separation      : {}".format(folder_split[26]))
        print("coupling        : {}".format(folder_split[32]))
    else:
        print("coupling        : {}".format(folder_split[30]))


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
    arr_dict['separation']   = min_separation

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
        
        # # A point close to the bottom-right edge of the exclusion plot
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_1969891329_mass_0.346737_distance_2.5_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2226503312_mass_0.346737_distance_2.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_5148817684_mass_0.346737_distance_1.5_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2748393110_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_5.252172519661923e-06/", var))

        # A point close to the bottom-right edge of the exclusion plot - scanning here the minimum distance
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_0129369347_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.0/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_7932358700_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.01/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_3464419000_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.02/lc_phase_1_primary_li_5.252172519661923e-06/", var))
        dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2405142246_mass_0.346737_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.05/lc_phase_1_primary_li_5.252172519661923e-06/", var))


        # # One of our interested points: light ALP with large coupling [mass: 5.01187000e-02, coupling:  8.84595614e-04]
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_3077700877_mass_0.0501187_distance_2.5_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_0.0007759442308140531/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_2380040305_mass_0.0501187_distance_2.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_0.0007759442308140531/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_6392341119_mass_0.0501187_distance_1.5_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_0.0007759442308140531/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_9547209163_mass_0.0501187_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_0.5_spectrum_primary/lc_phase_1_primary_li_0.0007759442308140531/", var))

        # # One of our interested points: light ALP with large coupling [mass: 5.01187000e-02, coupling:  8.84595614e-04] - scanning here the minimum distance
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_1024665565_mass_0.0501187_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.0/lc_phase_1_primary_li_0.0007759442308140531/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_4149326682_mass_0.0501187_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.01/lc_phase_1_primary_li_0.0007759442308140531/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_9293166185_mass_0.0501187_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.02/lc_phase_1_primary_li_0.0007759442308140531/", var))
        # dict_list.append(read_file("/storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/luxe_7519683781_mass_0.0501187_distance_1.0_targetlength_1.0_minenergy_0.5_detectorradius_1.0_spectrum_primary_separation_0.05/lc_phase_1_primary_li_0.0007759442308140531/", var))

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
            print(arr_dict['separation'])
            
            if var == "photon_radius_cumulative":
                entries      = arr_dict['frac']
                bins         = arr_dict['centers']
            else:
                entries      = arr_dict['entries']
                bins         = arr_dict['bins']
            xlabel         = arr_dict['xlabel']
            ylabel         = arr_dict['ylabel']
            x_range        = arr_dict['xrange']
            mass           = arr_dict['mass']
            coupling       = float(arr_dict['coupling'])
            variable       = arr_dict['variable']
            decay_volume   = arr_dict['decay_volume']
            min_separation = arr_dict['separation']
            
            # Set y-axis range
            if norm == True:
                y = np.max(entries) / ((bins[1] - bins[0]) * np.trapz(entries))
                if y > max_y :
                    max_y = y
            else:
                y = np.max(entries)
                if y > max_y :
                    max_y = y
                
            my_label = "mass = {} - coupling = {} - decay volume = {}".format(round(float(mass),4), round(coupling,4), decay_volume)
            if separation == 1:
                my_label = "mass = {} - coupling = {} - min separation = {}".format(round(float(mass),4), round(coupling,4), min_separation)
        
            if var == "photon_radius_cumulative":
                plt.hist(bins-bins[0],
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
                
            if 'radius' in var or 'distance' in var:
                plt.xlim([0.0, 1.00])
            plt.ylim([0, 1.5*max_y])
            plt.xlabel(xlabel, loc = 'right', fontsize = 14, labelpad = -2)
            plt.ylabel(ylabel, loc = 'top',   fontsize = 14)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.title(              "LUXE-NPOD",          fontsize = 14, fontweight = "bold", loc = 'left')
            plt.figtext(0.34, 0.90, "(work in progress)", fontsize = 12, fontweight = "light")
            plt.legend()
            output_folder_name = f'{output_directory}/mass_{mass}_coupling_{coupling}/' # mass_0.346737_coupling_5.252172519661923e-06
            if separation == 1:
                output_folder_name = f'{output_directory}/mass_{mass}_coupling_{coupling}_separation/'
            os.system(f'mkdir -p {output_folder_name}')
            output_name = f'{output_folder_name}/{var}'
            if norm == True:
                output_name = f'{output_folder_name}/{var}_normalized'
            plt.savefig(output_name + '.png')
            plt.savefig(output_name + '.pdf')
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
