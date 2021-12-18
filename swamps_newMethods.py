# =======================================
#   SWAMP: CURRENT CONDITIONS
# =======================================
# author:     Vincent Falardeau
# date:       December 13, 2021
# purpose:    To isolate and map the kinds of landcover we are interested in on swamp soils,
#             reclassifying landcover to focus on natural swamps with and without trees,
#             agricultural land, waters, and developed land (including buffers around
#             buildings and roads).

# =======================================
#   SET UP THE SCRIPT
# =======================================

# import tools from WBT module
from WBT.whitebox_tools import WhiteboxTools

# import math module
import math

# declare a name for the tools
wbt = WhiteboxTools()

# set working directory, a folder with the inputs
wbt.work_dir = "/Users/vincentfalardeau/projects/GEOG0310/wbt_pySpace-master/SwampExportMidd"

# =========================
#   INPUTS
# =========================

# export the data from Google Earth Engine here: https://code.earthengine.google.com/817a1d84209bc94c67b73347357faae6

lc = 'lc.tif' # landcover raster with 8 classes

swampsoil = 'swampsoil.tif' # binary of soil series associated with swamps

bufferedbuildings = 'imageBB_inv.tif' # buildings buffered by 100 feet, inverted (zeros within building buffers)

rdsFragmenting = 'rdsFragmenting.tif' # rasterized fragmenting roads (federal/state highways and Class 3 roads)

ag = 'agImage.tif' # binary raster of agricultural lands

# ==========================
#   LAND COVER
# ==========================

# Invert agriculture raster.
wbt.not_equal_to(ag,1,'agZero.tif')
# Multiply landcover by inverted agriculture to get zeroes where there is agriculture.
wbt.multiply(lc,'agZero.tif','lcAgZero.tif')
# Reclass the altered land cover raster, focus on trees, grass/shrub/RR, ag, water, and all other/developed.
# 1) Trees, 2) Grass/Shrub/RR, 3) Ag, 4) Water, 5) All Other/Developed.
reclassvals = '3;0;1;1;2;2;5;3;4;4;5;5;5;6;5;7;2;8'
wbt.reclass('lcAgZero.tif','lcReclass.tif',reclassvals, assign_mode=True)

# ========================================
#   BUFFERED BUILDINGS AND ROADS to 5
# ========================================

# 100-meter buffered buildings
wbt.multiply('lcReclass.tif',bufferedbuildings,'lc_bb_Zero.tif') # burn zeros into the landcover raster within building buffers
reclass_developed = '5;0;1;1;2;2;3;3;4;4;5;5' # define reclassification values for converting zeros to fives while leaving the rest unchanged
wbt.reclass('lc_bb_Zero.tif','lc_bbuffer.tif',reclass_developed,assign_mode=True) # reclass burnt-in zeros to fives for developed/other


# 3-meter buffered roads
wbt.buffer_raster(rdsFragmenting,'roadbuffer.tif',3,gridcells=False) # buffer fragmenting roads by 3 meters
wbt.not_equal_to('roadbuffer.tif',1,'invert_roads.tif') # invert fragmenting roads raster (zeros for fragmenting roads)
wbt.multiply('lc_bbuffer.tif','invert_roads.tif','lc_rdZero.tif') # multiply to burn zeros into the landcover raster
wbt.reclass('lc_rdZero.tif','lc_withbuffers.tif',reclass_developed,assign_mode=True) # reclass burnt-in zeros to fives for developed/other

# ==============================
#   NARROW BY SWAMP SOILS
# ==============================

wbt.multiply('lc_withbuffers.tif',swampsoil,'lc_swampsoil.tif') # multiply by swamp soil binary to get zeros in non-swamp-soil areas
