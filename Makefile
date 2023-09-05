BUILD_NAME?=nlp-toolkit
SVC_TAG?=latest
SSH_HOST :=git@github.com
SSH_PATH :=Kavender/nlp_toolkit.git

# Docker configuration
DOCKER_IMG := $(BUILD_NAME):$(SVC_TAG)
DOCKERFILE := Dockerfile

# AWS ENVIRONMENT VARIABLES - Needed for Local Only
PWD = $(shell pwd)

all:
	$(MAKE) local

local:
	$(MAKE) build
	$(MAKE) run

sh:
	$(MAKE) run cmd="/bin/bash"

unit:
	$(MAKE) run cmd="python -m pytest ."

lint:
	$(MAKE) run cmd="python -m flake8 . --count"


black:
	$(MAKE) run cmd=run cmd="/bin/bash -c 'pip install black==19.10b0 click==8.0.4 typed_ast==1.5.0 && black -l 120 .'"

test:
	$(MAKE) run cmd="python -m pytest $(TEST)"

build:
	# Build the base dependencies image
	docker build --rm \
		-f Dockerfile \
		--build-arg SSH_HOST=$(SSH_HOST) \
		--build-arg SSH_PATH=$(SSH_PATH) \
		-t $(DOCKER_IMG) \
		.

run:
	$(MAKE) stop
	docker run \
	    -it \
		-v $(PWD)/:/libs \
		--name $(BUILD_NAME) \
		$(DOCKER_IMG) \
		$(cmd)

stop:
	docker stop $(BUILD_NAME) || true && docker rm $(BUILD_NAME) || true

clean:
	docker rmi $(DOCKER_IMG)
