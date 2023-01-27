'''
### Documentation:
https://root.cern.ch/doc/master/group__tutorial__dataframe.html
https://root.cern/doc/master/classROOT_1_1RDataFrame.html

### Before using:
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh
'''

import ROOT

import os, sys
import optparse

# from list_files_e1npod_0_5_165gev_cv9qgsphp_tv33_hv1_9 import list_files

# df = ROOT.RDataFrame("Tracks", "/ceph/ferber/LUXE/ptarmigan-v0.8.1/e-laser/phase0/ppw/e0ppw_7_0_0_particles_g4.root")
# df = ROOT.RDataFrame("Tracks", ["/ceph/rquishpe/luxe/npod/lx_npod_ce5bc8d0/tungsten/run_dumpZ_1000_BXs_0/luxe_npod_signal_e1npod_0_5_165gev_cv9qgsphp_tv33_hv1_0_100.root",])
#                                "/ceph/rquishpe/luxe/npod/lx_npod_ce5bc8d0/tungsten/run_dumpZ_1000_BXs_0/luxe_npod_signal_e1npod_0_5_165gev_cv9qgsphp_tv33_hv1_0_101.root"])

#df = ROOT.RDataFrame("Tracks", list_files)

# Options parsing
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
    
parser.add_option('--input_file', dest='input_file', help='Input rootfile',          default='DEFAULT') 
parser.add_option('--material',   dest='material',   help='Dump material',           default='tungsten') 
parser.add_option('--length',     dest='length',     help='Dump length',             default='1000') 
parser.add_option('--BX',         dest='BX',         help='Bunch crossing',          default='0') 
parser.add_option('--number',     dest='number',     help='Progressing file number', default='1') 

# Assigning variables to the inputs
(opt, args) = parser.parse_args()

input_file = opt.input_file
material   = opt.material
length     = opt.length
BX         = opt.BX
number     = opt.number

# Summary of inputs
print("Input file:     {}".format(opt.input_file))
print("Dump material:  {}".format(opt.material))
print("Dump length:    {}".format(opt.length))
print("Bunch crossing: {}".format(opt.BX))
print("File number:    {}".format(opt.number))

df = ROOT.RDataFrame("Tracks", input_file)
print(df.GetColumnNames())

####################
# Main RDF filtering
####################

# https://root.cern/doc/master/classROOT_1_1VecOps_1_1RVec.html
# "E", "pdg","detid","weight","theta","phi","vtxx","vtxy","vtxz","px","py","pz","x","y","z","t"
df2 = df.Define("mask",     "detid == 9000 && sqrt(x*x+y*y)< 1000.0") \
        .Redefine("E",      "E[mask]")       \
        .Redefine("pdg",    "pdg[mask]")     \
        .Redefine("theta",  "theta[mask]")   \
        .Redefine("phi",    "phi[mask]")     \
        .Redefine("vtxx",   "vtxx[mask]")    \
        .Redefine("vtxy",   "vtxy[mask]")    \
        .Redefine("vtxz",   "vtxz[mask]")    \
        .Redefine("px",     "px[mask]")      \
        .Redefine("py",     "py[mask]")      \
        .Redefine("pz",     "pz[mask]")      \
        .Redefine("x",      "x[mask]")       \
        .Redefine("y",      "y[mask]")       \
        .Redefine("z",      "z[mask]")       \
        .Redefine("xlocal", "xlocal[mask]")  \
        .Redefine("ylocal", "ylocal[mask]")  \
        .Redefine("zlocal", "zlocal[mask]")  \
        .Redefine("t",      "t[mask]")       \
        .Redefine("detid",  "detid[mask]")   \
#        .Redefine("weight", "weight[mask]")  \
# && E > 0.5") \

# a1 = df2.Display({"detid","mask","E","slim_E"})
a2 = df2.Display({"detid","E","x","y","pdg"})
a2.Print()

# (abs(df_tmp["z"]-16000) < 0.1) & (abs(df_tmp["x"]) < 999.0) & (abs(df_tmp["y"]) < 999.0) & (df_tmp["E"]>energy_cut)
filter_tot_energy = "Sum(E) > 0"
filter_E          = "E > 0.5"
df3 = df2.Filter(filter_tot_energy)

