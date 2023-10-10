# LUXE-NPOD

Repository with code for LUXE-NPOD studies

### Before starting

Source required to use RDataFrame:

    source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh 

### Post-process G4 simulation files

Legacy cfg:

    python submit_RDF_jobs.py --input_file=list_files_tungsten_LegacyCfg_BX0 --material=tungsten --length=LegacyCfg --BX=0

Tungsten:

    python submit_RDF_jobs.py --input_file=list_files_tungsten_1000_BX0 --material=tungsten --length=1000 --BX=0
    python submit_RDF_jobs.py --input_file=list_files_tungsten_1000_BX3 --material=tungsten --length=1000 --BX=3
    python submit_RDF_jobs.py --input_file=list_files_tungsten_1000_BX4 --material=tungsten --length=1000 --BX=4
    python submit_RDF_jobs.py --input_file=list_files_tungsten_1000_BX5 --material=tungsten --length=1000 --BX=5

    python submit_RDF_jobs.py --input_file=list_files_tungsten_500_BX1  --material=tungsten --length=500  --BX=1


Lead:

    python submit_RDF_jobs.py --input_file=list_files_lead_1000_BX4     --material=lead     --length=1000 --BX=4


Copper:

    python submit_RDF_jobs.py --input_file=list_files_copper_1000_BX3   --material=copper   --length=1000 --BX=3


Older tests:

    python submit_RDF_jobs.py --input_file=list_files_npod_old                        --material=copper                 --length=1000 --BX=OLD

    python submit_RDF_jobs.py --input_file=list_files_copper_run_old_1000_BX3         --material=copper_run_old         --length=1000 --BX=3

    python submit_RDF_jobs.py --input_file=list_files_copper_run_old_no_flag_1000_BX3 --material=copper_run_old_no_flag --length=1000 --BX=3

### Produce plots running on post-processed rootfiles

    python mkPlot.py --input_folder=rootfiles --particle=Photons   --material=tungsten --length=LegacyCfg --BX=0.5 --number=_0
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons  --material=tungsten --length=LegacyCfg --BX=0.5 --number=_0

    python mkPlot.py --input_folder=rootfiles --particle=Photons   --material=tungsten --length=1000 --BX=4 --number=_0345
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons  --material=tungsten --length=1000 --BX=4 --number=_0345

    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=1000 --BX=1 --number=_0
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=1000 --BX=1 --number=_0

    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=500 --BX=1 --number=_1
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=500 --BX=1 --number=_1


    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=lead --length=1000 --BX=1 --number=_4
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=lead --length=1000 --BX=1 --number=_4


    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=copper --length=1000 --BX=1 --number=_3
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=copper --length=1000 --BX=1 --number=_3

    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=copper_OLD --length=1000 --BX=1 --number=""
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=copper_OLD --length=1000 --BX=1 --number=""

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=copper_run_old         --length=1000 --BX=1 --number="" 
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=copper_run_old         --length=1000 --BX=1 --number=""

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=copper_run_old_no_flag --length=1000 --BX=1 --number=""
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=copper_run_old_no_flag --length=1000 --BX=1 --number=""


Extrapolation at different dump-detector distances:

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=Extrapolate_1000 --BX=0.1 --number="_0" --output_folder=plots_extrapolation
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=Extrapolate_1000 --BX=0.1 --number="_0" --output_folder=plots_extrapolation

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=Extrapolate_500 --BX=0.1 --number="_0" --output_folder=plots_extrapolation
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=Extrapolate_500 --BX=0.1 --number="_0" --output_folder=plots_extrapolation

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=Extrapolate_300 --BX=0.1 --number="_0" --output_folder=plots_extrapolation
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=Extrapolate_300 --BX=0.1 --number="_0" --output_folder=plots_extrapolation


    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=lead --length=Extrapolate_1000 --BX=0.1 --number="_0" --output_folder=plots_extrapolation
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=lead --length=Extrapolate_1000 --BX=0.1 --number="_0" --output_folder=plots_extrapolation

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=lead --length=Extrapolate_500 --BX=0.1 --number="_0" --output_folder=plots_extrapolation
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=lead --length=Extrapolate_500 --BX=0.1 --number="_0" --output_folder=plots_extrapolation

    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=lead --length=Extrapolate_300 --BX=0.1 --number="_0" --output_folder=plots_extrapolation
    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=lead --length=Extrapolate_300 --BX=0.1 --number="_0" --output_folder=plots_extrapolation


