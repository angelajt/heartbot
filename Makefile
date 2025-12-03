TAG := 0.$(shell date +%Y.%m.%d.%H%M)
export TAG

all: build caddy-build push caddy-push restart

build:
	docker build -f docker/Dockerfile -t us-central1-docker.pkg.dev/heartbot2/heartbot/heartbot:$(TAG) docker

push:
	docker push us-central1-docker.pkg.dev/heartbot2/heartbot/heartbot:$(TAG)

restart:
	docker-compose --env-file docker/local/.env -H "ssh://angela@34.171.194.61" down
	docker-compose --env-file docker/local/.env -H "ssh://angela@34.171.194.61" up -d

caddy-build:
	docker build -f caddy/Dockerfile -t us-central1-docker.pkg.dev/heartbot2/heartbot/caddy:latest caddy

caddy-push:
	docker push us-central1-docker.pkg.dev/heartbot2/heartbot/caddy:latest

