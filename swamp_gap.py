# =======================================
#   SWAMP: EVALUATION & GAP ANALYSIS
# =======================================
# author:     Vincent Falardeau
# date:       December 13, 2021
# purpose:    To identify how much of Middlebury's swamp is protected,
#             considering which land cover types are protected and
#             whether they are protected under agriculture or natural conditions.
#             Then to evaluate how much of the swamp would be protected under an alternative system,
#             where habitat blocks and riparian corridors are prioritized for conservation.

# =======================================
#   SET UP THE SCRIPT
# =======================================

# import tools from WBT module
from WBT.whitebox_tools import WhiteboxTools

# import math module
import math
 
# declare a name for the tools
wbt = WhiteboxTools()

wbt.work_dir = "/Users/vincentfalardeau/projects/GEOG0310/wbt_pySpace-master/swampmethods2"

# =========================
#   INPUTS
# =========================

# export the data from Google Earth Engine here: https://code.earthengine.google.com/817a1d84209bc94c67b73347357faae6

swamp_landcover = 'lc_swampsoil.tif'
protected = 'proFlat.tif'
hb = 'hb.tif'
riparian = 'imageRip.tif'
significant = 'sncImage.tif'

# ================================
#   EVALUATE PROTECTED STATUS
# ================================

# Add 100 times the protected status (100 protected under ag, 200 protected natural)
wbt.multiply(protected,100,'protected.tif')
wbt.add(swamp_landcover,'protected.tif','swamp_protected.tif')
# Create a constant raster to use for area calculations
wbt.multiply(swamp_landcover,0,'zeroraster.tif')
wbt.add('zeroraster.tif',1,'constantraster.tif')
# Carry out zonal statistics to get the area of each combination of landcover/protected status.
wbt.zonal_statistics('constantraster.tif','swamp_protected.tif',output=None,stat='total',out_table='swamp_protected.html')

# ==========================================
#   HABITAT BLOCKS AND RIPARIAN CORRIDORS
# ==========================================

# Double the riparian corridor binary before adding to habitat blocks.
wbt.multiply(riparian,2,'riparian2.tif')
# Binarize habitat clumps.
wbt.greater_than(hb,0,'hb_binary.tif',incl_equals=False)
# Add habitat blocks and riparian corridor so 0=neither, 1=habitat block, 2=riparian corridor, 3=both.
wbt.add('hb_binary.tif','riparian2.tif','habitatriparian.tif')
# Multiply by ten before adding to original classification.
wbt.multiply('habitatriparian.tif',10,'habitatriparian_10.tif')
# Add zero/ten/twenty/thirty to original swamp landcover.
wbt.add(swamp_landcover,'habitatriparian_10.tif','swamp_hab_rip.tif')
# Carry out zonal statistics to calculate the area of each combination of landcover & habitat/riparian.
wbt.zonal_statistics('constantraster.tif','swamp_hab_rip.tif',output=None,stat='total',out_table='swamp_hab_rip.html')

# ==========================================
#   STATE SIGNIFICANCE
# ==========================================

# Multiply state significasnt communities binary by ten before adding to landcover.
wbt.multiply(significant, 10, 'sig10.tif')
# Add state significance to landcover to get twelve classes.
wbt.add('sig10.tif',swamp_landcover,'swamp_sig.tif')
# Carry out zonal statistics to get the number of cells in each class,
# from which we can calculate the percent significant by land cover type.
wbt.zonal_statistics('constantraster.tif','swamp_sig.tif',output=None,stat='total',out_table='swamp_sig.html')

# ==========================================
#   CREATE CHARTS IN GOOGLE SHEETS
# ==========================================

#   Go to this link to paste results from zonal statistics and generate charts:
#   https://docs.google.com/spreadsheets/d/1j7zxvLrIyrl-VepVu4NiPnDPaNeGREOiFyCdB9DF2i4/edit?usp=sharing
