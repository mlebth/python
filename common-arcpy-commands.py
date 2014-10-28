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
...     print "projected"
... else:
...     print "nope"