### Plot signal distributions and exclusion limits

Source the needed cvmfs setup:

    source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

Produce signal kinematical distributions:

    python plot_signal_distributions.py

Plot exclusion limits:

    python plot_limits.py --decay_volume 2.5 --radius 1.0 --excl_list 2550818117
    python plot_limits.py --decay_volume 2.0 --radius 1.0
    python plot_limits.py --decay_volume 1.5 --radius 1.0
    python plot_limits.py --decay_volume 1.0 --radius 1.0

    python plot_2D_contour.py --radius 1.0


    python plot_limits.py --decay_volume 2.5 --radius 0.5
    python plot_limits.py --decay_volume 2.0 --radius 0.5
    python plot_limits.py --decay_volume 1.5 --radius 0.5
    python plot_limits.py --decay_volume 1.0 --radius 0.5

    python plot_2D_contour.py --radius 0.5


    python plot_limits.py --decay_volume 2.5 --radius 0.3
    python plot_limits.py --decay_volume 2.0 --radius 0.3
    python plot_limits.py --decay_volume 1.5 --radius 0.3
    python plot_limits.py --decay_volume 1.0 --radius 0.3

    python plot_2D_contour.py --radius 0.3


    python plot_limits.py --decay_volume 2.5 --radius 0.2
    python plot_limits.py --decay_volume 2.0 --radius 0.2
    python plot_limits.py --decay_volume 1.5 --radius 0.2
    python plot_limits.py --decay_volume 1.0 --radius 0.2

    python plot_2D_contour.py --radius 0.2


    python plot_limits.py --decay_volume 2.5 --radius 0.1 --minseparation 0.0
    mv 2D_contour_decay_volume_2.5_det_radius_0.1_separation_0.0.npy 2D_contour_decay_volume_2.5_det_radius_0.1.npy

    python plot_limits.py --decay_volume 2.0 --radius 0.1 --minseparation 0.0
    mv 2D_contour_decay_volume_2.0_det_radius_0.1_separation_0.0.npy 2D_contour_decay_volume_2.0_det_radius_0.1.npy

    python plot_limits.py --decay_volume 1.5 --radius 0.1 --minseparation 0.0
    mv 2D_contour_decay_volume_1.5_det_radius_0.1_separation_0.0.npy 2D_contour_decay_volume_1.5_det_radius_0.1.npy

    python plot_limits.py --decay_volume 1.0 --radius 0.1 --minseparation 0.0
    mv 2D_contour_decay_volume_1.0_det_radius_0.1_separation_0.0.npy 2D_contour_decay_volume_1.0_det_radius_0.1.npy

    python plot_2D_contour.py --radius 0.1


    python plot_2D_contour.py --radius 0.5 --scan_radii 1 --decay_volume 1.0
    python plot_2D_contour.py --radius 0.5 --scan_radii 1 --decay_volume 1.5
    python plot_2D_contour.py --radius 0.5 --scan_radii 1 --decay_volume 2.0
    python plot_2D_contour.py --radius 0.5 --scan_radii 1 --decay_volume 2.5


Plot exclusion limits vs minimum photons separation:

    python plot_limits.py --decay_volume 1.0 --radius 1.0
    python plot_limits.py --decay_volume 1.0 --radius 1.0 --minseparation 0.01
    python plot_limits.py --decay_volume 1.0 --radius 1.0 --minseparation 0.02 --excl_list 4305401700
    python plot_limits.py --decay_volume 1.0 --radius 1.0 --minseparation 0.05

    python plot_2D_contour.py --radius 1.0 --scan_separation 1 --decay_volume 1.0


    python plot_limits.py --decay_volume 1.5 --radius 1.0
    python plot_limits.py --decay_volume 1.5 --radius 1.0 --minseparation 0.01
    python plot_limits.py --decay_volume 1.5 --radius 1.0 --minseparation 0.02 --excl_list 9954835239,9587931072
    python plot_limits.py --decay_volume 1.5 --radius 1.0 --minseparation 0.05

    python plot_2D_contour.py --radius 1.0 --scan_separation 1 --decay_volume 1.5


    python plot_limits.py --decay_volume 2.0 --radius 1.0
    python plot_limits.py --decay_volume 2.0 --radius 1.0 --minseparation 0.01 --excl_list 2340249156,1878311950,2339173445
    python plot_limits.py --decay_volume 2.0 --radius 1.0 --minseparation 0.02 --excl_list 3157945829,2712751416,4169018722
    python plot_limits.py --decay_volume 2.0 --radius 1.0 --minseparation 0.05 --excl_list 3792642379

    python plot_2D_contour.py --radius 1.0 --scan_separation 1 --decay_volume 2.0


    python plot_limits.py --decay_volume 2.5 --radius 1.0
    python plot_limits.py --decay_volume 2.5 --radius 1.0 --minseparation 0.01
    python plot_limits.py --decay_volume 2.5 --radius 1.0 --minseparation 0.02 --excl_list 1293342293
    python plot_limits.py --decay_volume 2.5 --radius 1.0 --minseparation 0.05

    python plot_2D_contour.py --radius 1.0 --scan_separation 1 --decay_volume 2.5


