.DEFAULT_GOAL := help

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

logs:
	@docker-compose logs -f

# Django commands
shell:
	@docker-compose run --rm -e SHELL=True web

migrations:
	@docker-compose run --rm -e MIGRATIONS=True web

migrate:
	@docker-compose run --rm -e MIGRATE=True web

populate:
	@docker-compose exec web python manage.py populate

# Test commands
test:
	@docker-compose exec web python manage.py test

createsuperuser:
	@docker-compose exec web python manage.py createsuperuser

collectstatic:
	@docker-compose exec web python manage.py collectstatic --no-input

help:
	@echo "Comandos disponíveis:"
	@echo "  build    : Constrói as imagens Docker"
	@echo "  up       : Inicia os containers Docker"
	@echo "  down     : Para os containers Docker"
	@echo "  migrations: Cria as migrações do banco de dados"
	@echo "  migrate  : Aplica as migrações do banco de dados"
	@echo "  test     : Executa os testes do projeto"
	@echo "  shell    : Abre o shell do Django"
	@echo "  logs     : Exibe os logs dos containers"
	@echo "  populate : Popula o banco de dados com dados iniciais"
	@echo "  createsuperuser: Cria um superusuário"
	@echo "  collectstatic: Coleta os arquivos estáticos"