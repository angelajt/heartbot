tag = 0.0

all: build push restart

build:
	docker build -f docker/Dockerfile -t us-central1-docker.pkg.dev/heartbot2/heartbot/heartbot:$(tag) docker

push:
	docker push us-central1-docker.pkg.dev/heartbot2/heartbot/heartbot:$(tag)

restart:
	docker-compose --env-file ./local/.env -H "ssh://angela@34.171.194.61" down
	docker-compose --env-file ./local/.env -H "ssh://angela@34.171.194.61" up -d
