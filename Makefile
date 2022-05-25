
.PHONY: server
server:
	docker compose up -d app

.PHONY: stop
stop:
	docker compose stop

.PHONY: logs
logs:
	docker compose logs -f

.PHONY: consumer
consumer:
	docker compose run --rm  consumer

.PHONY: producer
producer:
	docker compose run --rm producer

.PHONY: manage
manage:
	docker compose run --rm app poetry run python manage.py $(ARGS)

.PHONY: es
es:
	docker compose up -d es
