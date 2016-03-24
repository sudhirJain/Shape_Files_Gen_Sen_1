#!/usr/bin/python

#-----------------------------------------------------------------------
#
# Author     :  S Jain
# Date       :  Feb 20, 2016
# Description:  This Python utility reads gml file templete and kml
#               file update the coordenates from kml file with
#               an additional point at the end making polygon as closed
#               one. Creates a temp gml file for this updating.  The temp
#               gml file is used for generating esri shape file.
# Revision   :
#-----------------------------------------------------------------------

import os
import sys
import glob

GML_PATH=os.getcwd()+'/'
GML_TEMPLATE_FILE="SENTINEL_1_TEMPLATE.gml"
GML_FL_PATH=GML_PATH+GML_TEMPLATE_FILE

GML_CORD_PATTERN_S="<gml:coordinates>"
GML_CORD_PATTERN_E="</gml:coordinates>"

KML_FILE_PAiTTERN="*.kml"
KML_FL_PATH=GML_PATH

KML_CORD_PATTERN_S="<coordinates>"
KML_CORD_PATTERN_E="</coordinates>"

GML_OUTPUT = "Sentinel1_Temp.gml"

gml_string=[]
kml_string=[]

def get_kml():
    kml_fl=glob.glob(KML_FL_PATH+KML_FILE_PAiTTERN)
    kml_fl.sort(reverse=True)
    return kml_fl[0]

def get_kml_string(fl):
    try:
        k_str=open(fl).read()
    except IOError:
        print "Erro in Opening template files !"
    return k_str


def main():

    global temp_files
    print GML_FL_PATH

    try:
        gml_string=open(GML_FL_PATH).read()
    except IOError:
        print "Erro in Opening template files !"

    kml_string = get_kml_string(get_kml())

    gml_inx_s=gml_string.index(GML_CORD_PATTERN_S) + len(GML_CORD_PATTERN_S)
    gml_inx_e=gml_string.index(GML_CORD_PATTERN_E)

    kml_inx_s=kml_string.index(KML_CORD_PATTERN_S) + len(KML_CORD_PATTERN_S)
    kml_inx_e=kml_string.index(KML_CORD_PATTERN_E)

    coord_string = kml_string[kml_inx_s:kml_inx_e]
    first_coord  = coord_string[0:coord_string.index(' ')]
    coord_string = coord_string + ' ' + first_coord
    coord_string = coord_string

    gml_string = gml_string[:gml_inx_s] + coord_string + gml_string[gml_inx_e:]

    print " Generated gml file ........."
    open(GML_OUTPUT,"w").write(gml_string)
    return 0


if __name__ == "__main__":

    if main() == 0:
        sys.exit(0)
