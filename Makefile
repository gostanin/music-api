docker_up:
	docker-compose -p music-api up -d --build --remove-orphans --force-recreate

docker_test:
	docker-compose -p music-api exec -T api python -B -m pytest

docker_stop:
	docker-compose -p music-api docker_stop

docker_down:
	docker-compose -p music-api down