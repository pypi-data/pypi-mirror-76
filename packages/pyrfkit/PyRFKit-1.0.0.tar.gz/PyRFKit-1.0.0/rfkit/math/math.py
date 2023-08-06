''' rfkit.math module. '''

from typing import Tuple, Optional, List
import numpy as np
import skrf as rf

def net_to_gmm(net: rf.Network, p: int = 2) -> rf.Network:
    ''' Convert network to gmm network. '''
    gmm_net = net.copy()
    gmm_net.se2gmm(p)
    return gmm_net

def gmm_to_se(gmm_net: rf.Network, p: int = 2, z0: float = 50):
    ''' Convert GMM network into single-ended.
        NOTE: Using rf.Network.gmm2se appears to be giving incorrect results.
    Args:
        gmm_net (rf.Network): GMM rf.Network
        p (int): # diff ports
        z0 (int): SE z0
    Returns:
        rf.Network: SE rf.Network
    '''
    gmm_s = gmm_net.s
    se_s = np.zeros_like(gmm_s)
    n = int(gmm_s.shape[1]/2)
    for i in range(n):
        for j in range(n):
            I1 = 2*i
            I2 = 2*i + 1
            I3 = 2*j
            I4 = 2*j + 1
            se_s[:, I1, I3] = (gmm_s[:, i, j] + gmm_s[:, i, j+n] + gmm_s[:, i+n, j] + gmm_s[:, i+n, j+n])/2
            se_s[:, I2, I3] = (-gmm_s[:, i, j] - gmm_s[:, i, j+n] + gmm_s[:, i+n, j] + gmm_s[:, i+n, j+n])/2
            se_s[:, I1, I4] = (-gmm_s[:, i, j] + gmm_s[:, i, j+n] - gmm_s[:, i+n, j] + gmm_s[:, i+n, j+n])/2
            se_s[:, I2, I4] = (gmm_s[:, i, j] - gmm_s[:, i, j+n] - gmm_s[:, i+n, j] + gmm_s[:, i+n, j+n])/2
    net = rf.Network(s=se_s, f=gmm_net.f, f_unit=gmm_net.frequency.unit, z0=z0)
    return net


def se_to_diff(net: rf.Network, p=2) -> rf.Network:
    ''' Convert SE network to DIFF network. '''
    diff_net = net_to_gmm(net, p=p)
    diff_net.s = diff_net.s[:, :2, :2]
    return diff_net

def net_to_diff(net: rf.Network) -> np.ndarray:
    ''' Get DIFF Mode from network. '''
    gmm_net = net_to_gmm(net)
    diff = gmm_net.s[:, :2, :2]
    return diff

def net_to_dc(net: rf.Network) -> np.ndarray:
    ''' Get DC Mode conversion. '''
    gmm_net = net_to_gmm(net)
    dc = gmm_net.s[:, :2, -2:]
    return dc

def net_to_cd(net: rf.Network) -> np.ndarray:
    ''' Get CD Mode conversion. '''
    gmm_net = net_to_gmm(net)
    # Quad 3
    cd = gmm_net.s[:, -2:, :2]
    return cd


def net_to_cm(net: rf.Network) -> np.ndarray:
    ''' Get CM Mode conversion. '''
    gmm_net = net_to_gmm(net)
    cm = gmm_net.s[:, -2:, -2:]
    return cm

def net_correction_comment(net: rf.Network) -> str:
    ''' Add touchstone comment stating ports are corrected. '''

    num_ports = net.nports
    port_list = f"Full {num_ports} Port({','.join([str(p+1) for p in range(num_ports)])})"
    # Add corrected comment to de-embedded network
    corrected_ports = [f'S{i+1}{j+1}({port_list})' for i in range(num_ports) for j in range(num_ports)]  # noqa
    corrected_comment = 'Correction: {0}'.format('\n'.join(corrected_ports))
    return corrected_comment


def net_to_tdr(net: rf.Network, ports: Optional[List[int]] = None) -> Tuple[np.array, np.ndarray]:
    ''' Convert network to TDR for all ports specified. '''
    z0 = np.abs(net.z0.item(0))
    ports = list(range(net.nports)) if ports is None else ports
    s_ports = [f's{p+1}{p+1}' for p in ports]
    # Extrapolate to DC if Fmin > 0 Hz
    dc_net = net.extrapolate_to_dc(kind='linear') if net.f[0] > 1e-3 else net.copy()
    ts = None
    tdr = None
    for p in range(net.nports):
        ts, response = getattr(dc_net, s_ports[p]).impulse_response(pad=0)
        step_model = np.cumsum(response.squeeze())
        y = z0*(1.0+step_model)/(1-step_model)
        if tdr is None:
            tdr = np.zeros((net.nports, len(y)))
        tdr[p] = y
    return ts, tdr

def compute_iloss_fit(iloss: np.array, f: rf.Frequency, fmin: float, fmax: float, method='FIT_TO_FB'):
    ''' Fit insertion loss using given IEEE method. '''
    fmin_ghz = fmin/1.0e9
    fmax_ghz = fmax/1.0e9
    freq_ghz = f/1.0e9
    min_idx = np.where(freq_ghz >= fmin_ghz)[0]
    max_idx = np.where(freq_ghz >= fmax_ghz)[0]
    min_idx = min_idx[0] if len(min_idx) > 0 else 0
    max_idx = max_idx[0] if len(max_idx) > 0 else len(freq_ghz)-1
    orig_freq = freq_ghz
    freq_ghz = freq_ghz[min_idx:max_idx+1]
    ilm = np.abs(iloss[min_idx:max_idx+1])
    il = 20*np.log10(ilm)
    F = np.stack((ilm, np.sqrt(freq_ghz)*ilm, freq_ghz*ilm, (freq_ghz**2)*ilm), axis=1)
    L = il*ilm
    alpha = np.linalg.inv(F.conj().T@F)@F.conj().T@L
    fit = alpha[0]+alpha[1]*np.sqrt(freq_ghz)+alpha[2]*freq_ghz + freq_ghz**2*alpha[3]
    iloss_fit = np.zeros_like(orig_freq)
    iloss_fit[min_idx:max_idx+1] = fit
    rmse = np.sqrt(np.mean(np.sum(np.power(iloss_fit[min_idx:max_idx+1] - il.T, 2))))
    return iloss_fit, rmse

