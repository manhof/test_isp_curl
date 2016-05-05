#!/bin/bash
test=$(curl -L -w '%{url_effective},%{http_code},%{remote_ip}:%{remote_port},%{speed_download},%{speed_upload},%{time_namelookup},%{time_connect},%{time_appconnect},%{time_pretransfer},%{time_redirect},%{time_starttransfer},%{time_total}' -o /dev/null -s "$1" -A "$2")
dts="$(TZ=America/New_York date +%D" "%T.%3N)"
echo "$dts","$1",\""$2"\",$test >> $3
exit 
