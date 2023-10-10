"""
Run using:
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

python plot_2D_contour.py
"""

import numpy as np
import matplotlib.pyplot as plt 

import sys, os
argv = sys.argv
sys.argv = argv[:1]

import optparse

# Actual script
if __name__ == '__main__':
   
    # Read input parameters
    sys.argv = argv

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--radius',          dest='radius',          help='detector radius',                                     default='DEFAULT')
    parser.add_option('--scan_radii',      dest='scan_radii',      help='do a scan on detector radii',                         default='0')
    parser.add_option('--scan_separation', dest='scan_separation', help='do a scan on minimum photons separation',             default='0')
    parser.add_option('--decay_volume',    dest='decay_volume',    help='decay volume length to use in case of scan on radii', default='1.0')

    (opt, args) = parser.parse_args()

    print(f"Radius:                          {opt.radius}")
    print(f"Do radii scan:                   {opt.scan_radii}")
    print(f"Do photons separation scan:      {opt.scan_separation}")
    print(f"Decay volume used in radii scan: {opt.decay_volume}")

    # Value Errors in case input parameters are missing
    if opt.radius == 'DEFAULT' :
        raise ValueError("Please specify the radius")
    radius = opt.radius

    if opt.scan_radii != '0' and opt.scan_radii != '1':
        raise ValueError("Please specify if you want to scan the detector radii")
    scan_radii = False
    if opt.scan_radii == '1':
        scan_radii = True

    if opt.scan_separation != '0' and opt.scan_separation != '1':
        raise ValueError("Please specify if you want to scan the minimum photons separation")
    scan_separation = False
    if opt.scan_separation == '1':
        scan_separation = True

    if opt.decay_volume != '1.0' and opt.decay_volume != '1.5' and opt.decay_volume != '2.0' and opt.decay_volume != '2.5':
        raise ValueError("Please specify a valid decay volume to scan the detector radii")
    decay_volume = opt.decay_volume 

    arr_list = []

    # Perform scan on decay volume
    if (scan_radii == False and scan_separation == False):

        # Read numpy objects
        arr_list.append(np.load(f'2D_contour_decay_volume_2.5_det_radius_{radius}.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_2.0_det_radius_{radius}.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_1.5_det_radius_{radius}.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_1.0_det_radius_{radius}.npy', allow_pickle=True))
        
        labels = [
            "L $_V$ = 2.5 m",
            "L $_V$ = 2.0 m",
            "L $_V$ = 1.5 m",
            "L $_V$ = 1.0 m",
        ]

        # Plotting
        for count,arr in enumerate(arr_list):
            plt.plot(arr[:,0],
                     arr[:,1],
                     label = labels[count],
                     linestyle='dashed',
                     linewidth=1
            )
        plt.title(              "LUXE-NPOD",            fontsize = 14, fontweight = "bold", loc = 'left')
        plt.figtext(0.34, 0.90, "(work in progress)",   fontsize = 12, fontweight = "normal")
        plt.figtext(0.69, 0.84, f"R $_{{Det}}$ = {radius} m", fontsize = 12, fontweight = "normal")
        plt.figtext(0.69, 0.79, "L $_{D}$ = 1.0 m",     fontsize = 12, fontweight = "normal")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel('ALP mass m$_{a,\phi}$ [GeV]',       loc='right', fontsize=14, labelpad = -1)
        plt.ylabel('1/$\Lambda_{a,\phi}$ [GeV$^{-1}$]', loc='top',   fontsize=14, labelpad = -5)
        plt.xlim([0.01, 0.50])
        plt.ylim([1e-6, 2e-3])
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.legend(bbox_to_anchor=(1.0, 0.88), loc='upper right', frameon=False)
        # plt.show()
        
        output_name = f'signal_plots/limit_detector_radius_{radius}'
        plt.savefig(output_name + ".png")
        plt.savefig(output_name + ".pdf")
        plt.close()

    # Perform scan on detector radii
    elif (scan_radii == True and scan_separation == False):

        # Read numpy objects
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_0.1.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_0.2.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_0.3.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_0.5.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_1.0.npy', allow_pickle=True))
        
        labels = [
            "R $_{Det}$ = 0.1 m",
            "R $_{Det}$ = 0.2 m",
            "R $_{Det}$ = 0.3 m",
            "R $_{Det}$ = 0.5 m",
            "R $_{Det}$ = 1.0 m",
        ]

        # Plotting
        for count,arr in enumerate(arr_list):
            plt.plot(arr[:,0],
                     arr[:,1],
                     label = labels[count],
                     linestyle='dashed',
                     linewidth=1
            )
        plt.title(              "LUXE-NPOD",          fontsize = 14, fontweight = "bold", loc = 'left')
        plt.figtext(0.34, 0.90, "(work in progress)", fontsize = 12, fontweight = "normal")
        plt.figtext(0.69, 0.84, f"L $_V$ = {decay_volume} m", fontsize = 12, fontweight = "normal")
        plt.figtext(0.69, 0.79, "L $_D$ = 1.0 m",  fontsize = 12, fontweight = "normal")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel('ALP mass m$_{a,\phi}$ [GeV]',       loc='right', fontsize=14, labelpad = -1)
        plt.ylabel('1/$\Lambda_{a,\phi}$ [GeV$^{-1}$]', loc='top',   fontsize=14, labelpad = -5)
        plt.xlim([0.01, 0.50])
        plt.ylim([1e-6, 2e-3])
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.legend(bbox_to_anchor=(1.0, 0.88), loc='upper right', frameon=False)
        # plt.show()
        
        output_name = f'signal_plots/limit_detector_radius_scan_decay_volume_{decay_volume}'
        plt.savefig(output_name + ".png")
        plt.savefig(output_name + ".pdf")
        plt.close()

    # Perform scan on minimum photons separation
    elif (scan_radii == False and scan_separation == True):

        # Read numpy objects
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_1.0.npy',                 allow_pickle=True)) # we did not run again with zero separation, just to add the appendix in the name
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_1.0_separation_0.01.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_1.0_separation_0.02.npy', allow_pickle=True))
        arr_list.append(np.load(f'2D_contour_decay_volume_{decay_volume}_det_radius_1.0_separation_0.05.npy', allow_pickle=True))

        labels = [
            "Min dist = 0 cm",
            "Min dist = 1 cm",
            "Min dist = 2 cm",
            "Min dist = 5 cm",
        ]

        # Plotting
        for count,arr in enumerate(arr_list):
            plt.plot(arr[:,0],
                     arr[:,1],
                     label = labels[count],
                     linestyle='dashed',
                     linewidth=1
            )
        plt.title(              "LUXE-NPOD",          fontsize = 14, fontweight = "bold", loc = 'left')
        plt.figtext(0.34, 0.90, "(work in progress)", fontsize = 12, fontweight = "normal")
        plt.figtext(0.65, 0.84, f"L $_V$ = {decay_volume} m", fontsize = 12, fontweight = "normal")
        plt.figtext(0.65, 0.79, f"L $_D$ = {radius} m",       fontsize = 12, fontweight = "normal")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel('ALP mass m$_{a,\phi}$ [GeV]',       loc='right', fontsize=14, labelpad = -1)
        plt.ylabel('1/$\Lambda_{a,\phi}$ [GeV$^{-1}$]', loc='top',   fontsize=14, labelpad = -5)
        plt.xlim([0.01, 0.50])
        plt.ylim([1e-6, 2e-3])
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.legend(bbox_to_anchor=(1.0, 0.88), loc='upper right', frameon=False)
        # plt.show()

        output_name = f'signal_plots/limit_detector_separation_scan_decay_volume_{decay_volume}_radius_{radius}'
        plt.savefig(output_name + ".png")
        plt.savefig(output_name + ".pdf")
        plt.close()
