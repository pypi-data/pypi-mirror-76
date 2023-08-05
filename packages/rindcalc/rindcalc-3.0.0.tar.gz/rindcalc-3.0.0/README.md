 <img align="left" src="./docs/source/rindcalc_logo.png" width="140" height="149.4"/> 

# Rindcalc

**A Spectral Index Raster Calculator For Satellite Image Processing**

[![Documentation Status](https://readthedocs.org/projects/rindcalc/badge/?version=2.0.5)](https://rindcalc.readthedocs.io/en/2.0.5/?badge=2.0.5)
[![Build Status](https://travis-ci.org/ocsmit/rindcalc.svg?branch=master)](https://travis-ci.org/ocsmit/rindcalc)
[![Conda Platforms](https://anaconda.org/rindcalc/rindcalc/badges/platforms.svg)](https://anaconda.org/rindcalc/rindcalc)
[![DOI](https://zenodo.org/badge/232691170.svg)](https://zenodo.org/badge/latestdoi/232691170)
---

#### For more information visit the [Rindcalc documentation](https://rindcalc.readthedocs.io/en/latest/)

Rindcalc is an open source python library built on numpy and gdal aiming to
provide seamless and accurate raster index calculations and composites of 
satellite and aerial imagery.    

It currently consists of index calculation, composite and utility functions
for Landsat-8 and USDA NAIP imagery, with Sentinel-2 and MODIS satellite
functionality in the works

**Roadmap**

- [ ] Finish Sentinel-2 implementation
- [x] Rework Landsat, NAIP, and Sentinel to operate in classes
- [ ] Segmentation and zonal statistics

**Install with pip**

Dependencies:
 * GDAL - *need to build from .whl file* 
 * NumPy

```console
pip install rindcalc
```    

**Install with conda**

```console
conda install -c rindcalc rindcalc 
```
If rindcalc is not importing after conda install on Windows 10 then rindcalc 
files need to be moved from Lib/pythonX.X/site-packages/ to Lib/site-packages
within the conda env folder. 
