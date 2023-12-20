cat *.csv | gawk -F\, -v PAIR=GBPUSD '{print substr($1,0,10)","$1","PAIR","$2","$3","$4","$5}' > xo.csv

# !!!!
cat  GBPUSD-20231208.csv | gawk -F\, -v PAIR=GBPUSD -v q=\" '{print q substr($1,0,10) q "," q $1 q "," q PAIR q "," $2 "," $3 "," $4 "," $5}' | sed "s/Z\"\,/\"\,/" > xo.csv
cat  GBPUSD-*.csv | gawk -F\, -v PAIR=GBPUSD -v q=\" '{print q substr($1,0,10) q "," q $1 q "," q PAIR q "," $2 "," $3 "," $4 "," $5}' | sed "s/Z\"\,/\"\,/" > xo.csv