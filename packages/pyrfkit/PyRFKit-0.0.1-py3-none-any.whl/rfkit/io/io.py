''' rfkit.io module. '''

from typing import Optional, Dict, List
import numpy as np
import pandas as pd
import h5py
import skrf as rf

def net_from_dataframe(df: pd.DataFrame, units: str = 'Hz', column: Optional[str] = 'channel',
                       name: Optional[str] = None) -> rf.Network:
    ''' Read Network from DataFrame
    Args:
        df (pd.DataFrame): DataFrame to read from
        units (str): Frequency units ('Hz', 'GHz') since df cant contain attributes
        column (str, optional): Reduce rows by *column* matching *name*
        name (str, optional): Reduce rows by *column* matching *name*
    Returns:
        rf.Network
    '''
    m_ports: int = 0
    n_ports: int = 0
    net_df = df[df[column] == name] if name and column else df
    for s in filter(lambda c: 's_re' in c, net_df.columns):
        p_str = s.split(' ')[-1]
        m_ports = max(int(p_str[:len(p_str)//2]), m_ports)
        n_ports = max(int(p_str[len(p_str)//2:]), n_ports)
    f = net_df.index.to_numpy()
    snp = np.empty((len(f), m_ports, n_ports), dtype=np.complex128)
    for i in range(m_ports):
        for j in range(n_ports):
            snp[:, i, j].real = net_df[f's_re {i+1}{j+1}'].to_numpy()
            snp[:, i, j].imag = net_df[f's_im {i+1}{j+1}'].to_numpy()
    return rf.Network(f=f, s=snp, name=name, f_unit=units)

def nets_from_dataframe(df: pd.DataFrame, units: str = 'Hz', column: str = 'channel') -> Dict[str, rf.Network]:
    ''' Read Networks from DataFrame
    Args:
        df (pd.DataFrame): DataFrame to read from
        units (str): Frequency units ('Hz', 'GHz') since df cant contain attributes
        column (str): Networks split by unique entries in column (e.g. Channel: CH1 CH2)
    Returns:
        Dict[str, rf.Network]: Returns all networks as dict w/ key being column entry
    '''
    net_names = list(set(df[column]))
    nets = dict()
    for net_name in net_names:
        net = net_from_dataframe(df, units=units, column=column, name=net_name)
        nets[net_name] = net
    return nets

def net_to_dataframe(net: rf.Network) -> pd.DataFrame:
    ''' Convert network to DataFrame
    Args:
        net (rf.Network): Network to convert
    Returns:
        pd.DataFrame
    '''
    df = net.to_dataframe(attrs=['s_re', 's_im'])
    return df

def nets_to_dataframe(nets: List[rf.Network], net_names: Optional[List[str]] = None, column: str = 'channel'):
    ''' Convert networks to single DataFrame
    Args:
        nets (List[rf.Network]): Networks to convert
        net_names (List[str]): Optional names for given network to store in column
        column (str): Column name to save network name under
    Returns:
        pd.DataFrame
    '''

    df: pd.DataFrame = pd.DataFrame()
    for i, net in enumerate(nets):
        net_name = net_names[i] if net_names else net.name if net.name else i
        net_df = net_to_dataframe(net)
        net_df.insert(0, column, len(net_df)*[net_name], True)
        df = df.append(net_df)
    return df

def net_from_parquet(path: str, *args, **kwargs) -> rf.Network:
    ''' Read network from parquet file.
    Args:
        path (str): Parquet file path
        *args, **kwargs: See rfkit.io.net_from_dataframe arguments
    Returns:
        rf.Network
    '''
    df = pd.read_parquet(path)
    net = net_from_dataframe(df, *args, **kwargs)
    return net


def nets_from_parquet(path: str, *args, **kwargs) -> Dict[str, rf.Network]:
    ''' Read networks from parquet file.
    Args:
        path (str): Parquet file path
        *args, **kwargs: See rfkit.io.nets_from_dataframe arguments
    Returns:
        rf.Network
    '''
    df = pd.read_parquet(path)
    nets = nets_from_dataframe(df, *args, **kwargs)
    return nets

def nets_to_parquet(nets: List[rf.Network], path: str, *args, **kwargs):
    ''' Writes networks to parquet file.
    Args:
        nets (List[rf.Network]): Networks to save
        path (str): Parquet file path
        *args, **kwargs: See rfkit.io.nets_to_dataframe arguments
    '''
    df = nets_to_dataframe(nets, *args, **kwargs)
    df.to_parquet(path)

def nets_from_hdf5(path: str, prefix: str = '/', units: Optional[str] = 'Hz') -> Dict[str, rf.Network]:
    ''' Read Networks from HDF5 file
    Args:
        path (pd.DataFrame): HDF5 file path
        prefix (str): HDF5 prefix to look for networks
        units (str, optional): Frequency units if not stored in HDF5
    Returns:
        Dict[str, rf.Network]: Returns all networks as dict
    '''
    nets = dict()
    with h5py.File(path, 'r') as h5:
        for net_name in h5[prefix].keys():
            net_prefix = f'{prefix}/{net_name}'
            net = rf.Network(
                name=net_name, f_unit=h5[f'{net_prefix}/f'].attrs.get('units', units),
                f=h5[f'{net_prefix}/f'][()],
                s=h5[f'{net_prefix}/s'][()]
            )
            nets[net_name] = net
    return nets

def nets_to_hdf5(nets: List[rf.Network], path: str, prefix: str = '/', net_names: Optional[List[str]] = None,
                 attrs: Optional[Dict[str, any]] = None):
    ''' Save Networks to HDF5 file
    Args:
        nets (List[rf.Network]): Networks to save
        path (pd.DataFrame): HDF5 file path
        prefix (str): HDF5 prefix to store networks under
        net_names (List[str], optional): names to save network under otherwise use Network.name
    '''
    with h5py.File(path, 'w') as h5:
        if attrs:
            for attr, val in attrs.items():
                h5.attrs[attr] = val
        for i, net in enumerate(nets):
            net_name = net_names[i] if net_names else net.name if net.name else i
            net_prefix = f'{prefix}/{net_name}'
            net_group = h5.create_group(net_prefix)
            f_dset = net_group.create_dataset('f', data=net.f, compression='gzip')
            f_dset.attrs['units'] = net.frequency.unit
            s_dset = net_group.create_dataset('s', data=net.s, compression='gzip')
            s_dset.attrs['units'] = 'RI'
