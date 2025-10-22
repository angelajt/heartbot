TAG := 0.$(shell date +%Y.%m.%d.%H%M)
export TAG

all: build push restart

build:
	docker build -f docker/Dockerfile -t us-central1-docker.pkg.dev/heartbot2/heartbot/heartbot:$(TAG) docker

push:
	docker push us-central1-docker.pkg.dev/heartbot2/heartbot/heartbot:$(TAG)

restart:
	docker-compose --env-file docker/local/.env -H "ssh://angela@34.171.194.61" down
	docker-compose --env-file docker/local/.env -H "ssh://angela@34.171.194.61" up -d
