# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

def tplot_ascii(tvar,filename=None):
    # grab data, prepend index column
    if filename is None:
        filename=tvar
    df = pytplot.data_quants[tvar].values
    sbf = pytplot.data_quants[tvar].coords['spec_bins'].values
    # save data and spec_bins
    sb_name = filename + '_v'
    np.savetxt(filename, df, fmt="%-14s", delimiter='   ')
    np.savetxt(sb_name, sbf, fmt="%-14s", delimiter='   ')
