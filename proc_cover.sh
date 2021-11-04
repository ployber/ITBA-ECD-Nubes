#!/bin/bash
#set -x


# script de ejecucion del calculo de porcentaje de covertura
# ejemplo de uso:
#./proc_cover.sh 2019 01 &>> out201901 &

YY=$1
MM=$2
SUF=$3
fileout="coverturas$YY$MM$SUF.txt"
c=0
touch $fileout
input="lista_cloud_cover_"$YY$MM$SUF
NICE=--20
lineas=`wc -l $input`
hostname
date
echo "$input"
echo "$fileout"
while IFS= read -r line
do
  let "c++"
  inicio=$SECONDS
  res=`eval "grep -c $line $fileout"`
  if [ $res -eq "0" ]; then
        python3 kmask.py -i "$line" -m mask_vmartelli.jpg >> $fileout
        fin=$SECONDS
        let duracion=fin-inicio
        echo $c"/"$lineas" "$duracion" "$line
  else
        fin=$SECONDS
        let duracion=fin-inicio
        echo $c"/"$lineas" hecho. "$line
  fi
done < "$input"
