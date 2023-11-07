# -------------------------------------------------------
# -------------------------------------------------------
FROM iztokkucan/pybase:0.2.0

USER root

RUN mkdir -p /scratch
RUN rm -f /scratch/*
WORKDIR /scratch

RUN . /root/.bashrc && mamba create     n sxo

RUN mkdir -p /scratch/linux-64
RUN mkdir -p /scratch/noarch
COPY channeldata.json /scratch/
COPY ik.sxo-v*.tar.bz2 /scratch/linux-64
COPY repodata-linux-64.json /scratch/linux-64/repodata.json
COPY repodata-noarch.json /scratch/noarch/repodata.json
RUN . /root/.bashrc && mamba install -yq -n sxo -c /scratch ik.sxo

RUN rm -rf /scrath/*
ENV PATH=$PATH:/opt/mambaforge/bin
