#Import arcpy and set workspace
import arcpy
from arcpy import env
env.workspace = "H:/UEP 235/A4_automation/Project/Python.gdb"

#identify feature classes in geodatabase
arcpy.ListFeatureClasses()

#List tables in geodatabase
arcpy.ListTables()

#Make layers for hurricane evacuation zones and florida block groups
arcpy.MakeFeatureLayer_management("HurricaneEvac_Zone_proj", "HurricaneEvac_lyr")
arcpy.MakeFeatureLayer_management("florida_blockgroups", "Censusbg_lyr")

#Join and copy features to create block group layer with ACS data
CensubgACSjoin = arcpy.management.AddJoin("Censusbg_lyr", 'GEOFIPS', 
'miami_ACS_blockgroup_2018', 'Geo_FIPS', 'KEEP_COMMON')
arcpy.management.CopyFeatures(CensubgACSjoin, "BG_ACS_lyr")


#Select hurricane evacuation zones with category 0
arcpy.analysis.Select("HurricaneEvac_lyr","Hurricane_Cat0_lyr","CATEGORY=0")

#Intersect bg data onto category 0 zones
arcpy.analysis.Intersect(["BG_ACS_lyr", "Hurricane_Cat0_lyr"], "HurrCat0bgroups_lyr", "ALL")

#Calculate summary income statistics for category 0
statsfields = [["SE_A14006_001", "Median"], ["SE_A14006_001", "Mean"]]
arcpy.analysis.Statistics("HurrCat0bgroups_lyr","SummaryIncomeCat0",statsfields)

for Cat_Num in [1,2,3,4,5]:
    Cat=str(Cat_Num)
    #Select hurricane evacuation zones with category 
    arcpy.analysis.Select("HurricaneEvac_lyr","Hurricane_Cat"+Cat+"_lyr","CATEGORY="+Cat)
    #Intersect bg data onto category 2 zones
    arcpy.analysis.Intersect(["BG_ACS_lyr", "Hurricane_Cat"+Cat+"_lyr"], "HurrCat"+Cat+"bgroups_lyr", "ALL")
    #Calculate summary income statistics for category 2
    statsfields = [["SE_A14006_001", "Median"], ["SE_A14006_001", "Mean"]]
    arcpy.analysis.Statistics("HurrCat"+Cat+"bgroups_lyr","SummaryIncomeCat"+Cat,statsfields)  


