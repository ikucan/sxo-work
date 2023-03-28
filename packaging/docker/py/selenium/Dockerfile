# -------------------------------------------------------
# -------------------------------------------------------
FROM iztokkucan/pybase:0.0.1

WORKDIR /scratch

# move to base
RUN apt-get install -qq unzip

# install chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -qq ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

RUN google-chrome --version | sed "s/[A-z ]*//" > chrome_ver
 
# install chrome driver
RUN wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip

# create a selenium conda env;

RUN unzip chromedriver_linux64.zip
RUN mv -f chromedriver /bin/

COPY selenium-env.yml /scratch
ENV PATH=$PATH:/opt/mambaforge/bin
RUN echo $PATH
RUN mamba list
RUN mamba env create -f selenium-env.yml
RUN rm /scratch/*

RUN useradd -ms /bin/bash selenium
USER selenium
RUN mamba init



WORKDIR /home/selenium
