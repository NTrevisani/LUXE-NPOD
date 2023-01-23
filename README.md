# LUXE-NPOD

Repository with code for LUXE-NPOD studies

### Before starting

Sourse required to use RDataFrame:

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