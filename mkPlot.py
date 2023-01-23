'''
### What is missing:
- A function to make the plots

### Documentation:
https://root.cern.ch/doc/master/group__tutorial__dataframe.html
https://root.cern/doc/master/classROOT_1_1RDataFrame.html

### Before using:
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh
'''

import ROOT

import os, sys
import optparse

import tdrStyle as tdrStyle
tdrStyle.setTDRStyle()

# Plotting function
def plot_histo(rdf, variable, bins, min_x, max_x, weight="1", title="", x_label="", y_label="", file_name=None, folder_name=None, file_format="png", y_log=False):
    """Plot distributions from dataframe.

    Arguments:
    rdf: input rdataframe
    variable: distribution to plot
    title: appears on top of the plot
    weight: weight to apply to the histogram
    bins: number of bins
    range: x-axis range (tuple)
    x_label: label of x-axis
    y_label: label of y-axis
    file_name: if not empty, name of file where plot is printed
    folder_name: if not empty, name of directory where plot is printed
    file_format: if file_name not empty, format of output file
    """
    
    histogram = rdf.Define("w",weight).Histo1D((variable, title, bins, min_x, max_x), variable, "w")

    histogram.GetXaxis().SetTitle(x_label)
    histogram.GetYaxis().SetTitle(y_label)

    # output_name = "{}_{}_{}_Energy.png".format(particle,material,length)
    
    output_name = file_name

    c1 = ROOT.TCanvas()
    # histogram.Draw("hist")
    c1.SetTitle(title)
    histogram.SetMarkerColor(ROOT.kBlue)
    histogram.Draw()
    if y_log == True:
        c1.SetLogy()
        output_name =  "log_" + output_name
        
    if folder_name:
        os.system("mkdir -p {}".format(folder_name))
        output_name = folder_name + "/" + output_name

    c1.SaveAs(output_name + "." + file_format)
    
    # output_name = "plots/log_{}_{}_{}_Energy.png".format(particle,material,length)
    # log_c1 = ROOT.TCanvas()
    # Energy.GetYaxis().SetRangeUser(1.,1e8)
    # Energy.Draw("hist")
    # log_c1.SaveAs(output_name)


# Options parsing
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
    
parser.add_option('--input_folder', dest='input_folder', help='Directory with input rootfiles', default='rootfiles') 
parser.add_option('--particle',     dest='particle',     help='Particle to inspect',            default='Photons') 
parser.add_option('--material',     dest='material',     help='Dump material',                  default='tungsten') 
parser.add_option('--length',       dest='length',       help='Dump length',                    default='1000') 
parser.add_option('--BX',           dest='BX',           help='Number of bunch crossings',      default='1') 
parser.add_option('--number',       dest='number',       help='Progressing file number',        default='0') 

# Assigning variables to the inputs
(opt, args) = parser.parse_args()

sys.argv.append( '-b' )
ROOT.gROOT.SetBatch()
    
input_folder = opt.input_folder
particle     = opt.particle
material     = opt.material
length       = opt.length
BX           = opt.BX
number       = opt.number

if BX == 0:
    raise ValueError("We must have at least 1 BX !!")

# Summary of inputs
print("Input folder:   {}".format(opt.input_folder))
print("Particle:       {}".format(opt.particle))
print("Dump material:  {}".format(opt.material))
print("Dump length:    {}".format(opt.length))
print("Bunch crossing: {}".format(opt.BX))
print("File number:    {}".format(opt.number))

# Open rootfiles
################
my_file = "{}/{}_RDF_{}_{}{}.root".format(input_folder,particle,material,length,number)

df = ROOT.RDataFrame("Tracks", my_file)
print(df.GetColumnNames())

det_position = "16000"
if length == "LegacyCfg": det_position = "17130"

# We are currently assuming we used a factor 10 less photons than required, but it is not true.
# We thus adjust the per-event weight, dividing it by 10
weight_adjust = 0.1

