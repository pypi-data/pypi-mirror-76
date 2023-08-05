import os
from osgeo import gdal
import numpy as np


def save_index(in_array, out, snap, dType=gdal.GDT_Float32):
    """
    save_raster(in_array, out, snap, dType=gdal.GDT_Float32)

    Saves the input NumPy array as a one band raster.

    Parameters:

            in_array :: array, required
                * NumPy array to be saved as TIFF raster file.

            out :: str, required
                * Output path and file name for TIFF raster file.

            snap :: gdal raster, required
                * Raster file with which projections and geotransformations
                  are based off.

            dType :: gdal datatype, required (default=gdal.GDT_Float32)_
                * Datatype to save raster as.
    """
    if os.path.exists(out):
        os.remove(out)

    snap = gdal.Open(snap)

    driver = gdal.GetDriverByName('GTiff')
    metadata = driver.GetMetadata()
    shape = in_array.shape
    dst_ds = driver.Create(out,
                           xsize=shape[1],
                           ysize=shape[0],
                           bands=1,
                           eType=dType)
    proj = snap.GetProjection()
    geo = snap.GetGeoTransform()
    dst_ds.SetGeoTransform(geo)
    dst_ds.SetProjection(proj)
    dst_ds.GetRasterBand(1).WriteArray(in_array)
    dst_ds.FlushCache()
    dst_ds = None

    return in_array
