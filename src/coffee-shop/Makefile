.PHONY: run db-migrate db-upgrade

run:
	docker-compose up -d

run-debug:
	docker-compose stop -t 0
	docker-compose run --rm --service-ports web

run-tests:
	docker-compose run --rm web poetry run py.test -s

db-migrate:
	docker-compose run --rm web poetry run flask db migrate

db-upgrade:
	docker-compose run --rm web poetry run flask db upgrade