def compute_group_delay(net: rf.Network, p1: int, p2: int) -> np.ndarray:
    ''' Compute group delay of network for ports. '''
    phase = -1.0*np.unwrap(np.angle(net.s[:, p1, p2]))
    diff_phase = np.diff(phase)
    d_phase_lo = np.concatenate((diff_phase[:1], diff_phase))
    d_phase_hi = np.concatenate((diff_phase, diff_phase[-1:]))
    diff_w = np.diff(net.f)*2*np.pi
    d_w_lo = np.concatenate((diff_w[:1], diff_w))
    d_w_hi = np.concatenate((diff_w, diff_w[-1:]))
    gd: np.array = 0.5*d_phase_lo/d_w_lo + 0.5*d_phase_hi/d_w_hi
    return gd

def compute_iphase_delay(net: rf.Network, p1: int, p2: int):
    ''' Compute improved phase delay of network for ports. '''
    tgt_angle = np.angle(net.s[:, p1, p2])
    pd = -1.0*0.5*np.unwrap(2*tgt_angle)/(2*np.pi*net.f)
    if net.f[0] > 0:
        N = 10
        gd = compute_group_delay(net, p1, p2)
        if len(gd) >= N:
            start_delay = np.mean(gd[0:N+1])
        else:
            start_delay = np.mean(gd)
        mod_unwrap = np.unwrap(2*tgt_angle)-2*np.round(start_delay*net.f[0])*2*np.pi
        pd = -1*0.5*mod_unwrap/(2*np.pi*net.f)
    return pd

def compute_phase_delay(net: rf.Network, p1: int, p2: int):
    ''' Compute phase delay of network for ports. '''
    return -1.0*np.unwrap(np.angle(net.s[:, p1, p2]))/(np.pi*net.f)

def compute_skew(net: rf.Network, src_ports: Optional[List[int]] = None, dst_ports: Optional[List[int]] = None):
    ''' Compute skew for 2N network on given port pairs. '''
    if src_ports is None:
        src_ports = [0, 1]
    if dst_ports is None:
        dst_ports = [2, 3]
    if not isinstance(src_ports, list) or len(src_ports) != 2:
        raise Exception('portsA must be a list of length 2')
    if not isinstance(dst_ports, list) or len(dst_ports) != 2:
        raise Exception('portsB must be a list of length 2')
    pd13 = compute_phase_delay(net, p1=src_ports[0], p2=dst_ports[0])
    pd24 = compute_phase_delay(net, p1=src_ports[1], p2=dst_ports[1])
    skew = pd13 - pd24
    return skew, pd13, pd24

def compute_impedance(net: rf.Network, tgt_ts: float = 1e-9, port: int = 0) -> float:
    ''' Approximate impedance in TDR at given timestamp. '''
    gnet = net_to_gmm(net) if net.nports == 4 else net
    ts, tdr = net_to_tdr(gnet, ports=[port])
    tidx = np.where(ts >= tgt_ts)[0]
    tidx = tidx[0] if len(tidx) > 0 else 0
    return tdr[0][tidx]

def has_discontinuity(net: rf.Network, il_lim: float = -3, tdr_lim: float = 3) -> bool:
    ''' Detect discontinuity by checking IL and TDR. '''
    gmm_net = net_to_gmm(net) if net.nports == 4 else net
    _, tdr = net_to_tdr(net)
    iloss = gmm_net.s_db[:, 0, 1]
    z0 = np.abs(net.z0.item(0))
    # IL < L dB @ start freq -AND- SE TDR has abs(tdr(t)) > K*z0 for any t
    is_open = iloss[0] < il_lim and np.any(np.abs(tdr) > tdr_lim*z0)
    return is_open

def apply_pwl_mask(xdata: np.array, ydata: np.array, mask, direction: str = 'ABOVE'):
    ''' Apply PWL mask to given data set. '''

    dir_sign = -1 if direction == 'BELOW' else 1
    ydata = ydata.squeeze()
    # If multiple y sets, we want first dim to equal dim of x
    if ydata.ndim == 2 and ydata.shape[1] == xdata.shape[0]:
        ydata = ydata.transpose()
    for i in range(1, len(mask)):
        xmin = np.argmin(np.abs(xdata - mask[i-1, 0]))
        xmax = np.argmin(np.abs(xdata - mask[i, 0]))
        mask_line = np.interp(xdata[xmin:xmax+1], mask[i-1:i+1, 0].squeeze(), mask[i-1:i+1, 1].squeeze())
        # To broadcast add/sub, last dimensions must be equal so tranpose y then transpose back result
        mask_delta = dir_sign*(mask_line - ydata[xmin:xmax+1].transpose()).transpose()
        crossings = np.where((mask_delta) < 0)[0]
        min_delta = np.min(mask_delta)
        max_value = np.max(ydata[xmin:xmax+1]) if direction == 'ABOVE' else np.min(ydata[xmin:xmax+1])
        yield mask[i-1, 0], mask[i, 0], mask[i-1, 1], mask[i, 1], crossings, min_delta, max_value
