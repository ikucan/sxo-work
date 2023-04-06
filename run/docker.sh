docker run -it -v /tmp/saxo_token:/tkn -v /data:/data:rw -e TOKEN_FILE=/tkn -e DATA_DIR=/data -e INSTRUMENTS=GBPUSD iztokkucan/sxo-data-feeds:0.0.2
