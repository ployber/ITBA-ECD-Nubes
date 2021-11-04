SOURCE=/media/pablo/Seagate\ Expansion\ Drive/SONA_VM/2017/
DESTINATION=/opt/borde/BIG2021/SONA_VM/2017

find "${SOURCE}" -type f > /tmp/backup.txt

time (cat /tmp/backup.txt | parallel -j 8 \
rsync -ah --no-compress --progress {} ${DESTINATION})


