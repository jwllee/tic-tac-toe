FROM ubuntu:18.04
LABEL maintainer "Wai Lam Jonathan Lee <jonathan.wailam.lee@gmail.com>"

ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Build prequisites
RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	libxcb-xinerama0-dev \
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

RUN git config --global user.email "jonathan.wailam.lee@gmail.com" \
	&& git config --global user.name "Wai Lam Jonathan Lee" \
	&& git config --global commit.gpgsign false

WORKDIR $HOME

RUN useradd --home-dir $HOME jonny \
	&& groupadd code \
	&& gpasswd -a jonny code \
	&& chown -R jonny:jonny $HOME

USER jonny

RUN pip3 install --user fbs PyQt5==5.9.2
