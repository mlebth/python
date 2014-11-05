#to set working document to location of current map
mxd = arcpy.mapping.MapDocument("CURRENT")

#create random points
arcpy.CreateRandomPoints_management("D:\\filepath","gravellyclippoints1","filename","otherfilename",number of points)

#dissolve
arcpy.Dissolve_management("gravellyclip","gravellyclippoints")

#erase behind some other feature (basically a reverse clip)
arcpy.Erase_analysis("loams","Unburned Portions of Park","loamyclip")

#create buffers around a feature
arcpy.Buffer_analysis("sand-gravel-loam","soilbuffer","1 FOOT")

#clip analysis
arcpy.Clip_analysis("sandydissolve","Burn_Severity_Clipped nb, sc, lb","sandlo")

#To determine whether featureclass is projected
fc="D:\\Research\\GIS files\\gravelhipoints3.shp"
desc = arcpy.Describe(fc)
sr= desc.spatialReference

if sr.type == "Projected":
    print "projected"
else:
    print "nope"

#Batch project
import arcpy
arcpy.env.workspace = r"D:\Research\GIS files\Soils"

arcpy.BatchProject_management(["citylim.shp", "flood.shp", "faultzn.shp"], "C:/data/output/batchproject", "",  "C:/data/usa.gdb/templatefc")

# ##########################################Name: BatchProject.py
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
        
# Output workspace
#THIS IS WHERE THE REPROJECTED SHAPEFILES WILL BE SAVED, THIS FOLDER MUST EXIST
out_workspace = r"D:\Research\GIS files\Soils" 

# Output coordinate system - leave it empty
#IF YOU ARE NOT USING A TEMPLATE SHAPEFILE,
#YOUR PROJECTION PARAMETERS WOULD GO IN HERE
out_cs = ''

# Template dataset - it has GCS_North_American_1983 coordinate system
template = "D:\Research\GIS files\Boundaries"

# Geographic transformation - 
transformation = "whatever it is"

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