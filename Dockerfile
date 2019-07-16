FROM ubuntu:18.04
LABEL maintainer "Wai Lam Jonathan Lee <jonathan.wailam.lee@gmail.com>"

ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV UNAME jwllee

# Build prequisites
RUN apt-get update && apt-get install -y \
	python3 \
	python3-dev \
	python3-pip \
	python3-venv \
	libxcb-xinerama0-dev \
	make \
	build-essential \
	pulseaudio \
	pulseaudio-utils \
	alsa-base \
	alsa-utils

# Other useful tools
RUN apt-get update && apt-get install -y \
	wget \
	zip \
	git \
	vim

ENV HOME=/home/${UNAME}
WORKDIR $HOME

# setup dotfiles
RUN git clone --recursive https://github.com/jwllee/dotfiles.git \
	&& cd dotfiles && make 

# setup vim
RUN git clone --recursive https://github.com/jwllee/.vim.git .vim \
	&& ln -sf /.vim/vimrc /.vimrc \
	&& cd $HOME/.vim \
	&& git submodule update --init

RUN export UNAME=$UNAME UID=1000 GID=1000 && \
	mkdir -p "/home/${UNAME}" && \
	echo "${UNAME}:x:${UID}:${GID}:${UNAME} User,,,:/home/${UNAME}:/bin/bash" >> /etc/passwd && \
	echo "${UNAME}:x:${UID}:" >> /etc/group && \
	mkdir -p /etc/sudoers.d && \
	echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${UNAME} && \
	chmod 0440 /etc/sudoers.d/${UNAME} && \
	chown ${UID}:${GID} -R /home/${UNAME} && \
	gpasswd -a ${UNAME} audio

COPY pulse-client.conf /etc/pulse/client.conf

# standard locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
# set locales UTF-8
RUN apt-get update && apt-get install -y \
	locales && locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8

RUN git config --global user.email "jonathan.wailam.lee@gmail.com" \
	&& git config --global user.name "Wai Lam Jonathan Lee" \
	&& git config --global commit.gpgsign false

RUN apt-get update && apt-get install -y \
	libgl1-mesa-glx \
	qt5-default \
	qtbase5-dev \
	qttools5-dev-tools

# fpm package manager required by fps to freeze qt applications in linux
RUN apt-get update && apt-get install -y \
	ruby \
	ruby-dev \
	rubygems \
	&& gem install --no-ri --no-rdoc fpm

USER $UNAME

ENV VIRTUAL_ENV=$HOME/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin":$PATH
ENV PYTHONPATH="/home/${UNAME}/.local/lib/python3.6/site-packages/":$PYTHONPATH

ADD ./setup_requirements.txt /tmp/setup_requirements.txt
RUN pip install -r /tmp/setup_requirements.txt

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# install pygame-menu
RUN git clone https://github.com/ppizarror/pygame-menu.git /tmp/pygame-menu \
	&& cd /tmp/pygame-menu \
	&& python setup.py install --user 

CMD ["jwllee", "-vvvv", "/dev/urandom"]
