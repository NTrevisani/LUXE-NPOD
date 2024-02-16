# LUXE Signal Distributions

Scripts to produce signal distributions for the LUXE-NPOD experiment (ALP -> $\gamma \gamma$).

The code uses some assumptions:
- the detector is always 100% efficient in detecting the photons hitting its surface
- the two photons produced by the ALP decay reach the detector only if the decay happens in the decay volume

The basic script is:

    read_signal.py

The script will usually run on several sets of parameters values, listed in files like:

    run_condor.sh 

To submit the jobs to condor, use:

   condor_submit submit_htc.jdl

The output will be sent to:

    /storage/9/rquishpe/luxe/npod/phase1/signal/LUXE-NPOD/output_condor/