# LUXE-NPOD

Repository with code for LUXE-NPOD studies

### Copy your plots on the web

General instructions:

    mkdir -p /etpwww/web/<your_login_name>/public_html/<your_web_directory>/

    cp -r e0ppw_3_0  /etpwww/web/<your_login_name>/public_html/<your_web_directory>/
    python gallery.py /etpwww/web/<your_login_name>/public_html/<your_web_directory>/e0ppw_3_0

    cp -r e0ppw_7_0  /etpwww/web/<your_login_name>/public_html/<your_web_directory>/
    python gallery.py /etpwww/web/<your_login_name>/public_html/<your_web_directory>/e0ppw_7_0

One specific example:

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

### Post-process G4 simulation files

    python submit_RDF_jobs.py --input_file=list_files_tungsten_1000_BX0 --material=tungsten --length=1000 --BX=0
    python submit_RDF_jobs.py --input_file=list_files_tungsten_500_BX1  --material=tungsten --length=500  --BX=1

    python submit_RDF_jobs.py --input_file=list_files_lead_1000_BX4     --material=lead     --length=1000 --BX=4

    python submit_RDF_jobs.py --input_file=list_files_copper_1000_BX3   --material=copper   --length=1000 --BX=3

    python submit_RDF_jobs.py --input_file=list_files_npod_old          --material=copper   --length=1000 --BX=OLD

### Produce plots running on post-processed rootfiles

    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=1000 --BX=1 --number=0
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=1000 --BX=1 --number=0

    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=tungsten --length=500 --BX=1 --number=1
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=tungsten --length=500 --BX=1 --number=1


    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=lead --length=1000 --BX=1 --number=4
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=lead --length=1000 --BX=1 --number=4


    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=copper --length=1000 --BX=1 --number=3
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=copper --length=1000 --BX=1 --number=3

    python mkPlot.py --input_folder=rootfiles --particle=Photons  --material=copper --length=1000 --BX=1 --number=OLD
    python mkPlot.py --input_folder=rootfiles --particle=Neutrons --material=copper --length=1000 --BX=1 --number=OLD
