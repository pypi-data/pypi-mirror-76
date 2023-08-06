from typing import List
from typing import Union
import collections
import numpy as np
import skrf as rf
import matplotlib as mpl
import matplotlib.pyplot as plt
import afrp
from mathRf import net2gmm, compute_iphase_delay, net2tdr, se2diff
from getPortMapping import getPortMapping

def make_axes(nets):
    x = np.ceil(np.sqrt(len(nets)))
    x = int(x)
    y = x
    fig, ax = plt.subplots(nrows = x, ncols = y)
    newAx  = []
    if isinstance(ax,collections.abc.Iterable):
        for lst in ax:
            lstIsIterable = True
            while lstIsIterable:
                if isinstance(lst,collections.abc.Iterable):
                    lst = lst[0]
                else:
                    lstIsIterable = False
                    newAx.append(lst)
    else:
        newAx = ax
                
    return fig, newAx
def getPairs(pm: list):
    pairs = [-1] * int((len(pm)/2))
    banned = []
    j = 0
    for i in range(len(pm)):
        if not((i in banned) or (pm[i] in banned)):
            pairs[j] = [i,pm[i]]
            banned.append(i)
            banned.append(pm[i])
            j = j + 1
    return pairs
def plot_freq_masks(ax: plt.Axes, lmask=None, umask=None, ymin=None, ymax=None, freq_scale=1.0e9, y_scale=1):
    ymin = ymin if ymin is not None else ax.get_ylim()[0]
    ymax = ymax if ymax is not None else ax.get_ylim()[1]
    if lmask is not None:
        ax.plot(lmask[:, 0]/freq_scale, lmask[:, 1]/y_scale, color='black', linestyle='--', linewidth=0.5)
        ax.fill_between(lmask[:, 0]/freq_scale, ymin, lmask[:, 1]/y_scale, facecolor='gray', alpha=0.2, zorder=0.1)
    if umask is not None:
        ax.plot(umask[:, 0]/freq_scale, umask[:, 1]/y_scale, color='black', linestyle='--', linewidth=0.5)
        ax.fill_between(umask[:, 0]/freq_scale, umask[:, 1]/y_scale, ymax, facecolor='gray', alpha=0.2, zorder=0.1)


def plot_iloss(networks: Union[List[rf.Network],rf.Network], ax: Union[List[plt.Axes], plt.Axes] = None,
               labels: List = None, lmask: List = None, umask: List = None, fitted: List = None, title: str = None,
               savepath: str = None,side: int = 0):
    
    if(isinstance(networks,list)):
        if(ax is None):
            fig, ax = make_axes(networks)
    else:
        networks = [networks]
        if(ax is None):
            fig, ax = make_axes(networks)
    #if not( isinstance(ax, list) or  isinstance(ax,tuple) or isinstance(ax,np.ndarray)):
    if not isinstance(ax, collections.abc.Iterable):
        ax = [ax]
    

    if len(networks) != len(ax):
        raise ValueError("length of networks list and length of axes list must be equal. length of networks: "+ len(networks)+", length of axes: "+ len(ax))
    for i, net in enumerate(networks):
        portMap = getPortMapping(net)
        pairs = getPairs(portMap)
        for j in range(len(pairs)):
            #if you need to add differetial or plot different sides then add those conditions here
            if side == 0:
                ax[i].plot(afrp.db.dB(net.s[:,pairs[j][0],pairs[j][1]]))
            else:
                ax[i].plot(afrp.db.dB(net.s[:,pairs[j][1],pairs[j][0]]))
            ax[i].grid(True)
            ax[i].set_xlabel('Frequency (GHz)')
            ax[i].set_ylabel('Magnitude (dB)')
            #ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    plt.show()
    

    '''           
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 4))
    ymin = -5
    ymax = 2
    xmin = 0
    xmax = 0
    freq_scale = 1.0e9
    freq = None
    lbl_prefix = 'sdd'
    for i, net in enumerate(networks):
        tgt_net = net2gmm(net) if net.nports == 4 else net
        freq = tgt_net.f
        net_name = labels[i] if labels else net.name
        lbl_prefix = 'sdd' if tgt_net.nports == 4 else 's'
        s12 = tgt_net.s_db[:, 0, 1].squeeze()
        s21 = tgt_net.s_db[:, 1, 0].squeeze()
        ax.plot(tgt_net.f/freq_scale, s12, label=f'{net_name} {lbl_prefix}12')
        ax.plot(tgt_net.f/freq_scale, s21, label=f'{net_name} {lbl_prefix}21')
        ymin = min(ymin, s12.min(), s21.min())
        ymax = max(ymax, s12.max(), s12.max())
        xmax = tgt_net.f[-1]/freq_scale
    # Plot masks
    plot_freq_masks(ax, lmask, umask, ymin=-35, ymax=15, freq_scale=freq_scale)
    if fitted is not None:
        real_idx = np.where(np.abs(fitted) > 1e-12)[0]
        min_idx = real_idx[0] if len(real_idx) else 0
        max_idx = real_idx[-1] if len(real_idx) else len(fitted)
        fit_freq = freq[min_idx:max_idx]/freq_scale
        fit_vals = fitted[min_idx:max_idx]
        ax.plot(fit_freq, fit_vals, label=f'FIT {lbl_prefix}21', linestyle='--')
    ymin = np.clip(np.floor(ymin), -30, -5)
    ymax = np.clip(np.ceil(ymax), 2, 5)
    ax.set_title(title if title else 'Insertion Loss')
    ax.grid(True)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax+1)
    ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Magnitude (dB)')
    if labels:
        ax.legend(fontsize='10')
    plt.tight_layout()
    if savepath:
        fig.savefig(savepath, format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()
    '''
