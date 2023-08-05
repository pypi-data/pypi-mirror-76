# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 12:20:29 2019

Load MATLAB 7.3 files into Python

@author: Simon
"""
import os
import numpy as np
import h5py



class HDF5Decoder():
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.d = {}
        self.refs = {} # this is used in case of matlab matrices

    def mat2dict(self, hdf5):
        if '#refs#' in hdf5: 
            self.refs = hdf5['#refs#']
        d = {}
        for var in hdf5:
            if var in ['#refs#','#subsystem#']:
                continue
            ext = os.path.splitext(hdf5.filename)[1].lower()
            if ext=='.mat':
                d[var] = self.unpack_mat(hdf5[var])
            elif ext=='.h5' or ext=='.hdf5':
                err = 'Can only load .mat. Please use package hdfdict instead'\
                      '\npip install hdfdict\n' \
                      'https://github.com/SiggiGue/hdfdict'
                raise NotImplementedError(err)
            else:
                raise ValueError('can only unpack .mat')
        return d
    
   
    def unpack_mat(self, hdf5, depth=0):
        """
        unpack a h5py entry: if it's a group expand,
        if it's a dataset convert
        
        for safety reasons, the depth cannot be larger than 99
        """
        if depth==99:raise Exception
        if isinstance(hdf5, (h5py._hl.group.Group)):
            d = dict()
            for key in hdf5:
                elem   = hdf5[key]
                self.d[key] = hdf5
                d[key] = self.unpack_mat(elem, depth=depth+1)
            return d
        elif isinstance(hdf5, h5py._hl.dataset.Dataset):
            return self.convert_mat(hdf5)


    def _has_refs(self, dataset):
        if len(dataset)==0: return False
        if not isinstance(dataset[0], np.ndarray): return False
        if isinstance(dataset[0][0], h5py.h5r.Reference):  
            return True
        return False


    def convert_mat(self, dataset):
        """
        Converts h5py.dataset into python native datatypes
        according to the matlab class annotation
        """      
        # all MATLAB variables have the attribute MATLAB_class
        # if this is not present, it is not convertible
        if not 'MATLAB_class' in dataset.attrs and not self._has_refs(dataset):
            if self.verbose:
                print(str(dataset), 'is not a matlab type')
            return None
        if self._has_refs(dataset):
            mtype='cell'
        else:
            mtype = dataset.attrs['MATLAB_class'].decode()
       
        if mtype=='cell':
            cell = []
            for ref in dataset:
                row = []
                for r in ref:
                    entry = self.unpack_mat(self.refs.get(r))
                    row.append(entry)
                cell.append(row)
            cell = list(map(list, zip(*cell))) # transpose cell
            if len(cell)==1:cell = cell[0]
            return cell
        elif mtype=='char': 
            string_array = np.array(dataset).ravel()
            string_array = ''.join([chr(x) for x in string_array])
            string_array = string_array.replace('\x00', '')
            return string_array
        elif mtype=='bool':
            return bool(dataset)
        elif mtype=='logical': 
            arr = np.array(dataset, dtype=bool).T.squeeze()
            if arr.size==1: arr=bool(arr)
            return arr
        elif mtype=='canonical empty': 
            return None
        # complex numbers need to be filtered out separately
        elif 'imag' in str(dataset.dtype):
            if dataset.attrs['MATLAB_class']==b'single':
                dtype = np.complex64 
            else:
                dtype = np.complex128
            arr = np.array(dataset)
            arr = (arr['real'] + arr['imag']*1j).astype(dtype)
            return arr.T.squeeze()
        # if it is none of the above, we can convert to numpy array
        elif mtype in ('double', 'single', 'int8', 'int16', 'int32', 'int64', 
                       'uint8', 'uint16', 'uint32', 'uint64'): 
            arr = np.array(dataset, dtype=dataset.dtype)
            return arr.T.squeeze()
        else:
            if self.verbose: 
                print('data type not supported: {}, {}'.format(mtype, dataset.dtype))
            return None
        
            
def loadmat(filename, verbose=True):
    """
    Loads a MATLAB 7.3 .mat file, which is actually a
    HDF5 file with some custom matlab annotations inside
    
    :param filename: A string pointing to the file
    :returns: A dictionary with the matlab variables loaded
    """
    assert os.path.isfile(filename), '{} does not exist'.format(filename)
    decoder = HDF5Decoder(verbose=verbose)
    try:
        with h5py.File(filename, 'r') as hdf5:
            dictionary = decoder.mat2dict(hdf5)
        return dictionary
    except OSError:
        raise TypeError('{} is not a MATLAB 7.3 file. '\
                        'Load with scipy.io.loadmat() instead.'.format(filename))
            
            
def savemat(filename, verbose=True):
    raise NotImplementedError

    
        
