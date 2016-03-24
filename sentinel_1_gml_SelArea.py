#!/usr/bin/python

#-----------------------------------------------------------------------
#
# Author      :  S Jain
# Date        :  Feb 20, 2016
# Description :  This Python utility reads gml file templete and kml
#               file update the coordenates from kml file with
#               an additional point at the end making polygon as closed
#               one. Creates a temp gml file for this updating.  The temp
#               gml file iis used for generating esri shape file.
#
# Revision    : March 9, 2016
# Description : Selected area parameters have been added in the global
#               section, so that shape files of the selected area can be
#               generated.
#
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

#-----------------------------------------------------------------------
#  Area Selction lon-min-e,lat-min-s log-max-e, lat-max-e
#-----------------------------------------------------------------------

LON_MIN_E   =  142
LAT_MIN_S   = -33

LON_MAX_E   =  143
LAT_MAX_S   = -32

SEL_AREA_STRING = ""
SEL_AREA_STRING = \
str(LON_MIN_E) + ',' + str(LAT_MIN_S) + ' ' + \
str(LON_MAX_E) + ',' + str(LAT_MIN_S) + ' ' + \
str(LON_MAX_E) + ',' + str(LAT_MAX_S) + ' ' + \
str(LON_MIN_E) + ',' + str(LAT_MAX_S)

SEL_AREA_LIST = SEL_AREA_STRING.split(' ')

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

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
        sys.exit(-1)

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

    kml_rec_coord = []
    kml_rec_coord = coord_string.split(' ')

#-----------------------------------------------------------------------
#   case 1 Check selected area diagnoal points with kml rec coordinates
#-----------------------------------------------------------------------

    r_flag = False
    for rc in kml_rec_coord:
        x,y=map(float,rc.split(','))
        if ( x >= LON_MIN_E ) and ( x <= LON_MAX_E ) and \
           ( y <= LAT_MAX_S ) and ( y >= LAT_MIN_S ):
            r_flag = True
            break

#-----------------------------------------------------------------------
#   case 2 Check kml diagnoal points with selcted area diagnol points
#-----------------------------------------------------------------------


    if not r_flag  :
        xll,yll=map(float,kml_rec_coord[1].split(','))
        xur,yur=map(float,kml_rec_coord[3].split(','))
        if ( xll > xur ):
            xll,yll=map(float,kml_rec_coord[0].split(','))
            xur,yur=map(float,kml_rec_coord[1].split(','))

            xll,yll=kml_rec_coord[0].split(',')
            xur,yur=kml_rec_coord[1].split(',')

        for rc in SEL_AREA_LIST:

            x,y=map(float,rc.split(','))
            if ( x >= xll ) and ( x <= xur ) and \
               ( y <= yur ) and ( y >= yll ):
                r_flag = True
                break


#-----------------------------------------------------------------------
#         Debug checks
#-----------------------------------------------------------------------
#    print '-----------------------------------------'
#    print gml_inx_s
#    print gml_inx_e
#    print gml_string[gml_inx_s:gml_inx_e]
#    print kml_inx_s
#    print kml_inx_e
#    print first_coord
#    print kml_string[kml_inx_s:kml_inx_e]
#    print kml_string


#    print LON_MIN_E
#    print LON_MAX_E
#    print LAT_MAX_S
#    print LAT_MIN_S
#    print kml_rec_coord
#    print SEL_AREA_LIST
#    print coord_string
#    print gml_string
#    print kml_rec_coord
#    print r_flag
#    print '-----------------------------------------'
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

    print " Generated gml file ........."
    open(GML_OUTPUT,"w").write(gml_string)
    if r_flag :
        return 0
    else:
        return -1


if __name__ == "__main__":

    if main() == 0:
        sys.exit(0)
    else:
        sys.exit(-1)
[
