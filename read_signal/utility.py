from random import randint, randrange
from glob import glob
import re, os, vector, time, uproot
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import sys

import multiprocessing
from multiprocessing import Pool

cmap = mpl.cm.get_cmap('viridis_r')

# find closest value in in list, needed do get the right mass files for given user input
def closest_in_list(lst, K):     
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def find_nearest_index(lst, value, tolerance = 1e-3):
    array = np.asarray(lst)
    idx = (np.abs(array - value)).argmin()
    
    # check if this value is really near
    if np.abs(array[idx] - value) > tolerance:
        print(f'WARNING: find_nearest_index could not find nearest value within tolerance ({tolerance}), returning -1')
        return -1
    
    return idx

def lifetime(mass, lam):
    width = mass**3 / (64 * np.pi * lam**2 )
    hbarc = 197.3269804 * 1e-3 * 1e-15 #fm MeV, https://pdg.lbl.gov/2019/reviews/rpp2019-rev-phys-constants.pdf
    ctau =  hbarc/width # tau =hbar/width, ctau = hbarc/width

    return width, ctau


def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-9):
 
    ndotu = planeNormal.dot(rayDirection)
    if abs(ndotu) < epsilon:
        print(epsilon)
        return None, None
        # raise RuntimeError("no intersection or line is within plane")

    w = rayPoint - planePoint
    si = -planeNormal.dot(w) / ndotu #if si is negative, the ray points backwards (i.e. unphysical)
    Psi = w + si * rayDirection + planePoint

    return Psi, si

def read_rootfile(ff, dtype=np.float32):
            
    arr_alps = np.zeros((10000,4), dtype=dtype)
    arr_photons = np.zeros((20000,4), dtype=dtype)

    with uproot.open(ff[1]) as rootfile:
        
        print('reading', ff[1])

        #this will each create a akward array of arrays
        tree_particle = rootfile["LHEF"]["Particle"]
        list_px = tree_particle["Particle.Px"].array()
        list_py = tree_particle["Particle.Py"].array()
        list_pz = tree_particle["Particle.Pz"].array()
        list_E = tree_particle["Particle.E"].array()
        list_status = tree_particle["Particle.Status"].array()
        list_pdg = tree_particle["Particle.PID"].array()

        # loop over events
        for evt, (lpx, lpy, lpz, lE, lstatus, lpdg) in enumerate(zip(list_px, list_py, list_pz, list_E, list_status, list_pdg)):

            # loop over particles in events
            list_photons = []
            nphot = 0
            for px, py, pz, E, status, pdg in zip(lpx, lpy, lpz, lE, lstatus, lpdg):
                if (status == 1) & ( pdg == 22):
                    p4 = vector.obj(px=px, py=py, pz=pz, E=E)
                    list_photons.append(p4)
                    
                    arr_photons[evt*2+nphot] = [px, py, pz, E]
                    nphot += 1

            p4_alp = list_photons[-1] + list_photons[-2]
            arr_alps[evt] = [p4_alp.px, p4_alp.py, p4_alp.pz, p4_alp.E]
            
        return ff[0], [arr_alps, arr_photons]

    
def read_rootfiles(list_energies_rootfiles, ncpu=40, debug=False, timing=False, dtype=np.float32):
    
    ncpu_available = int(multiprocessing.cpu_count())
    
    print(f'Reading rootfiles:')
    print(f'  {ncpu_available} CPU cores available')
    print(f'  {ncpu} CPU cores used')
    
    if ncpu > 1:
        print(f'using multi-processing')
        pool = Pool(processes=ncpu) 
        
        results = pool.map(read_rootfile, list_energies_rootfiles)
        
    else:
        print(f'using single core processing')
        results = []
        for file in list_energies_rootfiles:
            
            
            if debug is True:
                if np.abs(file[0] - 2.1) < 1e-5:
                    results.append(read_rootfile(file, dtype))
                    break
            else:
                results.append(read_rootfile(file, dtype))
            
    print(f'done.')
    
    return results
    
    
