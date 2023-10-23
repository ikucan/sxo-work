
# -------------------------------------------------------
# -------------------------------------------------------
FROM iztokkucan/sxo-base:0.2.1

USER root

RUN rm -Rf /scratch
RUN mkdir -p /scratch
WORKDIR /scratch


COPY capture.py /scratch
COPY capture.sh /scratch
RUN chmod ugo+x /scratch/capture.sh
ENV PATH=$PATH:/opt/mambaforge/bin
RUN . /root/.bashrc && mamba init

ENTRYPOINT ["/scratch/capture.sh"]