# Start plotting - do we want to move the actual list of plots in a separated dictionary and leave here only a loop on the dictionary items?
plot_histo(df, "E", 150, 0., 15., weight="{}*(E>0 && abs(z-{})<0.1)*weight/{}".format(weight_adjust,det_position,BX), title="Energy", x_label="Energy [GeV]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_Energy".format(particle,material,length))
plot_histo(df, "E", 150, 0., 15., weight="{}*(E>0 && abs(z-{})<0.1)*weight/{}".format(weight_adjust,det_position,BX), title="Energy", x_label="Energy [GeV]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_Energy".format(particle,material,length), y_log=True)

plot_histo(df, "E", 40, 0., 2., weight="{}*(E>0 && abs(z-{})<0.1)*weight/{}".format(weight_adjust,det_position,BX), title="Energy", x_label="Energy [GeV]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_Energy_zoom".format(particle,material,length))
plot_histo(df, "E", 40, 0., 2., weight="{}*(E>0 && abs(z-{})<0.1)*weight/{}".format(weight_adjust,det_position,BX), title="Energy", x_label="Energy [GeV]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_Energy_zoom".format(particle,material,length), y_log=True)

plot_histo(df, "t", 150, 0., 15., weight="{}*(E>0 && abs(z-{})<0.1)*weight/{}".format(weight_adjust,det_position,BX), title="Time of Arrival", x_label="Time of arrival [ns]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_time".format(particle,material,length))
plot_histo(df, "t", 150, 0., 15., weight="{}*(E>0 && abs(z-{})<0.1)*weight/{}".format(weight_adjust,det_position,BX), title="Time of Arrival", x_label="Time of arrival [ns]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_time".format(particle,material,length), y_log=True)


plot_histo(df, "vtxz", 1400, 5000.0, 19000.0, "{}*weight*(detid==9000 && sqrt(vtxx*vtxx+vtxy*vtxy)<300.0)/{}".format(weight_adjust,BX), title="Vertex z position for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo".format(particle,material,length))
plot_histo(df, "vtxz", 1400, 5000.0, 19000.0, "{}*weight*(detid==9000 && sqrt(vtxx*vtxx+vtxy*vtxy)<300.0)/{}".format(weight_adjust,BX), title="Vertex z position for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo".format(particle,material,length), y_log=True)

plot_histo(df, "vtxz", 1400, 5000.0, 19000.0, "{}*weight*(detid==9000 && sqrt(vtxx*vtxx+vtxy*vtxy)<300.0)/{}".format(weight_adjust,BX), title="Vertex z position for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo_concreteStructure".format(particle,material,length))
plot_histo(df, "vtxz", 1400, 5000.0, 19000.0, "{}*weight*(detid==9000 && sqrt(vtxx*vtxx+vtxy*vtxy)<300.0)/{}".format(weight_adjust,BX), title="Vertex z position for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo_concreteStructure".format(particle,material,length), y_log=True)


plot_histo(df, "vtxz", 100, 13630.0, 14630.0, "{}*weight*(detid==9000 && sqrt(vtxx*vtxx+vtxy*vtxy)<300.0)/{}".format(weight_adjust,BX), title="Vertex z position in the dump for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo_zoom".format(particle,material,length))
plot_histo(df, "vtxz", 100, 13630.0, 14630.0, "{}*weight*(detid==9000 && sqrt(vtxx*vtxx+vtxy*vtxy)<300.0)/{}".format(weight_adjust,BX), title="Vertex z position in the dump for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo_zoom".format(particle,material,length), y_log=True)

plot_histo(df, "vtxz", 100, 13630.0, 14630.0, "{}*weight*(detid==9000)/{}".format(weight_adjust,BX), title="Vertex z position in the dump for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo_zoom_concreteStructure".format(particle,material,length))
plot_histo(df, "vtxz", 100, 13630.0, 14630.0, "{}*weight*(detid==9000)/{}".format(weight_adjust,BX), title="Vertex z position in the dump for particles reaching the BSM detector", x_label="Vertex z position [mm]", y_label="Particles/bin", folder_name="plots_test", file_name="{}_{}_{}_vtxz_BSM_calo_zoom_concreteStructure".format(particle,material,length), y_log=True)