Copy plots to the etp webpage:

    mkdir -p /etpwww/web/ntrevisa/public_html/2023_07_24/

    cp -r  signal_plots /etpwww/web/ntrevisa/public_html/2023_07_24/
    python gallery.py /etpwww/web/ntrevisa/public_html/2023_07_24/

Plots will be visible at:

    https://etpwww.etp.kit.edu/~ntrevisa/2023_07_24/

### Copy your plots on the web

General instructions:

    mkdir -p /etpwww/web/<your_login_name>/public_html/<your_web_directory>/

    cp -r e0ppw_3_0  /etpwww/web/<your_login_name>/public_html/<your_web_directory>/
    python gallery.py /etpwww/web/<your_login_name>/public_html/<your_web_directory>/e0ppw_3_0

    cp -r e0ppw_7_0  /etpwww/web/<your_login_name>/public_html/<your_web_directory>/
    python gallery.py /etpwww/web/<your_login_name>/public_html/<your_web_directory>/e0ppw_7_0

Some specific examples:

    mkdir -p /etpwww/web/ntrevisa/public_html/2022_08_11/

    cp -r e0ppw_3_0  /etpwww/web/ntrevisa/public_html/2022_08_11/
    python gallery.py /etpwww/web/ntrevisa/public_html/2022_08_11/e0ppw_3_0/

    cp -r e0ppw_7_0  /etpwww/web/ntrevisa/public_html/2022_08_11/
    python gallery.py /etpwww/web/ntrevisa/public_html/2022_08_11/e0ppw_7_0/

    cp -r phase1_npod_test/ /etpwww/web/ntrevisa/public_html/2022_08_11/
    python gallery.py /etpwww/web/ntrevisa/public_html/2022_08_11/phase1_npod_test/

    cp -r plots_test/ /etpwww/web/ntrevisa/public_html/2022_08_11/
    python gallery.py /etpwww/web/ntrevisa/public_html/2022_08_11/plots_test/


    mkdir -p /etpwww/web/ntrevisa/public_html/2023_02_21/

    cp -r plots_extrapolation /etpwww/web/ntrevisa/public_html/2023_02_21/
    python gallery.py         /etpwww/web/ntrevisa/public_html/2023_02_21/plots_extrapolation/


Plots will be visible at:

    https://etpwww.etp.kit.edu/~<your_login_name>/<your_web_directory>/e0ppw_3_0/
    https://etpwww.etp.kit.edu/~<your_login_name>/<your_web_directory>/e0ppw_7_0/
    https://etpwww.etp.kit.edu/~<your_login_name>/<your_web_directory>/e0ppw_7_0/
    https://etpwww.etp.kit.edu/~<your_login_name>/<your_web_directory>/phase1_npod_test/
    https://etpwww.etp.kit.edu/~<your_login_name>/<your_web_directory>/plots_test/

In our example case:

    https://etpwww.etp.kit.edu/~ntrevisa/2022_08_11/e0ppw_3_0/
    https://etpwww.etp.kit.edu/~ntrevisa/2022_08_11/e0ppw_7_0/
    https://etpwww.etp.kit.edu/~ntrevisa/2022_08_11/phase1_npod_test/
    https://etpwww.etp.kit.edu/~ntrevisa/2022_08_11/plots_test/