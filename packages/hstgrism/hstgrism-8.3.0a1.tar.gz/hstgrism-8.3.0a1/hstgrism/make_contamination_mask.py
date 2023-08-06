# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import pandas as pd
import numpy as np

def make_contamination_mask(trace_c,xyref_c,bbcorner_obj,mask_obj,halfdyup,halfdylow):
    """
    This function makes a new mask image by combining the object mask with specified contamination object region.
    - trace_c = trace.csv of contamination object
    - xyref_c = xyref.csv of contamination object
    - bbcorner_obj = bbcorner.csv of the object itself
    - mask_obj = (path to object mask.fits, extension number)
    - halfdyup = number of pixels above the trace of contamination
    - halfdylow = number of pixels below the trace of contamination
    Note: contamination mask size = halfdylow + 1 + halfdyup
    Output = combined mask image
    """
    t = pd.read_csv(trace_c)
    xhc,yhc = t.xh.values.copy(),t.yh.values.copy()
    t = pd.read_csv(xyref_c)
    xyrefc = t.xyref.values.copy()
    bbcorner = pd.read_csv(bbcorner_obj)
    xcutc = xhc + xyrefc[0] - bbcorner.bb0x[0]
    ycutc = yhc + xyrefc[1] - bbcorner.bb0y[0]
    mdata = fits.open(mask_obj[0])[mask_obj[1]].data.copy()
    ny,nx = mdata.shape
    m = np.argwhere((xcutc.astype(int) <= nx-1)&(ycutc.astype(int) <= ny-1)).flatten()
    tx,ty = xcutc.astype(int)[m],ycutc.astype(int)[m]
    tm = mdata.copy()
    for i,ii in enumerate(tx):
        tm[ty[i]-halfdylow:ty[i]+halfdyup+1,tx[i]] = True
    return tm
    