# Prepare jobs submission for RDF_test.py

import os, sys
import optparse

import importlib

# Options parsing
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
    
parser.add_option('--input_file', dest='input_file', help='List of input rootfiles', default='DEFAULT') 
parser.add_option('--material',   dest='material',   help='Dump material',           default='tungsten') 
parser.add_option('--length',     dest='length',     help='Dump length',             default='1000') 
parser.add_option('--BX',         dest='BX',         help='Bunch crossing',          default='0') 
# parser.add_option('--number',     dest='number',     help='Progressing file number', default='100') 

# Assigning variables to the inputs
(opt, args) = parser.parse_args()

input_file = opt.input_file
material   = opt.material
length     = opt.length
BX         = opt.BX
# number     = opt.number

# Summary of inputs
print("Input file:     {}".format(opt.input_file))
print("Dump material:  {}".format(opt.material))
print("Dump length:    {}".format(opt.length))
print("Bunch crossing: {}".format(opt.BX))
# print("File number:    {}".format(opt.number))

my_module = importlib.import_module(input_file)
print(my_module.list_files)

cwd = os.getcwd()
print("Current working directory: {}".format(cwd))

os.system("mkdir -p script")

i = 0
for rf in my_module.list_files:
    print(i,rf)
    i = i+1

    output_file_name = "script/submit_{}_{}_{}_{}".format(material,length,BX,i)

    # Write .sh file
    with open(output_file_name + ".sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh\n")
        f.write("cd {}\n".format(cwd))
        f.write("python {}/RDF_test.py --input_file={} --material={} --length={} --BX={} --number={}".format(cwd,rf,material,length,BX,i))

    # Write .jds file
    with open(output_file_name + ".jds", "w") as f:
        f.write("Universe = docker\n")
        f.write("docker_image = mschnepf/slc7-condocker\n")
        f.write("Executable = {}.sh\n".format(output_file_name)) # /work/ntrevisa/scripts/jobs//mkShapes__LeptonMVA_studies_UL/mkShapes__LeptonMVA_studies_UL__ALL__WJets_LO_UL.0.sh
        f.write("Output = {}.out\n".format(output_file_name))    # /work/ntrevisa/scripts/jobs//mkShapes__LeptonMVA_studies_UL/mkShapes__LeptonMVA_studies_UL__ALL__WJets_LO_UL.0.out
        f.write("Error = {}.err\n".format(output_file_name))     # /work/ntrevisa/scripts/jobs//mkShapes__LeptonMVA_studies_UL/mkShapes__LeptonMVA_studies_UL__ALL__WJets_LO_UL.0.err
        f.write("Log = {}.log\n".format(output_file_name))       # /work/ntrevisa/scripts/jobs//mkShapes__LeptonMVA_studies_UL/mkShapes__LeptonMVA_studies_UL__ALL__WJets_LO_UL.0.log
        f.write("x509userproxy = /tmp/x509up_u12054\n")
        f.write("request_cpus = 1\n")
        f.write("RequestMemory = 8192\n") 
        f.write("request_disk = 10000000\n")
        f.write("accounting_group = cms.higgs\n")
        f.write("JobBatchName = mkShapes__LeptonMVA_studies_UL__ALL\n")
        f.write("Queue\n")
