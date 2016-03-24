#!/bin/sh

#-----------------------------------------------------------------------------------------
#
# Author     :  S Jain
# Date       :  Feb 20,2016
# Description:  Utilitiy to create shp files from kml files of Sentinel_1
#               The input to the utility is a list of files.
#
# Rev        :  07/03/2016
#            :  Checking Satellite, date month, and product from input
#
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#  Sentinel 1 GRD AND SLC Selection
#-----------------------------------------------------------------------------------------

# Usage Function

display_usage() {

    echo "Usgae: $0 S1_PRD_YYYYMM_a2.txt "
    exit 1
}

# Checking input parameters

if [ $# -ne 1 ]
then
    display_usage
fi

if [[ $1 =~ "S1" ]] ; then
   sat="Sentinel1"

else
   display_usage
fi

# Get Product and Year Month

if [[ $1 =~ "GRD" ]] || [[ $1 =~ "SLC" ]]; then

   prod=`echo $1 | cut -c4-6`
   yr=`echo $1 | cut -c8-11`
   mm=`echo $1 | cut -c12-13`
   yrmn=${yr}-${mm}

else
        display_usage
fi

SATELLITE=${sat}
if [[ ${SATELLITE} =~ "Sentinel1" ]]; then
      SOURCE_DIR="/g/data/fj7/SAR/Sentinel-1/${prod}/"
fi

#-----------------------------------------------------------------------------------------
# Month Selection
#-----------------------------------------------------------------------------------------

MONTH=${yrmn}
PRODUCT=`cut -d'/' -f 7 <<< ${SOURCE_DIR}`

DEST_DIR=`pwd`
DATA_IN_DIR=${SOURCE_DIR}${MONTH}"/"
BAND_FILTER='kml'
TOLERANCE=30
SENTINEL_TEMP_GML="Sentinel1_Temp.gml"
SENTINEL_TEMP_GFS="Sentinel1_Temp.gfs"

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


if [ $# -eq 0 ]
then
   display_usage
   exit 1
fi

rm -f Selected_Area_${MONTH}.txt
count=0
while read line
do
        arr=[]
        count=$((count+1))
        echo "------------------------------------------"
        echo $line
        ln -sf  ${DATA_IN_DIR}$line ${DEST_DIR}
        arr=(`unzip -l *.zip | grep ${BAND_FILTER} | sort`)
        v1=`echo ${#arr[@]}`
        v1=$((${v1}-1))
        i=3
        echo "        Downloading map_overlay.kml ........"
        while [ $i -le ${v1} ]
        do
                unzip -j *.zip ${arr[$i]} -d .
                i=$(($i+4))
        done
        echo "Finished Downloading kml ............"
        echo "Building gml file using template ...."

#        python sentinel_1_gml_AllArea.py
        python sentinel_1_gml_SelArea.py

#       ----------------------------------------------
#       check the status of python commsnd
#       ----------------------------------------------

        if [ $? -eq 0 ]; then

            echo "Finished Building gml file using template ...."
            echo "Shape File Building Started .................."
            echo "$line" >> Selected_Area_${MONTH}.txt
            ogr2ogr -wrapdateline -datelineoffset ${TOLERANCE}  -append -f "ESRI Shapefile" \
            ${SATELLITE}_${MONTH}_${PRODUCT}.shp ${SENTINEL_TEMP_GML}
            echo "Shape File Building Finished ................."
        fi

#-----------------------------------------------------------------------------------------
#       Cleaning files
#-----------------------------------------------------------------------------------------

        rm -f ${DEST_DIR}"/"*.kml
        unlink  ${DEST_DIR}"/"$line
        rm -f ${SENTINEL_TEMP_GML}
        rm -f ${SENTINEL_TEMP_GFS}
        echo "Count = ${count}"
        echo "------------------------------------------"

done < $1

