#!/bin/bash
#set -x
# modo optimista (casi) sin trapeo de errores

#work files
fileout="clasificados.txt"
fileerr="err.txt"
cmdlist="copiarimagenesclasificadas.sh"
touch $fileout
hostname
date

#Piwigo DB
host=192.168.0.100
dbname=piwigo
user=nubes
pw=clouds

#Directorios
DestDir="/tmp/SONA"
DestTodes=$DestDir"/todes"
DestTrain=$DestDir"/train"
DestTest=$DestDir"/test"

#
Porcentaje=20
let div=100/$Porcentaje

# Query a la db, lista files y clase
QRY="select i.path
          , CASE t.name 
                 WHEN 'Cumulus' THEN '1_cumulus'
                 WHEN 'Altocumulus y Cirrocumulus' THEN '2_altocumulus'
                 WHEN 'Cirrus y Cirrostratus' THEN '3_cirrus'
                 WHEN 'Cielo Claro' THEN '4_clearsky'
                 WHEN 'Stratocumulus, Stratus y Altostratus' THEN '5_stratocumulus'
                 WHEN 'Cumulonimbus y Nimbostratus' THEN '6_cumulonimbus'
                 WHEN 'Nubes varias' THEN '7_mixed'
             END clase
from pwg_images i 
   , pwg_tags t 
   , pwg_image_tag it  
   , pwg_categories c 
   , pwg_image_category ic 
where i.id = it.image_id 
  and it.tag_id = t.id 
  and i.id = ic.image_id  
  and ic.category_id = c.id 
  and c.id not in (7629, 7630, 7631, 7632, 7633, 7634, 7635, 7636);"

####################
# C O M I E N Z O
####################
echo "#!/bin/bash" > $cmdlist
echo "mkdir -p $DestTodes/{1_cumulus,2_altocumulus,3_cirrus,4_clearsky,5_stratocumulus,6_cumulonimbus,7_mixed}"  >> $cmdlist
#echo "cd /var/www/html/nubes/ " >> $cmdlist

# Ejecucion Query a la db
echo $QRY|mysql -u $user -D $dbname -p$pw -N > $fileout 2> $fileerr
# Script para actualizar la copia de los files al dir DestDir
cat $fileout|sed  's/^\.\//\/var\/www\/html\/nubes\//'|awk -v dest=$DestTodes '{print "cp "$1" "dest"/"$2}' >> $cmdlist

#Directorios
echo "mkdir -p $DestTrain/{1_cumulus,2_altocumulus,3_cirrus,4_clearsky,5_stratocumulus,6_cumulonimbus,7_mixed}"  >> $cmdlist
echo "mkdir -p $DestTest/{1_cumulus,2_altocumulus,3_cirrus,4_clearsky,5_stratocumulus,6_cumulonimbus,7_mixed}"  >> $cmdlist

#Ejec script
source $cmdlist

#Copia Porcentaje de files a train y test
#find $DestTodes -type f -exec dirname {} + | uniq -c | while read n d;do echo "Directory:$d Files:$n";let i=0;let um=$n/$div;echo $n,$um;find $d -type f | while read file;do let i++;if [ $i -gt $um ]; then cp $file $DestTrain`echo $d|sed 's/^.*\//\//g'`; else cp $file $DestTest`echo $d|sed 's/^.*\//\//g'`/; fi;done;echo "done1";done;echo "done2"
find $DestTodes -type f -exec dirname {} + | uniq -c | while read n d;do let i=0;let um=$n/$div;find $d -type f | while read file;do let i++;if [ $i -gt $um ]; then cp $file $DestTrain`echo $d|sed 's/^.*\//\//g'`; else cp $file $DestTest`echo $d|sed 's/^.*\//\//g'`/; fi;done;done;

#Output de cantidades
echo "Todes"
find $DestTodes -type f -exec dirname {} + | uniq -c 
echo "Train"
find $DestTrain -type f -exec dirname {} + | uniq -c 
echo "Test"
find $DestTest -type f -exec dirname {} + | uniq -c 

echo "Comprimiendo"
#zip -r clasificades $DestTrain $DestTest 2&1>> $fileerr
tar -czf clasificades.tar.gz -C $DestDir train test
ls -lh clasificades.tar.gz
echo "listo."