a3 = df3.Display({"detid","E","x","y","pdg"})
a3.Print()

entries3 = df3.Count()
print('{} entries passed all filters'.format(entries3.GetValue()))


#######################
# Preparing Photons RDF
#######################

# filter_photon = "pdg == 22"
# df_photons = df3.Filter(filter_photon)

det_position = "16000"
if length == "LegacyCfg": det_position = "17130"

df_photons = df.Define("mask",     "detid==9000 && sqrt(x*x+y*y)<1000.0 && pdg==22 && abs(z-{})<0.1".format(det_position)\
               .Redefine("E",      "E[mask]")       \
               .Redefine("pdg",    "pdg[mask]")     \
               .Redefine("theta",  "theta[mask]")   \
               .Redefine("phi",    "phi[mask]")     \
               .Redefine("vtxx",   "vtxx[mask]")    \
               .Redefine("vtxy",   "vtxy[mask]")    \
               .Redefine("vtxz",   "vtxz[mask]")    \
               .Redefine("px",     "px[mask]")      \
               .Redefine("py",     "py[mask]")      \
               .Redefine("pz",     "pz[mask]")      \
               .Redefine("x",      "x[mask]")       \
               .Redefine("y",      "y[mask]")       \
               .Redefine("z",      "z[mask]")       \
               .Redefine("xlocal", "xlocal[mask]")  \
               .Redefine("ylocal", "ylocal[mask]")  \
               .Redefine("zlocal", "zlocal[mask]")  \
               .Redefine("t",      "t[mask]")       \
               .Redefine("detid",  "detid[mask]")   \
               
df_photons_2 = df_photons.Filter(filter_tot_energy)

a_photons = df_photons_2.Display({"detid","E","weight","theta","phi","pdg","t"})
a_photons.Print()

print(df_photons_2.GetColumnNames())

########################
# Preparing Neutrons RDF
########################

df_neutrons = df.Define("mask",    "detid==9000 && sqrt(x*x+y*y)<1000.0 && pdg==2112 && abs(z-{})<0.1".format(det_position)\
               .Redefine("E",      "E[mask]")       \
               .Redefine("pdg",    "pdg[mask]")     \
               .Redefine("theta",  "theta[mask]")   \
               .Redefine("phi",    "phi[mask]")     \
               .Redefine("vtxx",   "vtxx[mask]")    \
               .Redefine("vtxy",   "vtxy[mask]")    \
               .Redefine("vtxz",   "vtxz[mask]")    \
               .Redefine("px",     "px[mask]")      \
               .Redefine("py",     "py[mask]")      \
               .Redefine("pz",     "pz[mask]")      \
               .Redefine("x",      "x[mask]")       \
               .Redefine("y",      "y[mask]")       \
               .Redefine("z",      "z[mask]")       \
               .Redefine("xlocal", "xlocal[mask]")  \
               .Redefine("ylocal", "ylocal[mask]")  \
               .Redefine("zlocal", "zlocal[mask]")  \
               .Redefine("t",      "t[mask]")       \
               .Redefine("detid",  "detid[mask]")   \
               
df_neutrons_2 = df_neutrons.Filter(filter_tot_energy)

a_neutrons = df_neutrons_2.Display({"detid","E","weight","theta","phi","pdg","t"})
a_neutrons.Print()

print(df_neutrons_2.GetColumnNames())


##################
# Making snapshots
##################

output_file_name_photons = "rootfiles/Photons_RDF_{}_{}_{}_{}.root".format(material,length,BX,number)
df_photons_2.Snapshot("Tracks", output_file_name_photons, ["E","pdg","detid","weight","theta","phi","vtxx","vtxy","vtxz","px","py","pz","x","y","z","t"])
# df_photons_2.Snapshot("Tracks", "Photons_RDF.root")

output_file_name_neutrons = "rootfiles/Neutrons_RDF_{}_{}_{}_{}.root".format(material,length,BX,number)
df_neutrons_2.Snapshot("Tracks", output_file_name_neutrons, ["E","pdg","detid","weight","theta","phi","vtxx","vtxy","vtxz","px","py","pz","x","y","z","t"])
# df_neutrons_2.Snapshot("Tracks", "Neutrons_RDF.root")

