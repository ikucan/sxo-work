# -------------------------------------------------------
# -------------------------------------------------------
FROM debian:buster-slim

# use bash instead of sh
SHELL ["/bin/bash", "-c"]

# install some basic tools
RUN apt-get update
RUN apt-get install -qq vim tree htop dstat tmux
RUN apt-get install -qq curl wget
RUN apt-get install -qq unzip


RUN mkdir /scratch
WORKDIR /scratch

#RUN wget -q --show-progress https://github.com/conda-forge/miniforge/releases/download/4.14.0-0/Mambaforge-4.14.0-0-Linux-x86_64.sh
RUN wget -q --show-progress https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

#RUN /bin/bash /scratch/Mambaforge-4.14.0-0-Linux-x86_64.sh -b -p /opt/mambaforge
RUN /bin/bash /scratch/Miniforge3-Linux-x86_64.sh -b -p /opt/miniforge

#RUN /opt/mambaforge/bin/conda init -v
RUN /opt/miniforge/bin/conda init -v

COPY bashrc.template /scratch
RUN  cat /scratch/bashrc.template >> ~/.bashrc
RUN  source ~/.bashrc && mamba install conda-lock  -y

WORKDIR /root