# output directory for pictures
def make_random_dir(n = 10):
    
    directory = ''
    if n > 0:
        random_number = ''.join(['{}'.format(randint(0, 9)) for num in range(0, n)])
        directory = 'luxe_' + random_number
    return directory

def create_output_directory(suffix, nrand=0, parent_dir = '/home/ferber/work_dir/luxe_plots'):

    #create directory name
    save_dir = os.path.join(parent_dir, make_random_dir(nrand))
    save_dir = save_dir + suffix
    print(f'create_output_directory: {save_dir}')

    #check if it exists
    while True:
        exists = os.path.exists(save_dir)
        if exists:
            sleep(1)
        else:
            os.makedirs(save_dir)
            break
    
    return save_dir

# get list of all cross sections
def get_xsec(filename):
    searchfile = open(filename, "r")
    findline = None
    for line in searchfile:
        if "Integrated weight" in line:
            findline = line
            break
    searchfile.close()
    return(findline)

def get_cross_sections(input_banner_dir, mass):
    list_energies_xsec = []

    xsec_foldername = os.path.join(input_banner_dir, 'mass' + str(mass) + 'GeV')
    xsec_list_files = glob(os.path.join(xsec_foldername, '*'),recursive = True)
    xsec_templist_normfiles = [os.path.basename(os.path.normpath(x)) for x in xsec_list_files]

    # get a list of all simulated photon energies and the respective xsec
    xsec_list_energies = [[float(re.search('_beam(.*)GeV_', x).group(1)), os.path.join(xsec_foldername, x)] for x in xsec_templist_normfiles]

    for ll in xsec_list_energies:
        line = get_xsec(ll[1])
        xsec = 0.0
        if line is not None:
            xsec = float(line.split()[-1])
        list_energies_xsec.append([ll[0], xsec])
        
    return list_energies_xsec


