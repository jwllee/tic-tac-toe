DIR=$(shell pwd)

build-docker:
	docker build -t tic-tac-toe .

run-container: build-docker
	docker run -it \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(DIR):/home/jonny/code \
		-e DISPLAY=unix$(DISPLAY) \
		--device /dev/snd:/dev/snd \
		tic-tac-toe /bin/bash