'''
def plot_iloss_data(
        f: np.array, data: List[np.array],
        labels: List = None, lmask: List = None, umask: List = None, fitted: List = None, title: str = None, savepath: str = None):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 4))
    ymin = -5
    ymax = 2
    xmin = 0
    xmax = 0
    freq_scale = 1.0e9
    freq = None
    lbl_prefix = 'sdd'
    for i, y in enumerate(data):
        net_name = labels[i] if labels else ''
        ax.plot(f/freq_scale, y, label=f'{net_name}')
        ymin = min(ymin, y.min())
        ymax = max(ymax, y.max())
        xmax = f[-1]/freq_scale
    # Plot masks
    plot_freq_masks(ax, lmask, umask, ymin=-35, ymax=15, freq_scale=freq_scale)
    if fitted is not None:
        real_idx = np.where(np.abs(fitted) > 1e-12)[0]
        min_idx = real_idx[0] if len(real_idx) else 0
        max_idx = real_idx[-1] if len(real_idx) else len(fitted)
        fit_freq = freq[min_idx:max_idx]/freq_scale
        fit_vals = fitted[min_idx:max_idx]
        ax.plot(fit_freq, fit_vals, label=f'FIT {lbl_prefix}21', linestyle='--')
    ymin = np.clip(np.floor(ymin), -30, -5)
    ymax = np.clip(np.ceil(ymax), 2, 5)
    ax.set_title(title if title else 'Insertion Loss')
    ax.grid(True)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax+1)
    ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Magnitude (dB)')
    if labels:
        ax.legend(fontsize='10')
    plt.tight_layout()
    if savepath:
        fig.savefig(savepath, format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()
'''
'''
def plot_cd(
        networks: List[rf.Network],
        labels: List = None, lmask: List = None, umask: List = None, title: str = None, savepath: str = None):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 4))
    ymin = -5
    ymax = 2
    xmin = 0
    xmax = 0
    freq_scale = 1.0e9
    lbl_prefix = 'scd'
    for i, net in enumerate(networks):
        tgt_net = net2gmm(net)
        net_name = labels[i] if labels else net.name
        scd12 = tgt_net.s_db[:, 2, 1].squeeze()
        scd21 = tgt_net.s_db[:, 3, 0].squeeze()
        ax.plot(tgt_net.f/freq_scale, scd12, label=f'{net_name} {lbl_prefix}12')
        ax.plot(tgt_net.f/freq_scale, scd21, label=f'{net_name} {lbl_prefix}21')
        ymin = min(ymin, scd12.min(), scd21.min())
        ymax = max(ymax, scd12.max(), scd21.max())
        xmax = tgt_net.f[-1]/freq_scale
    # Plot masks
    plot_freq_masks(ax, lmask, umask, ymin=-55, ymax=15, freq_scale=freq_scale)
    ymin = np.clip(np.floor(ymin), -50, -10)
    ymax = np.clip(np.ceil(ymax), 2, 5)
    ax.set_title(title if title else 'CD Mode Conversion')
    ax.grid(True)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax+1)
    ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Magnitude (dB)')
    if labels:
        ax.legend(fontsize='10')
    plt.tight_layout()
    if savepath:
        fig.savefig(savepath, format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()

'''
def plot_rloss(networks: Union[List[rf.Network],rf.Network], ax: Union[List[plt.Axes], plt.Axes] = None,
 labels: List = None, lmask: List = None, umask: List = None, title: str = None,
               savepath: str = None,side: int = 0):

    if(isinstance(networks,list)):
        if(ax is None):
            fig, ax = make_axes(networks)
    else:
        networks = [networks]
        if(ax is None):
            fig, ax = make_axes(networks)
    #if not( isinstance(ax, list) or  isinstance(ax,tuple) or isinstance(ax,np.ndarray)):
    if not isinstance(ax, collections.abc.Iterable):
        ax = [ax]


    if len(networks) != len(ax):
        raise ValueError("length of networks list and length of axes list must be equal. length of networks: "+ len(networks)+", length of axes: "+ len(ax))
    for i, net in enumerate(networks):
        portMap = getPortMapping(net)
        pairs = getPairs(portMap)
        for j in range(len(pairs)):
            #if you need to add differetial or plot different sides then add those conditions here
            if side == 0:
                ax[i].plot(afrp.db.dB(net.s[:,pairs[j][0],pairs[j][0]]))
            else:
                ax[i].plot(afrp.db.dB(net.s[:,pairs[j][1],pairs[j][1]]))

            ax[i].grid(True)
            ax[i].set_xlabel('Frequency (GHz)')
            ax[i].set_ylabel('Magnitude (dB)')
            #ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    plt.show()
    '''           
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 4))
    ymin = -15
    ymax = 2
    xmin = 0
    xmax = 0
    freq_scale = 1.0e9
    for i, net in enumerate(networks):
        tgt_net = net2gmm(net) if net.nports == 4 else net
        net_name = labels[i] if labels else net.name
        lbl_prefix = 'sdd' if tgt_net.nports == 4 else 's'
        s11 = tgt_net.s_db[:, 0, 0].squeeze()
        ax.plot(tgt_net.f/freq_scale, s11, label=f'{net_name} {lbl_prefix}11')
        # s22 = tgt_net.s_db[:, 0, 0].squeeze()
        # ax.plot(tgt_net.f/freq_scale, s22, label=f'{net_name} {lbl_prefix}22')
        ymin = min(ymin, s11.min())
        ymax = max(ymax, s11.max())
        xmax = tgt_net.f[-1]/freq_scale
    # Plot masks
    plot_freq_masks(ax, lmask, umask, ymin=-35, ymax=15, freq_scale=freq_scale)
    ymin = np.clip(np.floor(ymin), -30, -15)
    ymax = np.clip(np.ceil(ymax), 2, 5)
    ax.set_title(title if title else 'Return Loss')
    ax.grid(True)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax+1)
    ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Magnitude (dB)')
    if labels:
        ax.legend(fontsize='10')
    plt.tight_layout()
    if savepath:
        fig.savefig(savepath, format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()
    '''
