#!/bin/sh

#-----------------------------------------------------------------------------------------
# Utility to create shp files from jp2 from a selective band ( S Jain )
#-----------------------------------------------------------------------------------------

display_usage() {

    echo "Usgae: $0 S1_PRD_YYYYMM_a2.txt "
    exit 1
}

#----------------------------------------------
# Checking input parameters
#----------------------------------------------

if [ $# -ne 2 ]; then
    display_usage
fi

if [[ $1 =~ "S2" ]] ; then
   sat="Sentinel2"

else
   display_usage
fi

#----------------------------------------------
# Get Product and Year Month
#----------------------------------------------

echo $1
echo $sat

if [[ $1 =~ "L1C" ]] ; then
   prod=`echo $1 | cut -c4-6`
   yr=`echo $1 | cut -c8-11`
   mm=`echo $1 | cut -c12-13`
   yrmn=${yr}-${mm}

else
        display_usage
fi

SATELLITE=${sat}
if [[ ${SATELLITE} =~ "Sentinel2" ]]; then
      SOURCE_DIR="/g/data/fj7/MSI/Sentinel-2/${prod}/"
fi

MONTH=${yrmn}
echo ${SOURCE_DIR}


DEST_DIR=`pwd`
DATA_IN_DIR=${SOURCE_DIR}${MONTH}"/"

echo $2
if [[ $2 =~ "1BAND" ]] || [[ $2 =~ "3BAND" ]]; then
        if [[ $2 =~ "1BAND" ]]; then
                BAND_FILTER='B01.jp2'
        fi
        if [[ $2 =~ "3BAND" ]]; then
                BAND_FILTER='B02.jp2\|B03.jp2\|B04.jp2'
        fi
else
    display_usage
fi

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

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
        echo "Downloading ..."
        while [ $i -le ${v1} ]
        do
                unzip -j *.zip ${arr[$i]} -d .
                i=$(($i+4))
        done
        echo "Building Shape File "
        gdaltindex -t_srs EPSG:4326 -src_srs_name src_srs S2_Shape_${MONTH}.shp `find . -name "*B*.jp2"`
        echo "Created Shape file S2_Shape_${MONTH}.shp"

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

        zip_var=(`ls S2*.zip`)
        for var in S2*.jp2
        do
                echo "${zip_var},${var}" >> S2_Collection_${MONTH}.txt
        done
#-----------------------------------------------------------------------------------------
#       Cleaning files
#-----------------------------------------------------------------------------------------

        rm -f ${DEST_DIR}"/"*.jp2
        unlink  ${DEST_DIR}"/"$line
        echo "Count = ${count}"
        echo "------------------------------------------"

done < $1
