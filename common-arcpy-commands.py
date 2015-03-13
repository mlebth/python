import arcpy
#to set working document to location of current map
mxd = arcpy.mapping.MapDocument("CURRENT")

#set workspace
arcpy.env.workspace = r"D:\Research\GIS files\Soils"

#create random points
arcpy.CreateRandomPoints_management("D:\\filepath","gravellyclippoints1","filename","otherfilename",number of points)

#dissolve
arcpy.Dissolve_management("gravellyclip","gravellyclippoints")

#intersect
arcpy.Intersect_analysis(["buescherbuffer_parkclip1","buescher sands"],r"D:\Research\GIS files\Soils\bueschersandsearch")

#erase behind some other feature (basically a reverse clip)
arcpy.Erase_analysis("loams","Unburned Portions of Park","loamyclip")

#create buffers around a feature
arcpy.Buffer_analysis("sand-gravel-loam","soilbuffer","1 FOOT")

#clip analysis
arcpy.Clip_analysis("sandydissolve","Burn_Severity_Clipped nb, sc, lb","sandlo")

#add coordinates
arcpy.AddXY_management("bueschersanddemogpoints51")

#export columns from attribute table to ASCII file
arcpy.ExportXYv_stats("AllPlots2014","PlotID;POINT_X;POINT_Y","COMMA","allplots4.txt")

# KMZ or KML to layer file ---------------------------------------------
arcpy.KMLToLayer_conversion(r'D:\Research\GIS files\Buescher_SP_Trails.kmz',r'D:\Research\GIS files','bueschertrails')

#To determine whether featureclass is projected
fc="D:\\Research\\GIS files\\gravelhipoints3.shp"
desc = arcpy.Describe(fc)
sr= desc.spatialReference

if sr.type == "Projected":
    print "projected"
else:
    print "nope"

#Batch project
arcpy.BatchProject_management(["citylim.shp", "flood.shp", "faultzn.shp"], "C:/data/output/batchproject", "",  "C:/data/usa.gdb/templatefc")

# ----------------Name: BatchProject.py (long form)
# Description: Changes coordinate systems of several datasets in a batch.

import arcpy, os #USE OPERATING SYSTEM FUNCTIONS
from arcpy import env

#THIS IS THE PATH TO YOUR DATA
mypath = r"D:\Research\GIS files\Soils"

#THIS IS AN EMPTY LIST WHERE WE WILL STORE OUR SHAPEFILE NAMES
shapefiles = []

# Set workspace environment
env.workspace = mypath

# Input feature classes
#HERE WE WILL USE THE OS.PATH FUNCTIONS TO GET A CRUDE LIST OF ALL
#OF THE SHAPEFILES IN THE DIRECTORY, BY GETTING A LIST OF ALL FILES
#IN THE DIRECTORY AND THEN FILTERING OUT ONLY FILES WITH THE .SHP EXTENSION
for filename in os.listdir(mypath):
    if filename.endswith('.shp'):
        shapefiles.append(filename)
        #emb addition
        print filename

input_features = []
for root, dirnames, filenames in os.walk(env.workspace):
  for filename in fnmatch.filter(filenames, '*.shp'):
      input_features.append(os.path.abspath(os.path.join(root, filename)))

# Output workspace
#THIS IS WHERE THE REPROJECTED SHAPEFILES WILL BE SAVED, THIS FOLDER MUST EXIST
out_workspace = r"D:\Research\GIS files\Soils" 

# Output coordinate system - leave it empty
#IF YOU ARE NOT USING A TEMPLATE SHAPEFILE,
#YOUR PROJECTION PARAMETERS WOULD GO IN HERE
out_cs = ''

# Template dataset - it has GCS_North_American_1983 coordinate system
template = r"D:\Research\GIS files\Boundaries\boundpy6_nov2007.shp"

# Geographic transformation - 
transformation = "WGS_1984_(ITRF00)_To_NAD_1983_HARN"

#THE TRY/EXCEPT STRUCTURE IS USED TO CATCH ANY ERRORS AND RETURN THE ERROR MESSAGES
try:
   #THIS LINE SETS UP THE BATCHPROJECT PARAMETERS
   res = arcpy.BatchProject(input_features, out_workspace, out_cs, template, transformation)
   if res.maxSeverity == 0: #THIS RUNS THE PROJECTION FOR ALL OF THE LISTED LAYERS
      print "projection of all datasets successful"
   else:
      print "failed to project one or more datasets"
except:
   print res.getMessages() #DISPLAYS ANY ERROR MESSAGES

# ------------------------END BATCH PROJECT LONG FORM

# -------------------TO EXTRACT RASTER VALUES TO A POINT SHAPEFILE
# Import system modules
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute ExtractValuesToPoints
ExtractValuesToPoints(inPointFeatures, inRaster, outPointFeatures, "INTERPOLATE", "VALUE_ONLY")
# EX to get aspect into allplots, interpolating from adjacent cells:
ExtractValuesToPoints("AllPlots2014","us_asp2010","plotaspects.shp","INTERPOLATE")
    #Note that Interpolate and Value_only are optional values.
# -------------------END EXTRACT RASTER VALUES