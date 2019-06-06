FROM ubuntu:18.04
LABEL maintainer "Wai Lam Jonathan Lee <jonathan.wailam.lee@gmail.com>"

ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Build prequisites
RUN apt-get update && apt-get install -y \
	python3 \
	python3-dev \
	python3-pip \
	python3-venv \
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

RUN apt-get update && apt-get install -y \
	libgl1-mesa-glx \
	qtbase5-dev

# fpm package manager required by fps to freeze qt applications in linux
RUN apt-get update && apt-get install -y \
	ruby \
	ruby-dev \
	rubygems \
	&& gem install --no-ri --no-rdoc fpm

USER jonny

ENV VIRTUAL_ENV=$HOME/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin":$PATH
ENV PYTHONPATH="/home/jonny/.local/lib/python3.6/site-packages/":$PYTHONPATH

ADD ./setup_requirements.txt /tmp/setup_requirements.txt
RUN pip install -r /tmp/setup_requirements.txt

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
