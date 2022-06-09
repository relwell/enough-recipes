
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

.PHONY: kubemanage
kubemanage:
	kubectl -n enough-recipes exec --stdin --tty $$(kubectl -n enough-recipes get pods | grep app | grep Running | cut -d' ' -f1 | head -n 1) -- poetry run python manage.py $(ARGS)

.PHONY: build-and-push
build-and-push:
	docker build -f prod.Dockerfile -t relwell/enough-recipes . ;\
	docker push relwell/enough-recipes

.PHONY: build-and-push-nginx
build-and-push-nginx:
	docker build -f nginx.Dockerfile -t relwell/enough-recipes-nginx . ;\
	docker push relwell/enough-recipes-nginx

.PHONY: kubedashpw
kubedashpw:
	kubectl -n kubernetes-dashboard create token admin-user | pbcopy