def read_photon_spectrum(file = '', tree='h_all', save_dir = '', N_e=0, plot=True, scale = 1.):

    with uproot.open(file) as rootfile:
        h1 = rootfile[tree].to_numpy()
        h1 = (h1[0] * scale, h1[1])
        
        # h1_phase0_ppw_xi_7_0 = rootfile['luxe_primary_photons_physical_dump_pos/energy_high_res/histo_Bkg_phase0_ppw_xi_7_0'].to_numpy()
        # h1_phase0_ppw_xi_7_0 = (h1_phase0_ppw_xi_7_0[0] * scale, h1_phase0_ppw_xi_7_0[1])

    xmin = h1[1][0]
    xmax = h1[1][-1]
    
    if plot:
        fig, ax = plt.subplots()
        ax.step(h1[1][:-1], h1[0]*N_e, label=tree, color='darkblue')
        # ax.step(h1_phase0_ppw_xi_7_0[1][:-1], h1_phase0_ppw_xi_7_0[0]*N_e, label=r'$\xi$=7.0', color='red')
        ax.set_yscale('log')
        ax.set_xlabel('Energy (GeV)')
        ax.set_ylabel('photons / BX')
        ax.set_xlim(xmin, xmax)
        # ax.set_ylim(1e-7, 1)
        ax.legend()

        plt.savefig(os.path.join(save_dir, 'photon_spectrum.pdf'), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box
    
    list_weights = []
    list_bincenters = []
    # for h1_laser in [h1_phase0_ppw_xi_3_0, h1_phase0_ppw_xi_7_0]:
    # rebin the histogram by 2, drop first bin
    list_weights_temp = []
    list_bincenters_temp = []
    for idx in range(1, len(h1[0])-1, 2): #increment in steps of 2
        bincenter = h1[1][idx+1]
        val = h1[0][idx]+h1[0][idx+1]
        list_weights_temp.append(val)
        list_bincenters_temp.append(bincenter)
    list_weights.append(list_weights_temp)
    list_bincenters.append(list_bincenters_temp)
    
    return h1, list_bincenters, list_weights

def get_weights_combined(list_energies_rootfiles, list_xsec, list_bincenters, list_weights):
    
    templist = []
    for idx, val in enumerate(list_energies_rootfiles):

        energy = val[0]
        rootfile = val[1]

        # find cross section (for MG value of coupling)
        list_xsec_0 = [x[0] for x in list_xsec] #need list of all energies in xsec file (can have different order!)
        index = find_nearest_index(list_xsec_0, energy)
        
        xsec = -1.0
        if index >= 0:
            xsec = list_xsec[index][1]

        #find photon weights
        index = find_nearest_index(list_bincenters, energy)
        
        photonweight = -1
        if index >= 0:
            photonweight = list_weights[index]
        
        templist.append([energy, xsec, photonweight, rootfile])
    templist.sort()
    
    return templist

def plot_spectra(list_weights, **plotdict):
    
    if plotdict['plot'] == False:
        return
    
    x = [val[0] for val in list_weights]
    w = [val[2] for val in list_weights]

    fig, ax = plt.subplots()
    ax.scatter(x, w, color='red', s=2, label=plotdict['label'])
    ax.set_yscale('log')
    ax.set_xlabel(plotdict['xlabel'])
    ax.set_ylabel(plotdict['ylabel'])
    ax.legend()

    plt.savefig(os.path.join(plotdict['save_dir'], plotdict['plotname']), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box
    plt.close(fig)
    
def plot_xsec(list_xsec, **plotdict):
    
    if plotdict['plot'] == False:
        return
    
    x = [val[0] for val in list_xsec]
    w = [val[1] for val in list_xsec]

    fig, ax = plt.subplots()
    ax.scatter(x, w, color='red', s=2, label=plotdict['label'])
    ax.set_yscale('log')
    ax.set_xlabel(plotdict['xlabel'])
    ax.set_ylabel(plotdict['ylabel'])
    ax.legend()

    plt.savefig(os.path.join(plotdict['save_dir'], plotdict['plotname']), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box
    plt.close(fig)
    
    
def displace(list_all_temp, mass, distance, target_end, target_length, ctau, r_x, r_y):
    
    # ---------------------------
    # random number generator
    rng = np.random.default_rng()

    # displacement
    list_alp_vtx = []
    list_photon = []

    planeNormal = np.array([0, 0, distance])
    planePoint = np.array([0, 0, distance]) #Any point on the plane

    epsilon = 1e-8
    
    speed_of_light = 299792458 #meter per second

    for idx, (ee, ww, xx, cc, results) in enumerate(list_all_temp):

        start = time.perf_counter()

        # print('in displace() loop')
        # print(idx, ee, ww, xx, cc)
        # print(len(results))
        # print(len(results[0]))
        # print(len(results[1]))
        
        templist_vtx = []
        templist_photon = []
        
        la = results[0]
        lg = results[1]
        
        for p in la:
            
            mag = np.sqrt(p[0]**2 + p[1]**2 + p[2]**2) #3-vector magnitude
            beta = mag / p[3] #lorentz beta
            gamma = 1./np.sqrt(1-beta*beta) #lorentz gamma

            decay_length = ctau * gamma
            
            d = rng.exponential(decay_length)
            decay_z = target_end - target_length + p[2]/mag*d

            if decay_z > target_end and decay_z < distance:
                # prod_x = rng.normal(loc=0, scale=r_x)
                # prod_y = rng.normal(loc=0, scale=r_y)            
                decay_x = rng.normal(loc=0, scale=r_x) + p[0]/mag*d
                decay_y = rng.normal(loc=0, scale=r_y) + p[1]/mag*d
                decay_time = d / (beta * speed_of_light) / 1e-9
                # print(p.to_beta3().unit())
                # print(d)
                # print(f'ALP x: {prod_x}->{decay_x}, y: {prod_y}->{decay_y}, z: {prod_z}->{decay_z}, t: {decay_time}, beta={p.beta}')
                templist_vtx.append([decay_x, decay_y, decay_z, d, decay_time])    
                
        stop_1 = time.perf_counter()
        # print(f'time_1 = {stop_1-start}')

        for idx, vtx in enumerate(templist_vtx):

            intercept1, si1 = LinePlaneCollision(planeNormal, planePoint, 
                                            np.array([lg[idx*2][0], lg[idx*2][1], lg[idx*2][2]]), 
                                            np.array([vtx[0], vtx[1], vtx[2]]), epsilon=epsilon)

            intercept2, si2 = LinePlaneCollision(planeNormal, planePoint, 
                                            np.array([lg[idx*2+1][0], lg[idx*2+1][1], lg[idx*2+1][2]]), 
                                            np.array([vtx[0], vtx[1], vtx[2]]), epsilon=epsilon)

            if si1 is None or  si1 < 0:
                intercept1 = None

            if si2 is None or si2 < 0:
                intercept2 = None

            dist = 1e10
            r1 = 1e10
            r2 = 1e10
            i1_x = 1e10
            i1_y = 1e10
            i2_x = 1e10
            i2_y = 1e10
            t1 = 1e10
            t2 = 1e10

            if intercept1 is not None and intercept2 is not None:
                dist = np.sqrt((intercept1[0]-intercept2[0])**2 + (intercept1[1]-intercept2[1])**2)
                
                r1 = np.sqrt(intercept1[0]**2 + intercept1[1]**2)
                r2 = np.sqrt(intercept2[0]**2 + intercept2[1]**2)    
                
                i1_x = intercept1[0]
                i1_y = intercept1[1]
                i2_x = intercept2[0]
                i2_y = intercept2[1]
                
                d1 = np.sqrt((i1_x-vtx[0])**2 + (i1_y-vtx[1])**2 + (distance-vtx[2])**2)
                # p1 = lg[idx*2]
                p1 = vector.obj(px=lg[idx*2][0], py=lg[idx*2][1], pz=lg[idx*2][2], E=lg[idx*2][3])
                t1 = d1 / (p1.beta * speed_of_light) / 1e-9 + vtx[4] #arrival time at detector
                
                d2 = np.sqrt((i2_x-vtx[0])**2 + (i2_y-vtx[1])**2 + (distance-vtx[2])**2)
                # p2 = lg[idx*2+1]
                p2 = vector.obj(px=lg[idx*2+1][0], py=lg[idx*2+1][1], pz=lg[idx*2+1][2], E=lg[idx*2+1][3])
                t2 = d2 / (p2.beta * speed_of_light) / 1e-9 + vtx[4] #arrival time at detector
                
                # print(f'gamma1 t: {t1}, beta={p1.beta}')
                # print(f'gamma2 t: {t2}, beta={p2.beta}')
                

            templist_photon.append([dist, r1, r2, lg[idx*2][3], lg[idx*2+1][3], i1_x, i1_y, i2_x, i2_y, t1, t2])

        list_alp_vtx.append(templist_vtx)
        list_photon.append(templist_photon)
        
        stop_2 = time.perf_counter()
        # print(f'time_2 = {stop_2-stop_1}')
        # print(f'time_total = {stop_2-start}')
        
    return list_alp_vtx, list_photon
        
def plot_cumulative_pair(list_particles, entryid1, entryid2, list_all_temp, list_mask, plotdict, metadict, plot_log = False):
    
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    bins = np.linspace(plotdict['xmin'], plotdict['xmax'], plotdict['nbins'])
    binwidth = bins[1]-bins[0]

    energy_range = [list_all_temp[0][0]*0.9, list_all_temp[-1][0]*1.1]
    delta_energy = energy_range[-1]-energy_range[0]
    
    list_x = []
    list_weights = []
    list_color = []
    
    for idx, _ in enumerate(list_all_temp):
 
        if len( list_particles[idx]) == 0:
            print(f'WARNING: plot_histogram, list_particles[{idx}] is empty')
            continue

        x1 = np.array([x[entryid1] for x in list_particles[idx]])
        x1 = x1[list_mask[idx]]
        x2 = np.array([x[entryid2] for x in list_particles[idx]])
        x2 = x2[list_mask[idx]]
        
        x = np.maximum(x1, x2)
        
        # energy, weight, xsec_scaled, ctau, results
        n_gamma = list_all_temp[idx][1] # gammas per incoming electron in energy window
        xsec_scaled = list_all_temp[idx][2] #cross section scaled for coupling

        n_exp = n_gamma * xsec_scaled * metadict['L_eff_pb'] #how many events are expected from this incoming photon energy bin
        w = n_exp/metadict['n_mg']

        list_x.append(x)
        list_weights.append(np.ones(len(x))*w)
        list_color.append(cmap((list_all_temp[idx][0]-energy_range[0])/delta_energy)) #color [0..1] in selected range

    # for some couplings, there will be zero events (since the lifetime is too short)
    if len(list_x) == 0:
        return None, None

    # draw stacked histogram
    a, b, c = axs.hist(list_x, bins=bins, weights=list_weights, 
                           histtype='stepfilled', stacked=True, 
                           color=list_color, lw=0)

    all_vtx_z = np.concatenate(list_x)
    all_vtx_z_weights = np.concatenate(list_weights)
    a_full, b_full, c_full = axs.hist(all_vtx_z, bins=bins, weights=all_vtx_z_weights, 
                           histtype='step', 
                           lw=2, color='black')

    axs.set_xlabel(plotdict['xlabel'])
    axs.set_ylabel(r'Entries / {:.4f} {}'.format(binwidth, plotdict['ylabel_unit']))
    axs.set_xlim(plotdict['xmin'], plotdict['xmax'])

    #colorbar
    normalize = mcolors.Normalize(vmin=list_all_temp[0][0]*0.9, vmax=list_all_temp[-1][0]*1.1)
    scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=cmap)
    cbar = plt.colorbar(scalarmappaple)
    cbar.set_label('Incoming $E_{\gamma}$ [GeV]')

    _ = axs.text(0.975, 0.925, r'$\Lambda^{{-1}}$={} GeV$^{{-1}}$, $m_{{a}}={}$ GeV'.format(metadict['lam_inv'], metadict['mass']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)
    _ = axs.text(0.975, 0.875, r'{}, $n_{{BX}}$={:4.2e}'.format(metadict['laserconfig'], metadict['N_bx']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)
    _ = axs.text(0.975, 0.825, r'$L_{{V}}$={}m, $L_{{D}}$={}m'.format(metadict['distance'], metadict['target_length']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)
    _ = axs.text(0.975, 0.755, r'$E_{{\gamma}}$>{}GeV'.format(metadict['min_energy']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)

    np.save(os.path.join(plotdict['save_dir'], plotdict['filename']), { 'entries': a_full, 'bins': b_full, 'xlabel': axs.get_xlabel(), 'ylabel': axs.get_ylabel(), 'xrange': [plotdict['xmin'], plotdict['xmax']]})
    plt.savefig(os.path.join(plotdict['save_dir'], plotdict['plotname']), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box
    
    if plot_log:
        axs.set_yscale('log')
        plt.savefig(os.path.join(plotdict['save_dir'], 'log_'+plotdict['plotname']), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box

        
    plt.close(fig)
    
    return a_full, b_full    
    
    
    
def plot_histogram(list_particles, entryid, list_all_temp, list_mask, plotdict, metadict):
    
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    bins = np.linspace(plotdict['xmin'], plotdict['xmax'], plotdict['nbins'])
    binwidth = bins[1]-bins[0]

    energy_range = [list_all_temp[0][0]*0.9, list_all_temp[-1][0]*1.1]
    delta_energy = energy_range[-1]-energy_range[0]
    
    list_x = []
    list_weights = []
    list_color = []
    
    for idx, _ in enumerate(list_all_temp):
 
        if len( list_particles[idx]) == 0:
            print(f'WARNING: plot_histogram, list_particles[{idx}] is empty')
            continue

        x = np.array([x[entryid] for x in list_particles[idx]])
        x = x[list_mask[idx]]

        # energy, weight, xsec_scaled, ctau, results
        n_gamma = list_all_temp[idx][1] # gammas per incoming electron in energy window
        xsec_scaled = list_all_temp[idx][2] #cross section scaled for coupling

        
        n_exp = n_gamma * xsec_scaled * metadict['L_eff_pb'] #how many events are expected from this incoming photon energy bin
        w = n_exp/metadict['n_mg']
        # print(n_gamma, xsec_scaled, metadict['L_eff_pb'])
        # print(n_exp, w)

        list_x.append(x.clip(min=plotdict['xmin'], max=plotdict['xmax']))
        list_weights.append(np.ones(len(x))*w)
        list_color.append(cmap((list_all_temp[idx][0]-energy_range[0])/delta_energy)) #color [0..1] in selected range
    
    # for some couplings, there will be zero events (since the lifetime is too short)
    if len(list_x) == 0:
        return None, None
    
    # draw stacked histogram
    a, b, c = axs.hist(list_x, bins=bins, weights=list_weights, 
                           histtype='stepfilled', stacked=True, 
                           color=list_color, lw=0)

    all_vtx_z = np.concatenate(list_x)
    all_vtx_z_weights = np.concatenate(list_weights)
    a_full, b_full, c_full = axs.hist(all_vtx_z, bins=bins, weights=all_vtx_z_weights, 
                           histtype='step', 
                           lw=2, color='black')

    axs.set_xlabel(plotdict['xlabel'])
    axs.set_ylabel(r'Entries / {:.4f} {}'.format(binwidth, plotdict['ylabel_unit']))
    axs.set_xlim(plotdict['xmin'], plotdict['xmax'])

    #colorbar
    normalize = mcolors.Normalize(vmin=list_all_temp[0][0]*0.9, vmax=list_all_temp[-1][0]*1.1)
    scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=cmap)
    cbar = plt.colorbar(scalarmappaple)
    cbar.set_label('Incoming $E_{\gamma}$ [GeV]')

    _ = axs.text(0.975, 0.925, r'$\Lambda^{{-1}}$={} GeV$^{{-1}}$, $m_{{a}}={}$ GeV'.format(metadict['lam_inv'], metadict['mass']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)
    _ = axs.text(0.975, 0.875, r'{}, $n_{{BX}}$={:4.2e}'.format(metadict['laserconfig'], metadict['N_bx']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)
    _ = axs.text(0.975, 0.825, r'$r_{{BSM}}$={}m, $L_{{V}}$={}m, $L_{{D}}$={}m'.format(metadict['detector_radius'], metadict['distance'], metadict['target_length']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)
    _ = axs.text(0.975, 0.755, r'$E_{{\gamma}}$>{}GeV'.format(metadict['min_energy']), 
             horizontalalignment='right', 
             verticalalignment='center', 
             transform=axs.transAxes,
             size=14)

#     plt.savefig(os.path.join(plotdict['save_dir'], plotdict['plotname']), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box
    np.save(os.path.join(plotdict['save_dir'], plotdict['filename']), { 'entries': a_full, 'bins': b_full, 'xlabel': axs.get_xlabel(), 'ylabel': axs.get_ylabel(), 'xrange': [plotdict['xmin'], plotdict['xmax']]})
    
    plt.savefig(os.path.join(plotdict['save_dir'], plotdict['plotname']), bbox_inches='tight') #speichern der Funktion als pdf, bbox==bounding box

    plt.close(fig)
    return a_full, b_full
