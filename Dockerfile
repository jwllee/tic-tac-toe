FROM ubuntu:18.04
LABEL maintainer "Wai Lam Jonathan Lee <jonathan.wailam.lee@gmail.com>"

ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV QT_VERSION v5.9.1
ENV QT_CREATOR_VERSION v4.3.1

# Build prequisites
RUN apt-get update && apt-get install -y \
	qtbase5-dev \
	libxcb-xinerama0-dev \
	python \
	make \
	build-essential 

# Other useful tools
RUN apt-get update && apt-get install -y \
	wget \
	zip \
	git \
	vim

ENV HOME=/home/jonny
WORKDIR $HOME

# setup dotfiles
RUN git clone --recursive https://github.com/jwllee/dotfiles.git \
	&& cd dotfiles && make 

# setup vim
RUN git clone --recursive https://github.com/jwllee/.vim.git .vim \
	&& ln -sf /.vim/vimrc /.vimrc \
	&& cd $HOME/.vim \
	&& git submodule update --init

# standard locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
# set locales UTF-8
RUN apt-get update && apt-get install -y \
	locales && locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8

RUN mkdir -p /qt/build
WORKDIR /qt/build

ADD build_qt.sh /qt/build/build_qt.sh
RUN QT_VERSION=$QT_VERSION QT_CREATOR=$QT_CREATOR_VERSION /qt/build/build_qt.sh

WORKDIR $HOME

RUN useradd --home-dir $HOME jonny \
	&& groupadd code \
	&& gpasswd -a jonny code \
	&& chown -R jonny:jonny $HOME

USER jonny
