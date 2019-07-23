DIR=$(shell pwd)
USER_UID=$(shell id -u)
DOCKER_IMAGE_ID=$(shell docker images --format="{{.ID}}" docker-pulseaudio-example:latest | head -n 1)
AUDIO_GROUPID=$(shell getent group audio | cut -d: -f3)

build-docker:
	docker build -t tic-tac-toe .

test-sound: build-docker
	echo "User ID: ${USER_UID}"
	docker run -it \
		-e PULSE_SERVER=unix:/run/user/${USER_UID}/pulse/native \
		-e DISPLAY=unix$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v /run/user/${USER_UID}/pulse:/run/user/1000/pulse \
		${DOCKER_IMAGE_ID}

# About passing pulse server when you pass display to docker as well so that
# sound continues to work:
# https://github.com/TheBiggerGuy/docker-pulseaudio-example/issues/1#issuecomment-312296665
run-container: build-docker
	echo "User ID: ${USER_UID}"
	docker run -it \
		-e DISPLAY=unix$(DISPLAY) \
		-e PULSE_SERVER=unix:/run/user/${USER_UID}/pulse/native \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v /run/user/${USER_UID}/pulse:/run/user/1000/pulse \
		-v $(DIR):/home/jwllee/code \
		--network="host" \
		tic-tac-toe /bin/bash
