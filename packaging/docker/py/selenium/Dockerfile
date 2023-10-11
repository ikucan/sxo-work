# -------------------------------------------------------
# -------------------------------------------------------
# FROM iztokkucan/pybase:0.0.2
FROM iztokkucan/pybase:0.1.0

WORKDIR /scratch

# move to base
RUN apt-get install -qq unzip
RUN apt-get install -qq libglib2.0-dev
RUN apt-get install -qq libnss3
RUN apt-get install -qq libatk1.0
RUN apt-get install -qq libatk-bridge2.0
RUN apt-get install -qq cups
RUN apt-get install -qq libdrm-dev
RUN apt-get install -qq libxkbcommon-dev
RUN apt-get install -qq libxcomposite-dev
RUN apt-get install -qq libxdamage-dev
RUN apt-get install -qq libxrandr-dev
RUN apt-get install -qq libgdm-dev
RUN apt-get install -qq libgbm-dev
RUN apt-get install -qq libpango1.0-dev
RUN apt-get install -qq libasound-dev

ENV CHROME_VERSION="117.0.5938.149"
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip

RUN unzip chrome-linux64.zip
RUN unzip chromedriver-linux64.zip

RUN cp -Rfd chrome-linux64/* /bin/
RUN cp -Rfd chromedriver-linux64/* /bin/

#RUN rm -Rf /scratch/*


# # install chrome
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install -qq ./google-chrome-stable_current_amd64.deb
# RUN rm google-chrome-stable_current_amd64.deb

# RUN google-chrome --version | sed "s/[A-z ]*//" > chrome_ver

# # install chrome driver
# #RUN wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip
# RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip

# # create a selenium conda env;
# RUN unzip chromedriver_linux64.zip
# RUN mv -f chromedriver /bin/

COPY selenium-env.yml /scratch
ENV PATH=$PATH:/opt/mambaforge/bin
ENV PATH=$PATH:/opt/miniforge/bin
RUN echo $PATH
RUN mamba list
RUN mamba env create -f selenium-env.yml
# RUN rm /scratch/*

RUN useradd -ms /bin/bash selenium
USER selenium
RUN mamba init

WORKDIR /home/selenium