'''
def plot_skew(networks: rf.Network, labels: List = None, lmask: List = None, umask: List = None, title: str = None,
              savepath: str = None, xmin=None):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 4))
    ymin = -30
    ymax = 30
    freq_scale = 1.0e9
    y_scale = 1e-12
    for i, net in enumerate(networks):
        net_name = labels[i] if labels else net.name
        pd13 = compute_iphase_delay(net, p1=2, p2=0)
        pd24 = compute_iphase_delay(net, p1=3, p2=1)
        skew = pd13 - pd24
        skew_ps = skew/y_scale
        ax.plot(net.f/freq_scale, skew_ps, label=f'{net_name}')
        ymin = min(ymin, skew_ps.min())
        ymax = max(ymax, skew_ps.max())
    # Plot masks
    plot_freq_masks(ax, lmask, umask, ymin=-30, ymax=30, freq_scale=freq_scale, y_scale=y_scale)
    ax.set_title(title if title else 'Skew')
    ax.grid(True)
    ymin = np.clip(np.floor(ymin), -30, -10)
    ymax = np.clip(np.ceil(ymax), 10, 30)
    ax.set_ylim(ymin, ymax+1)
    ax.set_yticks(np.linspace(ymin, ymax+1, 6))
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Skew (pS)', color='black')
    # ax.set_xscale('log', nonposx='clip')
    if xmin is not None:
        ax.set_xlim(xmin=xmin/freq_scale)
    if labels:
        ax.legend(fontsize='10')
    ax.xaxis.set_major_locator(plt.MaxNLocator(min_n_ticks=5, nbins=5))
    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, orientation='landscape', format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()
'''

