# GIS 5653 Term project
# Summer 2022
# Ben Stone
# Main file

# The eventual goal for this project is to identify the state parks in South Dakota near Interstate 90.

# Import system modules
import arcpy
import os
import sys
import pathlib

from arcpy import env
arcpy.env.overwriteOutput = True

from pathlib import Path

# Set workspace
arcpy.env.workspace = "C:/Users/Ben/Dropbox/OU/GIS 5653 - Spatial Programming/Term Project/BStone_GIS5653-999_TermProject"

# Import custom module
BStone_MyModule = "C:/Users/Ben/Dropbox/OU/GIS 5653 - Spatial Programming/Term Project/BStone_GIS5653-999_TermProject"
sys.path.append(BStone_MyModule)
import BStone_MyModule
BStone_MyModule.user_input()

# Set output geodatabase variables
outDir = "C:/Users/Ben/Dropbox/OU/GIS 5653 - Spatial Programming/Term Project/BStone_GIS5653-999_TermProject"
out_name = "term_project.gdb"

# Create geodatabase
arcpy.CreateFileGDB_management(outDir, out_name)

if not os.path.exists(outDir):
    os.mkdir(outDir)
    
# Set input variables
natl_interstates = "Default.gdb/tl_2021_us_primaryroads"
us_states = "Default.gdb/tl_2021_us_state"
sd_parks = "Default.gdb/Parks_And_Recreation_Areas"

print("Please wait a moment...")

# Project tool: 
# NAD 1983 (2011) StatePlane South Dakota S FIPS 4002 (US Feet)

# Set variables
natl_interstates_projected = "term_project.gdb/natl_interstates_projected"
us_states_projected = "term_project.gdb/us_states_projected"
sd_parks_projected = "term_project.gdb/sd_parks_projected"
SD_StatePlane_CS = arcpy.SpatialReference('NAD 1983 (2011) StatePlane South Dakota S FIPS 4002 (US Feet)')

# Execute Project tool
arcpy.management.Project(sd_parks, sd_parks_projected, SD_StatePlane_CS)
arcpy.management.Project(natl_interstates, natl_interstates_projected, SD_StatePlane_CS)
arcpy.management.Project(us_states, us_states_projected, SD_StatePlane_CS)



# Select tool
# Interstate 90
# Set variables
in_features_interstate = natl_interstates_projected
out_feature_class_interstate = interstate_90 = "term_project.gdb/interstate_90"
where_clause_interstate = '"FULLNAME" = \'I-90\' or "FULLNAME" = \'I- 90\''

# Execute Select tool
arcpy.analysis.Select(in_features_interstate, out_feature_class_interstate, where_clause_interstate)

# South Dakota
# Establish variables
in_features_state = us_states_projected
out_feature_class_state = south_dakota = "term_project.gdb/south_dakota"
where_clause_state = '"STATEFP" = \'46\''

# Execute Select tool
arcpy.analysis.Select(in_features_state, out_feature_class_state, where_clause_state)



# Clip tool
# Establish variables
interstate_90_within_south_dakota = "term_project.gdb/interstate_90_within_south_dakota"
in_features_clip = interstate_90
clip_features = south_dakota

# Execute Clip tool
arcpy.analysis.Clip(in_features_clip, clip_features, interstate_90_within_south_dakota)



# Near tool
# Set variables
in_features_near = sd_parks_projected
near_features = interstate_90_within_south_dakota
search_radius = "30 miles"

# Execute Near tool
arcpy.analysis.Near(in_features_near, near_features, search_radius)



# Select by Attributes tool & Copy Features tool
# Set variables
sd_parks_large = "term_project.gdb/sd_parks_large"
sd_parks_small = "term_project.gdb/sd_parks_small"

# Large parks 
# Select parks equal to or larger than 50 acres where the NEAR_FID field is not -1. 
lg_parks_selection = arcpy.management.SelectLayerByAttribute(sd_parks_projected, "NEW_SELECTION", '"ACRES" >= 50 and "NEAR_FID" <> -1')

# Copy selected features into new shapefile
arcpy.management.CopyFeatures(lg_parks_selection, sd_parks_large)

# Small parks
# Select parks smaller than 50 acres where the NEAR_FID field is not -1. 
sm_parks_selection = arcpy.management.SelectLayerByAttribute(sd_parks_projected, "NEW_SELECTION", '"ACRES" < 50 and "NEAR_FID" <> -1')

# Copy selected features into new shapefile
arcpy.management.CopyFeatures(sm_parks_selection, sd_parks_small)



# Summary Statistics tool
# Set variables
parks_lg_stats = "term_project.gdb/stats_sd_parks_large"
parks_sm_stats = "term_project.gdb/stats_sd_parks_small"
stats_fields = [["ACRES", "SUM"]]

arcpy.analysis.Statistics(sd_parks_large, parks_lg_stats, stats_fields)
arcpy.analysis.Statistics(sd_parks_small, parks_sm_stats, stats_fields)



# For loops
print()
print("The following is a list of large parks, 50 acres in size or larger, within a 30 mile distance from I-90 in South Dakota:")
values_lg = arcpy.SearchCursor(sd_parks_large)
for value in values_lg:
    Name = value.getValue("ParkName")
    County = value.getValue("COUNTY")
    Acres = (int(value.getValue("ACRES")))
    print(f"{Name} State Park, in {County} County, which about {Acres} acres in size.")
print()

print("The following is a list of small parks, less than 50 acres in size, within a 30 mile distance from I-90 in South Dakota:")
values_sm = arcpy.SearchCursor(sd_parks_small)
for value in values_sm:
    Name = value.getValue("ParkName")
    County = value.getValue("COUNTY")
    Acres = (int(value.getValue("ACRES")))
    print(f"{Name} State Park, in {County} County, which about {Acres} acres in size.")    
print()
