# -------------------------------------------------------
# -------------------------------------------------------
FROM iztokkucan/selenium:0.1.0

USER root

RUN mkdir -p /scratch
WORKDIR /scratch

COPY grab.py /scratch
COPY mainline.sh /scratch
RUN chmod ugo+x /scratch/mainline.sh

USER selenium
ENTRYPOINT ["/scratch/mainline.sh"]
