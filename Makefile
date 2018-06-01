.PHONY: syncdb user up down ps test

syncdb:
	@docker-compose exec proxy python3 proxy/manage.py makemigrations
	@docker-compose exec proxy python3 proxy/manage.py migrate

user:
	@docker-compose exec proxy python3 proxy/manage.py createsuperuser

up:
	@docker-compose up -d --build

down:
	@docker-compose down

ps:
	@docker-compose ps

test:
	@docker-compose exec proxy python3 proxy/manage.py test proxy/
