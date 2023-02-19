.PHONY: docs clean

COMMAND = docker-compose run --rm web /bin/bash -c
REDIS_COMMAND = docker exec -it exchange-api_redis_1 sh -c

PROD_BRANCH = main

build:
	docker-compose up -d --build

restart:
	docker-compose restart

run:
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose down && \
	docker-compose up -d

pip:
	pip freeze | xargs pip uninstall -y && \
	pip install -r requirements.txt

locale:
	python manage.py makemessages -l tr -i venv && \
	python manage.py makemessages -l en -i venv

redis-clear:
	$(REDIS_COMMAND) 'redis-cli flushall;'