def plot_tdr(networks: Union[List[rf.Network],rf.Network], ax: Union[List[plt.Axes], plt.Axes] = None, labels: List = None, title: str = None, savepath: str = None):
    
    if(isinstance(networks,list)):
        if(ax is None):
            fig, ax = make_axes(networks)
    else:
        networks = [networks]
        if(ax is None):
            fig, ax = make_axes(networks)
    #if not( isinstance(ax, list) or  isinstance(ax,tuple) or isinstance(ax,np.ndarray)):
    if not isinstance(ax, collections.abc.Iterable):
        ax = [ax]

    if len(networks) != len(ax):
        raise ValueError("length of networks list and length of axes list must be equal. length of networks: "+ len(networks)+", length of axes: "+ len(ax))
    for i, net in enumerate(networks):
        portMap = getPortMapping(net)
        pairs = getPairs(portMap)
        ts, tdr = net2tdr(net)
        for pair in pairs:
            ax[i].plot(tdr[pair[0]])
        #axes[i].set_yticks(np.linspace(ymin, ymax+1, 6))
        ax[i].grid(True)
        ax[i].set_xlabel('Time (ns)')
    plt.show()
    '''
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    z0 = 50
    freq_scale = 1.0e9
    xmin = -5
    xmax = 20
    ymin = z0-5
    ymax = z0+25
    for i, net in enumerate(networks):
        net_name = labels[i] if labels else net.name
        ts, tdr = net2tdr(net)
        for p in range(net.nports):
            axes_idx = round((p+1)/net.nports)
            axes[axes_idx].plot(freq_scale*ts.squeeze(), tdr[p], label=f'{net_name} S{p+1}{p+1}')
    ymin = z0-5
    ymax = z0+25
    for i in range(2):
        axes[i].set_xlim(xmin, xmax)
        axes[i].set_ylim(ymin, ymax)
        axes[i].set_yticks(np.linspace(ymin, ymax+1, 6))
        axes[i].grid(True)
        axes[i].set_xlabel('Time (ns)')
        if i == 0:
            axes[i].set_ylabel('Impedance (Ohms)')
        else:
            axes[i].set_yticklabels([])
        if labels:
            axes[i].legend(fontsize='10')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.suptitle(title if title else 'TDR - SE', fontsize=15, y=1.05)
    plt.tight_layout(h_pad=0, w_pad=0)
    if savepath:
        fig.savefig(savepath, orientation='landscape', format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()
    '''
'''
def plot_diff_tdr(networks: List[rf.Network], labels: List = None, title: str = None, savepath: str = None):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 4))
    z0 = 100
    xmin = -5
    xmax = 20
    ymin = z0
    ymax = z0
    for i, net in enumerate(networks):
        tgt_net = se2diff(net, p=2)
        ts, tdr = net2tdr(tgt_net)
        net_name = labels[i] if labels else tgt_net.name
        for p in range(tgt_net.nports):
            ymin = min(ymin, tdr[p].min())
            ymax = max(ymax, tdr[p].max())
            ax.plot(1e9*ts.squeeze(), tdr[p], label=f'{net_name} S{p+1}{p+1}')
    ax.set_title(title if title else 'TDR - Diff')
    ax.grid(True)
    ymin = np.clip(np.floor(ymin) - 5, .5*z0, 2*z0)
    ymax = np.clip(np.ceil(ymax) + 5, z0+15, 2*z0)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks(np.linspace(ymin, ymax, 6))
    ax.set_xlabel('Time (ns)')
    ax.set_ylabel('Impedance (Ohms)')
    if labels:
        ax.legend(fontsize='10')
    plt.tight_layout()
    if savepath:
        fig.savefig(savepath, format='png', transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        fig.show()
'''

#tests for plotting
net = rf.Network(r"C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF.s32p")
#plot_tdr(net)
#fig, ax = plt.subplots(nrows = 1, ncols = 1)
plot_tdr(net)