# -------------------------------------------------------
# -------------------------------------------------------
FROM linuxserver/openssh-server:latest

RUN apk add tree htop

RUN mkdir /.ssh
COPY id_rsa.pub /.ssh
