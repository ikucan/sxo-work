# -------------------------------------------------------
# -------------------------------------------------------
FROM iztokkucan/pybase:0.2.0

WORKDIR /scratch

# pre-reqs for chrome
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

COPY selenium-env.yml /scratch
ENV PATH=$PATH:/opt/mambaforge/bin
ENV PATH=$PATH:/opt/miniforge/bin
RUN echo $PATH
RUN mamba list
RUN mamba env create -f selenium-env.yml

RUN rm -Rf /scratch/*

RUN useradd -ms /bin/bash selenium
USER selenium
RUN mamba init

WORKDIR /home/selenium
